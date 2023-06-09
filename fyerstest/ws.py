import websocket
from threading import Thread
import logging
from logging.config import dictConfig
import os
import sys
import threading
import time
import websockets
import json
import define


class FyersSocket:
    """
    A class for sending and receiving data via WebSocket for orders, trades, and positions.

    """

    def __init__(self, access_token,run_background, log_path=None): 
        self.__access_token = access_token
        self.__url = "wss://socket.fyers.in/trade/v3"
        self.log_path = log_path
        self.run_background = run_background
        self.OnMessage = None
        self.OnError = None
        self.OnOpen =  None
        self.__ws_object = None
        self.__url = "wss://socket.fyers.in/trade/v3"
        self.ErrResponse = {"code":-99,"message":"","s":"error"}
        self.logger_setup()
        self.websocket_task = None
        self.logger.info("Initiate socket object")
        self.logger.debug('access_token ' + self.__access_token)
        self.run_background=run_background
        self.background_flag = False
        self.socket_type = {
               "orderUpdate" : "trades,positions,orders",
               "OnOrders":"orders",
               "OnTrades":"trades",
               "OnPositions":"positions",
               "OnPriceAlert":"pricealerts",
               "OnEdis":"edis"}


    def parse_position_data(self, msg):
        try:
            position_data_keys = ["buy_avg", "buy_qty", "buy_val", "cf_buy_qty", "cf_sell_qty", "day_buy_qty", "day_sell_qty", "fy_token", "id", "net_avg",
                                   "net_qty", "pl_realized", "product_type", "segment", "sell_avg", "sell_qty", "sell_val", "symbol", "tran_side"]
            position_data = {key: msg['positions'][key] for key in position_data_keys}
            position_data.update({
                "qty_multi": msg['positions']['qty_multiplier'],
                "rbi_ref_rate": msg['positions']['rbirefrate'],
                "sym_desc": msg['positions']['symbol_desc']
            })

            return {
                "ws_type": 1,
                "s": msg["s"],
                "d": position_data,
            }
        except Exception as e:
            self.ErrResponse['message'] = 'Error while parshing position data'
            self.On_error(self.ErrResponse)

    def parse_trade_data(self, msg):
        try:
            trade_data_keys = ["id_fill", "id", "qty_traded", "price_traded", "traded_val", "product_type", "client_id", "id_exchange", "ord_type",
                                "tran_side", "symbol", "time_epoch", "fy_token"]
            trade_data = dict((key, msg['trades'][key]) for key in trade_data_keys)
            trade_data['tradeNumber'] = msg['trades']['id']

            return {
                "ws_type": 1,
                "s": msg["s"],
                "d": trade_data,
            }
        except Exception as e:
            self.ErrResponse['message'] = 'Error while parshing trade data'
            self.On_error(self.ErrResponse)


    def parse_orderUpdate_data(self, msg):
        try:
            keyMap = {
                "update_time_epoch_oms": "orderDateTime",
                "id": "exchOrdId",
                "product_type": "productType",
                "instrument": "instrument",
                "side": "side",
                "ord_status": "status",
                "qty": "qty",
                "qty_filled": "filledQty",
                "qty_remaining": "remainingQuantity",
                "ord_type": "type",
                "validity": "orderValidity",
                "offline_flag": "offlineOrder",
                "status_msg": "message",
                "symbol": "symbol",
                "fy_token": "fyToken",
                "segment": "segment",
                "dqQtyRem": "dqQtyRem",
                "price_limit": "limitPrice",
                "price_stop": "stopPrice",
                "qty_disc": "discloseQty",
                "price_traded": "tradedPrice",
            }
            order = msg["orders"]
            order_data = {keyMap[key]: order.get(key, 0) for key in keyMap}

            order_data["orderNumStatus"] = order["id"] + ":" + str(order["org_ord_status"])
            order_data["id"] = order["id"]
            order_data["slNo"] = int(time.time())

            return {
                "ws_type": 1,
                "s": msg["s"],
                "d": order_data,
            }
        except Exception as e:
            self.ErrResponse['message'] = 'Error while parshing order data'
            self.On_error(self.ErrResponse)



    def On_message(self,message):
        # if self.OnMessage is not None:
        #     self.OnMessage(message)
        # else:
        #     print('')
        #     print(f"Response : {message}") 
        response = json.loads(message)
        if "orders" in response:
            response = self.parse_orderUpdate_data(response)
        elif "positions" in response:
            response = self.parse_position_data(response)
        elif "trades" in response:
            response = self.parse_trade_data(response)
        else:
            pass
        
        if self.run_background:
            self.logger.debug(f"Response:{response}")
        else:
            print(f"Received response: {response}")
            self.logger.debug(f"Response:{response}")




    def On_error(self,message):
        self.logger.error(message)
        if self.OnError is not None:
            self.OnError(message)
        else:
            print(f"Error Response : {message}")


    def __on_error(self, error):
        try:
            print('Error:', error)
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error in on_error(): Line {}: {}".format(exc_tb.tb_lineno, str(e)))
            


    def __on_open(self, ws):
        try:
            print('WebSocket connection opened')
            if self.__ws_object is None:
                self.__ws_object = ws
                thread = threading.Thread(target=self.ping).start()

                # thread.join()

        except Exception as e:
            thread.join()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error in on_open(): Line {}: {}".format(exc_tb.tb_lineno, str(e)))

    def __on_close(self,ws, close_code, close_reason):

        self.On_message({ 
                    "code" : define.success_code,
                    "message" : define.connection_closed,
                    "s" : define.success
                })

    def ping(self):
        while self.__ws_object.sock.connected:
            self.__ws_object.send("Ping")
            print('-------ping----------')

            time.sleep(10)

    def init_connection(self):
        try:
            if self.__ws_object is None:
                if self.run_background:
                    self.background_flag = True
                header = {"authorization": self.__access_token}
                ws = websocket.WebSocketApp(
                    self.__url,
                    header = header,
                    on_message=lambda ws, msg: self.On_message(msg),
                    on_error=lambda ws, msg: self.__on_error(msg),
                    on_close=lambda ws , close_code, close_reason: self.__on_close(ws, close_code, close_reason),
                    on_open=lambda ws: self.__on_open(ws)
                    
                )

                self.t = Thread(target= ws.run_forever)
                self.t.daemon = self.background_flag
                self.t.start()

        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error in init_connection(): Line {}: {}".format(exc_tb.tb_lineno, str(e)))
	
    def close_connection(self):
        if self.__ws_object:
            self.__ws_object.close()
            self.__ws_object = None

    def keep_running(self):
        self.__ws_run = True
        t = Thread(target=self.infinite_loop)
        t.start()

    def infinite_loop(self):
        while(self.__ws_run):
            pass

    def subscribe(self, data_type):
        self.init_connection()
        if self.__ws_object is not None:
            self.data_type = [self.socket_type[(type)] for type in data_type.split(",")]
            message = json.dumps({"T": "SUB_ORD", "SLIST": self.data_type, "SUB_T": 1})
            self.__ws_object.send(message)


    def unsubscribe(self, data_type):
        if self.__ws_object is not None:
            self.data_type = [self.socket_type[(type)] for type in data_type.split(",")]
            message = json.dumps({"T": "SUB_ORD", "SLIST": self.data_type, "SUB_T": -1})
            self.__ws_object.send(message)


    def logger_setup(self):
        if self.log_path is None:
            self.log_path = os.getcwd()
        try:
            os.chmod(self.log_path, 0o750)
        except:
            self.log_path = os.getcwd()
            os.chmod(self.log_path, 0o750)
        LOGGING = {
			'version': 1,
			'disable_existing_loggers': False,
			'formatters': {
				'verbose': {
					'format': '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s - %(lineno)d - %(message)s'
				}
			},
			'handlers': {
				'console': {
					'class': 'logging.StreamHandler',
					'level': 'DEBUG',
					'formatter': 'verbose',
				},
				'file': {
					'class': 'logging.FileHandler',
					'level': 'DEBUG',
					'formatter': 'verbose',
					'filename': os.path.join(self.log_path, 'fyers_socket.log')
				}
			},
			'loggers': {
				'fyers_socket': {
					'handlers': ['file'],
					'level': 'DEBUG',
					'propagate': False,
				}
			},
		}
        dictConfig(LOGGING)
        self.logger = logging.getLogger('fyers_socket')

# async def main():
client_id = "XC4EOD67IM-100"
access_token=  "XC4EOD67IM-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODc0MTA0MjUsImV4cCI6MTY4NzQ4MDIwNSwibmJmIjoxNjg3NDEwNDI1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2s5YjVhclJJQTNrTWM1YmJTTEJxc1lMbXZoV1FaVHhJOVlNRTIxcXJUQklaekxXOGtTLV9tV2Q3LXZCdkRkRzJjbVdjdHR4YTBYbTRKWVR3QXdETlhWdkN6d3g4V1lhek1IY0hhcWhnX2FaMEJKMD0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.EBiR2F4nXNSBpHJioz5OLh1k_iNDuv4Kdyu66JTx-xk"

fyers= FyersSocket(access_token,False , None)
fyers.subscribe('OnOrders')