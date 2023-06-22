import asyncio
import threading
import time
import websocket
from threading import Thread
import logging
from logging.config import dictConfig
import os
import struct
import base64
from fyersApi import SessionModel, FyersModelv3
import define
import sys
import websockets 

# {'s': 'error', 'code': -300, 'message': 'Please provide a valid symbol'}
# {'s': 'error', 'code': -1600, 'message': 'Could not authenticate the user '}


class SymbolConverstion():

    def __init__(self,access_token,datatype):
        self.datatype = datatype
        self.__access_token = access_token


    def symbol_to_token(self,symbols):   
        symbols =','.join(symbols)        
        fyers = FyersModelv3(token=self.__access_token, is_async=False)
        quotesData = fyers.quotes({"symbols": symbols})
        datadict = {}
        values ={}
        index_dict = {
            "NSE:NIFTY50-INDEX": "Nifty 50",
            "NSE:NIFTYINDIAMFG-INDEX": "Nifty India Manufacturing",
            "NSE:NIFTY100ESG-INDEX": "Nifty100 ESG",
            "NSE:NIFTYINDDIGITAL-INDEX": "Nifty India Digital",
            "NSE:NIFTYMICROCAP250-INDEX": "Nifty Microcap 250",
            "NSE:NIFTYCONSRDURBL-INDEX": "Nifty Consumer Durables",
            "NSE:NIFTYHEALTHCARE-INDEX": "Nifty Healthcare",
            "NSE:NIFTYOILANDGAS-INDEX": "Nifty Oil and Gas",
            "NSE:NIFTY100ESGSECLDR-INDEX": "Nifty100 ESG Sector Leaders",
            "NSE:NIFTY200MOMENTM30-INDEX": "Nifty200 Momentum 30",
            "NSE:NIFTYALPHALOWVOL-INDEX": "Nifty Alpha Low Volatility",
            "NSE:NIFTY200QUALTY30-INDEX": "Nifty200 Quality 30",
            "NSE:NIFTYSMLCAP50-INDEX": "Nifty Smallcap 50",
            "NSE:NIFTYMIDSELECT-INDEX": "Nifty Midcap Select",
            "NSE:NIFTYMIDCAP150-INDEX": "Nifty Midcap 150",
            "NSE:NIFTY100 EQL WGT-INDEX": "Nifty100 Equal Weight",
            "NSE:NIFTY50 EQL WGT-INDEX": "Nifty50 Equal Weight",
            "NSE:NIFTYGSCOMPSITE-INDEX": "Nifty GS Composite",
            "NSE:NIFTYGS1115YR-INDEX": "Nifty GS 11-15 Year",
            "NSE:NIFTYGS48YR-INDEX": "Nifty GS 4-8 Year",
            "NSE:NIFTYGS10YRCLN-INDEX": "Nifty GS 10 Year Clean",
            "NSE:NIFTYGS813YR-INDEX": "Nifty GS 8-13 Year",
            "NSE:NIFTYSMLCAP100-INDEX": "Nifty Smallcap 100",
            "NSE:NIFTYQUALITY30-INDEX": "Nifty100 Quality 30",
            "NSE:NIFTYPVTBANK-INDEX": "Nifty Private Bank",
            "NSE:NIFTYPHARMA-INDEX": "Nifty Pharma",
            "NSE:NIFTYLARGEMID250-INDEX": "Nifty LargeMidcap 250",
            "NSE:NIFTYGS15YRPLUS-INDEX": "Nifty GS 15 Year Plus",
            "NSE:NIFTYPSUBANK-INDEX": "Nifty PSU Bank",
            "NSE:NIFTYSMLCAP250-INDEX": "Nifty Smallcap 250",
            "NSE:NIFTYENERGY-INDEX": "Nifty Energy",
            "NSE:NIFTYALPHA50-INDEX": "Nifty Alpha 50",
            "NSE:NIFTYPSE-INDEX": "Nifty PSE",
            "NSE:NIFTYFINSRV2550-INDEX": "Nifty Financial Services 25/50",
            "NSE:FINNIFTY-INDEX": "Nifty Fin Service",
            "NSE:NIFTYREALTY-INDEX": "Nifty Realty",
            "NSE:NIFTY500-INDEX": "Nifty 500",
            "NSE:NIFTY500MULTICAP-INDEX": "Nifty500 Multicap",
            "NSE:NIFTYMIDCAP50-INDEX": "Nifty Midcap 50",
            "NSE:NIFTYTOTALMKT-INDEX": "Nifty Total Market",
            "NSE:NIFTY50PR2XLEV-INDEX": "Nifty50 PR 2x Leverage",
            "NSE:INDIAVIX-INDEX": "India VIX",
            "NSE:NIFTYDIVOPPS50-INDEX": "Nifty Dividend Opportunities 50",
            "NSE:NIFTYMNC-INDEX": "Nifty MNC",
            "NSE:NIFTY50VALUE20-INDEX": "Nifty50 Value 20",
            "NSE:NIFTY50-INDEX": "Nifty 50",
            "NSE:HANGSENG BEES-NAV-INDEX": "Hang Seng BeES",
            "NSE:NIFTY100LIQ15-INDEX": "Nifty100 Liquid 15",
            "NSE:NIFTY50TR2XLEV-INDEX": "Nifty50 TR 2x Leverage",
            "NSE:NIFTY100-INDEX": "Nifty 100",
            "NSE:NIFTY100 LOWVOL30-INDEX": "Nifty100 Low Volatility 30",
            "NSE:NIFTYBANK-INDEX": "Nifty Bank",
            "NSE:NIFTYFMCG-INDEX": "Nifty FMCG",
            "NSE:NIFTYIT-INDEX": "Nifty IT",
            "NSE:NIFTYGS10YR-INDEX": "Nifty GS 10 Year",
            "NSE:NIFTYMIDCAP100-INDEX": "Nifty Midcap 100",
            "NSE:NIFTYNEXT50-INDEX": "Nifty Next 50",
            "NSE:NIFTYM150QLTY50-INDEX": "Nifty MidSmallcap 400",
            "NSE:NIFTYSERVSECTOR-INDEX": "Nifty Services Sector",
            "NSE:NIFTYMIDSML400-INDEX": "Nifty Midcap Smallcap 400",
            "NSE:NIFTYAUTO-INDEX": "Nifty Auto",
            "NSE:NIFTYMETAL-INDEX": "Nifty Metal",
            "NSE:NIFTYINFRA-INDEX": "Nifty Infrastructure",
            "NSE:NIFTYMEDIA-INDEX": "Nifty Media",
            "NSE:NIFTY50PR1XINV-INDEX": "Nifty50 PR 1x Inverse",
            "NSE:NIFTY200-INDEX": "Nifty 200",
            "NSE:NIFTY50TR1XINV-INDEX": "Nifty50 TR 1x Inverse",
            "NSE:NIFTYCPSE-INDEX": "Nifty CPSE",
            "NSE:NIFTYMIDLIQ15-INDEX": "Nifty Midcap Liquid 15",
            "NSE:NIFTYCOMMODITIES-INDEX": "Nifty Commodities",
            "NSE:NIFTYCONSUMPTION-INDEX": "Nifty Consumption",
            "NSE:NIFTY50DIVPOINT-INDEX": "Nifty50 Dividend Points",
            "NSE:NIFTYGROWSECT15-INDEX": "Nifty Growth Sector 15",
            "BSE:100LARGECAPTMC-INDEX": "LCTMCI",
            "BSE:DFRG-INDEX": "DFRGRI",
            "BSE:QUALITY-INDEX": "BSEQUI",
            "BSE:DIVIDENDSTABILITY-INDEX": "BSEDSI",
            "BSE:250SMALLCAP-INDEX": "SML250",
            "BSE:150MIDCAP-INDEX": "MID150",
            "BSE:ESG100-INDEX": "ESG100",
            "BSE:SNXT50-INDEX": "SNXT50",
            "BSE:SNSX50-INDEX": "SNSX50",
            "BSE:UTILS-INDEX": "UTILS",
            "BSE:GREENEX-INDEX": "GREENX",
            "BSE:SENSEX-INDEX": "SENSEX",
            "BSE:REALTY-INDEX": "REALTY",
            "BSE:PRIVATEBANKS-INDEX": "BSEPBI",
            "BSE:CDGS-INDEX": "CDGS",
            "BSE:OILGAS-INDEX": "OILGAS",
            "BSE:ENERGY-INDEX": "ENERGY",
            "BSE:POWER-INDEX": "POWER",
            "BSE:500-INDEX": "BSE500",
            "BSE:100-INDEX": "BSE100",
            "BSE:PSU-INDEX": "BSEPSU",
            "BSE:HC-INDEX": "BSE HC",
            "BSE:400MIDSMALLCAP-INDEX": "MSL400",
            "BSE:BHRT22-INDEX": "BHRT22",
            "BSE:BANKEX-INDEX": "BANKEX",
            "BSE:ALLCAP-INDEX": "ALLCAP",
            "BSE:INFRA-INDEX": "INFRA",
            "BSE:CD-INDEX": "BSE CD",
            "BSE:MIDCAP-INDEX": "MIDCAP",
            "BSE:AUTO-INDEX": "AUTO",
            "BSE:BASMTR-INDEX": "BASMTR",
            "BSE:200-INDEX": "BSE200",
            "BSE:FIN-INDEX": "FIN",
            "BSE:CG-INDEX": "BSE CG",
            "BSE:ENHANCEDVALUE-INDEX": "BSEEVI",
            "BSE:TECK-INDEX": "TECK",
            "BSE:METAL-INDEX": "METAL",
            "BSE:CARBONEX-INDEX": "CARBON",
            "BSE:MIDSEL-INDEX": "MIDSEL",
            "BSE:SME IPO-INDEX": "SMEIPO",
            "BSE:MOMENTUM-INDEX": "BSEMOI",
            "BSE:TELCOM-INDEX": "TELCOM",
            "BSE:CPSE-INDEX": "CPSE",
            "BSE:250LARGEMIDCAP-INDEX": "LMI250",
            "BSE:SMLCAP-INDEX": "SMLCAP",
            "BSE:IT-INDEX": "BSE IT",
            "BSE:INDIAMANUFACTURING-INDEX": "MFG",
            "BSE:INDSTR-INDEX": "INDSTR",
            "BSE:LOWVOLATILITY-INDEX": "BSELVI",
            "BSE:LRGCAP-INDEX": "LRGCAP",
            "BSE:IPO-INDEX": "BSEIPO",
            "BSE:FMC-INDEX": "BSEFMC",
            "BSE:SMLSEL-INDEX": "SMLSEL"
        }
        mapping = {"1010":'nse_cm' ,"1011": 'nse_fo', "1120" : 'mcx_fo' , "1210" :'bse_cm', "1012" : 'cde_fo'}
        # print(quotesData)
        wrong_symbol =[]
        if 'd' in quotesData:
            for data in quotesData['d']:
                # print(data)
                if data['s'] == 'ok':
                    # datadict[data['n']] = {}
                    values = {}
                    # values['exch'] = data['v']['exchange']
                    values['fyToken'] = data['v']['fyToken']
                    values['symbol'] = data['v']['symbol']
                    key = values['fyToken'][:4]
                    values['segment'] = mapping[key]
                    data = values['symbol'].split('-')
                    # print(data)

                    if len(data) > 1 and data[-1] == "INDEX":
                        if values['symbol'] in index_dict:
                            values['exToken'] = index_dict[values['symbol']]
                        else:
                            values['exToken'] = values['symbol'].split(':')[1].split('-')[0]
                        values['subSymbol'] = 'if'+ '|'+values['segment'] + '|'+values['exToken']
                    elif self.datatype == 'depthUpdate':
                        values['exToken'] = values['fyToken'][10:]
                        values['subSymbol'] = 'dp'+ '|'+values['segment'] + '|'+values['exToken']

                    else :
                        values['exToken'] = values['fyToken'][10:]
                        values['subSymbol'] = 'sf'+ '|'+values['segment'] + '|'+values['exToken']
                    datadict[values['subSymbol']] = values['symbol']
                elif data['s'] == 'error':
                    wrong_symbol.append(data['n'])

            return [wrong_symbol , datadict]
        else:
            return [quotesData,{}]
        




class FyersHsmSocket():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self,access_token, log_path = None , litemode = False ):
        self.__url = "wss://socket.fydev.tech/hsm/v1-5/dev"
        self.__access_token = access_token 
        self.log_path = log_path
        self.Source = "PythonSDK-1.0.0"
        self.channelNum = None
        self.channels = []
        self.running_channels = set()
        self.datatype = None
        self.ackCount = None
        self.updateCount = 0
        self.OnMessage = None
        self.OnError = None
        self.OnOpen =  None
        self.onPing = None
        self.websocket = None
        self.sleep = 0
        self.__ws_run = None
        self.run_background = False
        self.background_flag= False
        self.output = {}
        self.literesp = {}
        self.channel_symbol = []
        self.symbol_token = {}
        self.scrips_count = {}
        self.scrips_per_channel = {}
        self.start = False
        self.websocket_lock = threading.Lock()
        self.unsub_symbol = []
        for i in range(1, 31):
            self.scrips_per_channel[i] = []
        self.active_channel = None
        self.logger_setup()
        self.logger.info("Initiate socket object")
        self.logger.debug('access_token ' + self.__access_token)
        self.message = []
        self.error_flag = False
        self.resp = {}
        self.symDict = {}
        self.__ws_object = None
        self.dp_sym = {}
        self.index_sym = {}
        self.scrips_sym = {}
        self.ErrResponse = {"code":-99,"message":"","s":"error"}
        self.SuccesResponse = {"code":200,"message":"","s":"Ok"}
        self.ack_bool = False
        self.dataVal = ["ltp","vol_traded_today" , "last_traded_time" , "ExFeedTime" , "bidSize" , 
                        "askSize" , "bidPrice" , "askPrice" , "last_traded_qty" , "tot_buy_qty" , 
                        "tot_sell_qty" ,"avg_trade_price","OI","low_price","high_price" ,"Yhigh",
                          "Ylow", "lowCircuit" , "upCircuit" ,"open_price", "close_price",'symbol']
        
        self.indexVal = ['ltp', 'close_price', 'ExFeedTime', 'high_price', 'low_price', 'open_price', 'symbol']

        self.litename = ["ltp","vol_traded_today" , "last_traded_time", 'symbol' ]
        
        self.depthvalue = ["bidPrice1","bidPrice2","bidPrice3","bidPrice4","bidPrice5",
                        "askPrice1", "askPrice2", "askPrice3", "askPrice4", "askPrice5", 
                        "bidsize1","bidsize2","bidsize3","bidsize4","bidsize5",
                        "askSize1","askSize2","askSize3","askSize4","askSize5",
                        "bidorder1","bidorder2","bidorder3","bidorder4","bidorder5",
                        "askorder1","askorder2","askorder3","askorder4","askorder5",'symbol']



    def __token_to_byte(self):
        try:
            buffer_size = 18 + len(self.__access_token) + len(self.Source)
            byte_buffer = bytearray(buffer_size)
            data_len = buffer_size - 2  
            struct.pack_into("!H", byte_buffer, 0, data_len)
            # ReqType
            byte_buffer[2] = 1 
            # FieldCount
            byte_buffer[3] = 4  
            # Field-1: AuthToken
            field1_id = 1
            field1_size = len(self.__access_token)
            struct.pack_into("!B", byte_buffer, 4, field1_id)
            struct.pack_into("!H", byte_buffer, 5, field1_size)
            struct.pack_into(f"!{field1_size}s", byte_buffer, 7, self.__access_token.encode())

            # Field-2
            field2_id = 2
            field2_size = 1
            struct.pack_into("!B", byte_buffer, 7+field1_size, field2_id)
            struct.pack_into("!H", byte_buffer, 8+field1_size, field2_size)
            byte_buffer[10+field1_size] = 78

            # Field-3
            field3_id = 3
            field3_size = 1
            struct.pack_into("!B", byte_buffer, 11+field1_size, field3_id)
            struct.pack_into("!H", byte_buffer, 12+field1_size, field3_size)
            byte_buffer[14+field1_size] = 1

            # Field-4: self.Source
            field4_id = 4
            field4_size = len(self.Source)
            struct.pack_into("!B", byte_buffer, 15+field1_size, field4_id)
            struct.pack_into("!H", byte_buffer, 16+field1_size, field4_size)
            struct.pack_into(f"!{field4_size}s", byte_buffer, 18+field1_size, self.Source.encode())

            return byte_buffer
        
        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Token message function')



    def __lite_mode_msg(self):
        try:
            self.channels = [self.channelNum]
            data = bytearray()

            data.extend(struct.pack('>H', 0))

            data.extend(struct.pack('B', 12))

            data.extend(struct.pack('B', 2))

            channel_bits = 0
            for channel_num in self.channels:
                if channel_num < 64 and channel_num > 0:
                    channel_bits |= 1 << channel_num
            # Field-1
            field_1 = bytearray()
            field_1.extend(struct.pack('B', 1))   
            field_1.extend(struct.pack('>H', 8))    
            field_1.extend(struct.pack('>Q', channel_bits))  
            data.extend(field_1)
            
            # Field-2
            field_2 = bytearray()
            field_2.extend(struct.pack('B', 2))    
            field_2.extend(struct.pack('>H', 1))    
            field_2.extend(struct.pack('B', 76))   
            data.extend(field_2)

            data_length = len(data) - 2
            data[0] = (data_length >> 8) & 0xFF
            data[1] = data_length & 0xFF

            return data    
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Lite mode message function')
        
        
    def __full_mode_msg(self):
        try:
            print('------full mode ---msg -----')
            self.channels = [self.channelNum]
            data = bytearray()

            data.extend(struct.pack('>H', 0))

            data.extend(struct.pack('B', 12))

            data.extend(struct.pack('B', 2))

            channel_bits = 0
            for channel_num in self.channels:
                if channel_num < 64 and channel_num > 0:
                    channel_bits |= 1 << channel_num
            # Field-1
            field_1 = bytearray()
            field_1.extend(struct.pack('B', 1))   
            field_1.extend(struct.pack('>H', 8))    
            field_1.extend(struct.pack('>Q', channel_bits))  
            data.extend(field_1)
            
            # Field-2
            field_2 = bytearray()
            field_2.extend(struct.pack('B', 2))    
            field_2.extend(struct.pack('>H', 1))    
            field_2.extend(struct.pack('B', 70))   
            data.extend(field_2)

            data_length = len(data) - 2
            data[0] = (data_length >> 8) & 0xFF
            data[1] = data_length & 0xFF

            return data    
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Full mode message function')
        
        
    def __subscription_msg(self,symbols):
        try:
            self.scrips_per_channel[self.channelNum] += symbols
            self.scrips = symbols
            self.scripsData = bytearray()
            self.scripsData.append(len(self.scrips) >> 8 & 0xFF)
            self.scripsData.append(len(self.scrips) & 0xFF)
            for scrip in self.scrips:
                scripBytes = str(scrip).encode("ascii")
                self.scripsData.append(len(scripBytes))
                self.scripsData.extend(scripBytes)

            dataLen = 18 + len(self.scripsData) + len(self.__access_token) + len(self.Source)
            reqType = 4
            fieldCount = 2
            buffer_msg = bytearray()
            buffer_msg.extend(struct.pack(">H", dataLen))
            buffer_msg.append(reqType)
            buffer_msg.append(fieldCount)

            # Field-1
            buffer_msg.append(1)
            buffer_msg.extend(struct.pack(">H", len(self.scripsData)))
            buffer_msg.extend(self.scripsData)

            # Field-2
            buffer_msg.append(2) 
            buffer_msg.extend(struct.pack(">H", 1))
            buffer_msg.append(self.channelNum)

            return buffer_msg
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Subscription message function')
        
        

    def __unsubscription_msg(self,scrips):
        try:
            scripsData = bytearray()
            scripsData.append(len(scrips) >> 8 & 0xFF)
            scripsData.append(len(scrips) & 0xFF)
            for scrip in scrips:
                scripBytes = str(scrip).encode("ascii")
                scripsData.append(len(scripBytes))
                scripsData.extend(scripBytes)

            dataLen = 18 + len(scripsData) + len(self.__access_token) + len(self.Source)
            reqType = 5
            fieldCount = 2
            buffer_msg = bytearray()
            buffer_msg.extend(struct.pack(">H", dataLen))
            buffer_msg.append(reqType)
            buffer_msg.append(fieldCount)

            # Field-1
            buffer_msg.append(1) 
            buffer_msg.extend(struct.pack(">H", len(scripsData)))
            buffer_msg.extend(scripsData)

            # Field-2
            buffer_msg.append(2) 
            buffer_msg.extend(struct.pack(">H", 1))
            buffer_msg.append(self.channelNum)

            return buffer_msg
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Unsubscription message function')
        
       
    def __channel_resume_msg(self,channel):
        try:

            self.channels = [channel]

            data = bytearray()

            data.extend(struct.pack('>H', 0))

            data.extend(struct.pack('B', 8))

            data.extend(struct.pack('B', 1))

            channel_bits = 0
            for channel_num in self.channels:
                if channel_num < 64 and channel_num > 0:
                    channel_bits |= 1 << channel_num
            # Field-1
            field_1 = bytearray()
            field_1.extend(struct.pack('B', 1))   
            field_1.extend(struct.pack('>H', 8))    
            field_1.extend(struct.pack('>Q', channel_bits))  
            data.extend(field_1)

            data_length = len(data) - 2
            data[0] = (data_length >> 8) & 0xFF
            data[1] = data_length & 0xFF

            return data
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Channel Resume Message function')

    def __channel_pause_msg(self,channel):
        try:
            self.channels = [channel]

            data = bytearray()

            data.extend(struct.pack('>H', 0))

            data.extend(struct.pack('B', 7))

            data.extend(struct.pack('B', 1))

            channel_bits = 0
            for channel_num in self.channels:
                if channel_num < 64 and channel_num > 0:
                    channel_bits |= 1 << channel_num
            # Field-1
            field_1 = bytearray()
            field_1.extend(struct.pack('B', 1))   
            field_1.extend(struct.pack('>H', 8))    
            field_1.extend(struct.pack('>Q', channel_bits))  
            data.extend(field_1)

            data_length = len(data) - 2
            data[0] = (data_length >> 8) & 0xFF
            data[1] = data_length & 0xFF

            return data
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Channel Pause Message function')
 
        

    def __ackowledgement_msg(self, messae_number):
        try:
            total_size = 11
            req_type = 3
            field_count = 1
            field_id = 1
            field_size = 4
            field_value = messae_number
            buffer_msg = bytearray()
            # Pack the data into the byte array
            buffer_msg.extend(struct.pack('>H', total_size - 2))
            buffer_msg.extend(struct.pack('B', req_type))
            buffer_msg.extend(struct.pack('B', field_count))
            buffer_msg.extend(struct.pack('B', field_id))
            buffer_msg.extend(struct.pack('>H', field_size))
            buffer_msg.extend(struct.pack('>I', field_value))
            return buffer_msg
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Ackowledgement message function')
        
        

    def __auth_resp(self,data):
        try:
            offset = 4
            field_id = struct.unpack('!B', data[offset:offset+1])[0]
            offset += 1
            field_length = struct.unpack('!H', data[offset:offset+2])[0]
            offset += 2
            string_val = data[offset:offset+field_length].decode('utf-8')
            offset += field_length

            if string_val == "K":
                
                self.On_message({ 
                                    "code" : define.success_code,
                                    "message" : define.auth_success,
                                    "s" : define.success
                                })
            else:
                self.On_error({ 
                                    "code" : define.auth_error_code,
                                    "message" : define.auth_fail,
                                    "s" : define.Error
                                })

            field_id = struct.unpack('!B', data[offset:offset+1])[0]
            offset += 1
            field_length = struct.unpack('!H', data[offset:offset+2])[0]
            offset += 2
            self.ack_count = struct.unpack('>I', data[offset:offset+4])[0]
            offset += 4
            json_obj = data[offset:].decode()
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Authentication Response function')

    def __subscribe_resp(self,data):
        try:

            offset = 3
            field_count = struct.unpack('B', data[offset:offset+1])[0]
            offset += 1
            field_id = struct.unpack('B', data[offset:offset+1])[0]
            offset += 1
            field_length = struct.unpack('H', data[offset:offset+2])[0]
            offset += 2
            print(offset)
            string_val = data[offset:offset+1].decode('latin-1')
            offset += field_length
            if string_val == "K":
                
                self.On_message({ 
                                    "code" : define.success_code,
                                    "message" : define.subscribe_success,
                                    "s" : define.success
                                })
            else:
                self.On_error({ 
                                    "code" : define.subs_error_code,
                                    "message" : define.subscribe_fail,
                                    "s" : define.Error
                                })


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Unsubsciption Response function')


    def __unsubscribe_resp(self,data):
        try:

            offset = 3
            field_count = struct.unpack('B', data[offset:offset+1])[0]
            offset += 1
            field_id = struct.unpack('B', data[offset:offset+1])[0]
            offset += 1
            field_length = struct.unpack('H', data[offset:offset+2])[0]
            offset += 2
            print(offset)
            string_val = data[offset:offset+1].decode('latin-1')
            offset += field_length
            if string_val == "K":
                
                self.On_message({ 
                                    "code" : define.success_code,
                                    "message" : define.unsubscribe_success,
                                    "s" : define.success
                                })
            else:
                self.On_error({ 
                                    "code" : define.unsubs_error_code,
                                    "message" : define.unsubscribe_fail,
                                    "s" : define.Error
                                })

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Unsubsciption Response function')

                       
    def __lite_full_mode_resp(self, data):
        try:
            offset = 3

            # Unpack the field count
            field_count = struct.unpack('!B', data[offset:offset + 1])[0]
            offset += 1

            if field_count >= 1:
                # Unpack the field ID
                field_id = struct.unpack('!B', data[offset:offset + 1])[0]
                offset += 1

                # Unpack the field length
                field_length = struct.unpack('!H', data[offset:offset + 2])[0]
                offset += 2

                # Extract the string value and decode it
                string_val = data[offset:offset + field_length].decode('utf-8')
                offset += field_length

                print('----------in response full mode----------')
                if string_val == "K":
                    if self.lite:
                        self.On_message({ 
                                            "code" : define.success_code,
                                            "message" : define.lite_mode,
                                            "s" : define.success
                                        })                    
                    else:
                        self.On_message({ 
                                            "code" : define.success_code,
                                            "message" : define.full_mode,
                                            "s" : define.success
                                        })
                else:
                    self.On_error({ 
                                        "code" : define.mode_error_code,
                                        "message" : define.mode_change_error,
                                        "s" : define.Error
                                    })

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Lite and Full mode Response function')




    def __response_output(self,data, datatype):

        try:
            dataResp = data
            response = {}
            if 'bidPrice1' not in dataResp and 'vol_traded_today' in dataResp and self.lite:
                # print(dataResp)
                for i , val in enumerate(self.litename):
                    if val in dataResp and val == 'ltp':
                        response[val] = dataResp[val] / (10 ** dataResp['precision']) 
                    else:
                        response[val] = dataResp[val]
            else:
                if datatype == 'depth':

                    for i , val in enumerate(self.depthvalue):
                        if val in dataResp and i < 10:
                            response[val] = dataResp[val] / (10 ** dataResp['precision']) 
                        else:
                            response[val] = dataResp[val]
                elif datatype == 'scrips':
                    for i , val in enumerate(self.dataVal):
                        if val in dataResp and i in [0,6,7,11,13,14,17,18,19,20]:
                            response[val] = dataResp[val] / (10 ** dataResp['precision']) 
                        else:
                            response[val] = dataResp[val]

                    if 'OI' in response:
                        response.pop('OI')
                    if 'Yhigh' in response:
                        response.pop('Yhigh')
                    if 'Ylow' in response:
                        response.pop('Ylow')
                else:
                    for i , val in enumerate(self.indexVal):
                        if val in dataResp and i in [0,1,3,4,5]:
                            response[val] = dataResp[val] / (10 ** dataResp['precision']) 
                        else:
                            response[val] = dataResp[val]
                

            self.On_message(response)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("ERR : -> Line:{} Exception:{} Function:''".format(exc_tb.tb_lineno, str(e)),'Response Output')




    def __datafeed_resp(self,data):
        try:
            updateCount = 0
            if self.ack_count > 0:
                updateCount += 1
                msgNum = struct.unpack('>I', data[3:7])[0]
                if updateCount == self.ack_count:
                    self.ack_bool = True
                    self.ack_msg = self.__ackowledgement_msg(msgNum)
                    updateCount = 0
            scripCount = struct.unpack('!H', data[7:9])[0]
            offset = 9

            for _ in range(scripCount):
                dataType = struct.unpack('B', data[offset:offset+1])[0]
                if dataType == 83: #Snapshot datafeed
                    self.output = {} 
                    offset += 1
                    topicId = struct.unpack('H', data[offset:offset+2])[0]
                    offset += 2
                    topicNameLength = struct.unpack('B', data[offset:offset+1])[0]
                    offset += 1

                    topicName = data[offset:offset+topicNameLength].decode('utf-8')
                    offset += topicNameLength

                    # Maintaining dict - topicId : topicName
                    # self.symDict[topicId] = topicName
                    if topicName[:2] == 'dp':
                        self.dp_sym[topicId] = topicName
                        self.resp[self.dp_sym[topicId]] = {}

                        fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                        offset += 1

                        for index in range(fieldCount):
                            value = struct.unpack('>I', data[offset:offset+4])[0]
                            offset += 4
                            self.resp[self.dp_sym[topicId]][self.depthvalue[index]] = value 

                        stringFieldLength = struct.unpack('H', data[offset:offset+2])[0]
                        offset += 2

                        multiplier = struct.unpack('H', data[offset:offset+2])[0]
                        self.resp[self.dp_sym[topicId]]["multiplier"] = multiplier
                        offset += 2

                        precision = struct.unpack('B', data[offset:offset+1])[0]
                        self.resp[self.dp_sym[topicId]]["precision"] = precision
                        offset += 1

                        val = ["exchange", "exchange_token", "symbol"]
                        for i in range(3):
                            stringLength = struct.unpack('B', data[offset:offset+1])[0]
                            offset += 1
                            stringData = data[offset:offset+stringLength].decode('utf-8')
                            self.resp[self.dp_sym[topicId]][val[i]] = stringData
                            offset += stringLength
                        self.resp[topicName]['symbol'] = self.symbol_token[topicName]
                        self.__response_output(self.resp[self.dp_sym[topicId]],'depth')




                    elif topicName[:2] == 'if':

                        self.index_sym[topicId] = topicName
                        self.resp[self.index_sym[topicId]] = {}

                         # fieldCount - 21 in scrips , 25 in depth , 6 in index
                        fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                        offset += 1

                        for index in range(fieldCount):
                            value = struct.unpack('>I', data[offset:offset+4])[0]
                            offset += 4

                            self.resp[self.index_sym[topicId]][self.indexVal[index]] = value


                        stringFieldLength = struct.unpack('H', data[offset:offset+2])[0]
                        offset += 2

                        multiplier = struct.unpack('H', data[offset:offset+2])[0]
                        self.resp[self.index_sym[topicId]]["multiplier"] = multiplier
                        offset += 2

                        precision = struct.unpack('B', data[offset:offset+1])[0]
                        self.resp[self.index_sym[topicId]]["precision"] = precision
                        offset += 1

                        val = ["exchange", "exchange_token", "symbol"]
                        for i in range(3):
                            stringLength = struct.unpack('B', data[offset:offset+1])[0]
                            offset += 1
                            stringData = data[offset:offset+stringLength].decode('utf-8')
                            self.resp[self.index_sym[topicId]][val[i]] = stringData
                            offset += stringLength
                        # print('\n',self.symbol_token, '\n')
                        self.resp[topicName]['symbol'] = self.symbol_token[topicName]

                        self.__response_output(self.resp[self.index_sym[topicId]],'index')




                    elif topicName[:2] == 'sf':
                        self.scrips_sym[topicId] = topicName
                        self.resp[self.scrips_sym[topicId]] = {}

                        # fieldCount - 21 in scrips , 25 in depth , 6 in index
                        fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                        offset += 1

                        for index in range(fieldCount):
                            value = struct.unpack('>I', data[offset:offset+4])[0]
                            offset += 4
                            self.resp[self.scrips_sym[topicId]][self.dataVal[index]] = value

                        stringFieldLength = struct.unpack('H', data[offset:offset+2])[0]
                        offset += 2

                        multiplier = struct.unpack('H', data[offset:offset+2])[0]
                        self.resp[self.scrips_sym[topicId]]["multiplier"] = multiplier
                        offset += 2

                        precision = struct.unpack('B', data[offset:offset+1])[0]
                        self.resp[self.scrips_sym[topicId]]["precision"] = precision
                        offset += 1
                        val = ["exchange", "exchange_token", "symbol"]
                        for i in range(3):
                            stringLength = struct.unpack('B', data[offset:offset+1])[0]
                            offset += 1
                            stringData = data[offset:offset+stringLength].decode('utf-8')
                            self.resp[self.scrips_sym[topicId]][val[i]] = stringData
                            offset += stringLength
                        self.resp[topicName]['symbol'] = self.symbol_token[topicName]

                        self.__response_output(self.resp[self.scrips_sym[topicId]],'scrips')
                    
                elif dataType == 85: #Full mode datafeed
                    offset += 1
                    topicId = struct.unpack('H', data[offset:offset+2])[0]
                    offset += 2

                    fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                    offset += 1
                    sf_flag , idx_flag , dp_flag = False, False,False

                    for index in range(fieldCount):
                        value = struct.unpack('>I', data[offset:offset+4])[0]
                        offset += 4
                        if fieldCount == 21:
                            self.resp[self.scrips_sym[topicId]][self.dataVal[index]] = value
                            sf_flag = True
                        elif fieldCount == 6:
                            self.resp[self.index_sym[topicId]][self.indexVal[index]] = value
                            idx_flag = True
                        else:
                            self.resp[self.dp_sym[topicId]][self.depthvalue[index]] = value
                            dp_flag = True

                    if sf_flag:
                        self.__response_output(self.resp[self.scrips_sym[topicId]],'scrips')
                    elif idx_flag:

                        self.__response_output(self.resp[self.index_sym[topicId]],'index')
                    elif dp_flag:
                        self.__response_output(self.resp[self.dp_sym[topicId]],'depth')

                    
                elif dataType == 76: #lite mode datafeed

                    offset += 1
                    topicId = struct.unpack('H', data[offset:offset+2])[0]
                    offset += 2
                    sf_flag , idx_flag  = False, False
                    if topicId in self.scrips_sym:

                        for index in range(3):
                            value = struct.unpack('>I', data[offset:offset+4])[0]
                            offset += 4
                            self.resp[self.scrips_sym[topicId]][self.dataVal[index]] = value
                            sf_flag = True

                    elif topicId in self.index_sym:
                            value = struct.unpack('>I', data[offset:offset+4])[0]
                            offset += 4
                            self.resp[self.index_sym[topicId]][self.indexVal[index]] = value
                    else:
                        print(topicId,self.scrips_sym , self.index_sym )

                    if sf_flag:
                        self.__response_output(self.resp[self.scrips_sym[topicId]],'scrips')
                        # print("scrips  ", self.resp[self.scrips_sym[topicId]])
                    elif idx_flag:
                        # self.__response_output(self.resp[self.index_sym[topicId]],'index')
                        print("index  ",self.resp[self.index_sym[topicId]])
                    else:
                        print(topicId,self.scrips_sym , self.index_sym )
                else:
                    pass                    
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("payload_creation :: ERR : -> Line:{} Exception:{} Function:{}".format(exc_tb.tb_lineno, str(e), 'Datafeed response'))
            self.ErrResponse['message'] = "Error While Unpacking datafeed"
            self.On_error(self.ErrResponse)



    def __resume_pause_response_resp(self, data,channeltype):
        try:
            offset = 3
            # Unpack the field count
            field_count = struct.unpack('!B', data[offset:offset + 1])[0]
            offset += 1

            # Unpack the field ID
            field_id = struct.unpack('!B', data[offset:offset + 1])[0]
            offset += 1

            # Unpack the field length
            field_length = struct.unpack('!H', data[offset:offset + 2])[0]
            offset += 2

            # Extract the string value and decode it
            string_val = data[offset:offset + field_length].decode('utf-8')
            offset += field_length
            print(string_val)

            if string_val == "K":
                if channeltype == 7:
                    self.On_message({ 
                                        "code" : define.success_code,
                                        "message" : define.channel_paused,
                                        "s" : define.success
                                    })                    
                else:
                    self.On_message({ 
                                        "code" : define.success_code,
                                        "message" : define.channel_resumed,
                                        "s" : define.success
                                    })
            else:
                self.On_error({ 
                                    "code" : define.mode_error_code,
                                    "message" : define.channel_change_fail,
                                    "s" : define.Error
                                })

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("payload_creation :: ERR : -> Line:{} Exception:{}".format(exc_tb.tb_lineno, str(e)))




    def __response_msg(self , data):


        datasize, respType = struct.unpack('!HB', data[:3])
        if respType == 1: # Authentication response
            self.__auth_resp(data)

        elif respType == 4: # subsciption response
            self.__subscribe_resp(data)

        elif respType == 5: # Unsubsciption response
            self.__unsubscribe_resp(data)

        elif respType == 12: # Full Mode Data Response
            self.__lite_full_mode_resp(data)

        elif respType == 6: # Data Feed Response
            self.__datafeed_resp(data)
        
        elif respType == 5:
            self.__unsubscribe_resp()

        elif respType == 7 or respType == 8:
            self.__resume_pause_response_resp(data , respType)


    def __check_auth_and_symbol(self):
        symbols = []
        flag = False
        symbol_dict = {}
        total_symbols = len(self.symbols)
        symbol_chunks = [self.symbols[i:i+50] for i in range(0, total_symbols, 50)]
        conv = SymbolConverstion(self.__access_token, self.datatype)
        for symbols in symbol_chunks:
            symbol_value = conv.symbol_to_token(symbols)
            symbol_dict = dict(symbol_dict | symbol_value[1])
            if type(symbol_value[0]) == list and len(symbol_value[0]) > 0:

                symbols += symbol_value[0]
                flag = True
        if flag:
            self.On_error({ 
                    "code" : define.invalid_code,
                    "message" : define.invalid_symbols,
                    "s" : define.Error
                })

        return symbol_dict

    def __channel_resume_pause(self):

        if self.__ws_object is not None and self.active_channel is not None and self.active_channel != self.channelNum:
            message = self.__channel_pause_msg(self.active_channel)
            self.message.append(message)
            if self.channelNum in self.running_channels:
                message = self.__channel_resume_msg(self.channelNum)
                self.message.append(message)
        self.running_channels.add(self.channelNum)
        self.active_channel = self.channelNum


    def On_message(self,message):
        if self.OnMessage is not None:
            self.OnMessage(message)
        else:
            print('')
            print(f"Response : {message}") 

    def __send_message(self,message):
        try:
            with self.websocket_lock:
                print('-------msg sent--------')
                self.__ws_object.send(message, websocket.ABNF.OPCODE_BINARY)
        except KeyboardInterrupt:
            pass

        # except Exception as e:
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     self.logger.error("payload_creation :: ERR : -> Line:{} Exception:{}".format(exc_tb.tb_lineno, str(e)))


    def __process_message_queue(self):
        while True:
            if self.message:
                message = self.message.pop(0)
                self.__send_message(message)
            else:
                pass

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
                thread = threading.Thread(target=self.__process_message_queue).start()
                thread = threading.Thread(target=self.ping).start()
                message = self.__token_to_byte()
                self.message.append(message)
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

                ws = websocket.WebSocketApp(
                    self.__url,
                    on_message=lambda ws, msg: self.__response_msg(msg),
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

    def unsubscribe(self, symbols, dataType=None, channel=1):
        try:

            self.__channel_resume_pause()

            self.datatype = dataType
            self.symbols = symbols
            self.channelNum = channel
            self.channel_symbol = self.__check_auth_and_symbol()
            self.unsub_symbol = list(self.channel_symbol.keys())
            for symb in self.unsub_symbol:
                if symb in self.scrips_count[self.channelNum]:
                    self.scrips_count[self.channelNum].remove(symb)
                else:
                    self.unsub_symbol.remove(symb)

            total_symbols = len(self.unsub_symbol)
            symbol_chunks = [self.unsub_symbol[i:i+100] for i in range(0, total_symbols, 100)]
            for symbols in symbol_chunks:
                message = self.__unsubscription_msg(symbols)
                self.message.append(message)

        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("payload_creation :: ERR : -> Line:{} Exception:{}".format(exc_tb.tb_lineno, str(e)))
   


    def subscribe(self, symbols, dataType=None, channel=1 , litemode = False):
        try:
            self.init_connection()
            time.sleep(1)

            self.datatype = dataType
            self.symbols = symbols
            self.channelNum = channel
            self.lite = litemode
            self.__channel_resume_pause()
            if self.lite:
                message = self.__lite_mode_msg()
                self.message.append(message)
            else:
                message = self.__full_mode_msg()
                self.message.append(message)
            self.channel_symbol = self.__check_auth_and_symbol()
            self.symbol_token = dict(self.symbol_token | self.channel_symbol)
            self.scrips_count[self.channelNum] = list(self.channel_symbol.keys())
            total_symbols = len(self.scrips_count[self.channelNum])
            if len(self.scrips_per_channel[self.channelNum]) > 200 or total_symbols > 200:
                self.On_error({ 
                                    "code" : define.limit_exceed_code,
                                    "message" : define.limit_exceed,
                                    "s" : define.Error
                                })
                return
            symbol_chunks = [self.scrips_count[self.channelNum][i:i+100] for i in range(0, total_symbols, 100)]
            print("unsub chunk",symbol_chunks)

            for symbols in symbol_chunks:
                message = self.__subscription_msg(symbols)
                self.message.append(message)
            print('---------')

        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("payload_creation :: ERR : -> Line:{} Exception:{}".format(exc_tb.tb_lineno, str(e)))
   

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





access_token=  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODc0MTA0MjUsImV4cCI6MTY4NzQ4MDIwNSwibmJmIjoxNjg3NDEwNDI1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2s5YjVhclJJQTNrTWM1YmJTTEJxc1lMbXZoV1FaVHhJOVlNRTIxcXJUQklaekxXOGtTLV9tV2Q3LXZCdkRkRzJjbVdjdHR4YTBYbTRKWVR3QXdETlhWdkN6d3g4V1lhek1IY0hhcWhnX2FaMEJKMD0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.EBiR2F4nXNSBpHJioz5OLh1k_iNDuv4Kdyu66JTx-xk"

client = FyersHsmSocket(access_token)
client1 = FyersHsmSocket(access_token)
print(client is client1)
symbols = ['NSE:NIFTYBANK-INDEX']
symbols = ['NSE:SBIN-EQ','NSE:NIFTYBANK-INDEX',    'NSE:WIPRO-EQ',
    # 'NSE:NIFTY50-INDEX',
    # 'NSE:NIFTYBANK-INDEX',
    # 'NSE:ADANIENT-EQ',
    # 'NSE:ADANIGREEN-EQ',
    # 'NSE:AARTIIND-EQ',
    # 'NSE:ADANITRANS-EQ',
    # 'NSE:DEEPAKNTR-EQ',
    # 'NSE:IRFC-EQ',
    # 'NSE:IDEA-EQ',
    # 'NSE:TATACOMM-EQ',    'NSE:ADANIGREEN-EQ',
    # 'NSE:AARTIIND-EQ',
    # 'NSE:ADANITRANS-EQ',
    # 'NSE:DEEPAKNTR-EQ',
    # 'NSE:IRFC-EQ',
    # 'NSE:IDEA-EQ',
    # 'NSE:TATACOMM-EQ',
    # 'NSE:ZOMATO-EQ',
    # 'NSE:PNB-EQ',
    # 'NSE:BFINVEST-EQ',
    # 'NSE:RECLTD-EQ',
    # 'NSE:ZEEL-EQ',
    # 'NSE:BRITANNIA-EQ',
    # 'NSE:NIFTY50-INDEX',
    # 'NSE:NIFTYBANK-INDEX',
    # 'NSE:NIFTY100MFG-INDEX',
    # 'NSE:NIFTY100ESG-INDEX',
    # 'NSE:NIFTYDIGITAL-INDEX',
    # 'NSE:NIFTYMICRO250-INDEX',
    # 'NSE:NIFTYCONSDUR-INDEX',
    # 'NSE:NIFTYHEALTH-INDEX',
    # 'NSE:NIFTYOILGAS-INDEX',
    # 'NSE:NIFTY100ESGSECLDR-INDEX',
    # 'NSE:NIFTY200MOM30-INDEX',
    # 'NSE:NIFTYALPHALOWVOL-INDEX',
    # 'NSE:NIFTY200QLTY30-INDEX',
    # 'NSE:NIFTYSMLCAP50-INDEX',
    # 'NSE:NIFTYMIDSEL-INDEX',
    # 'NSE:NIFTYMIDCAP150-INDEX',
    # 'NSE:NIFTY100EQLWGT-INDEX',
    # 'NSE:NIFTY50EQLWGT-INDEX',
    # 'NSE:NIFTYGS200COMPOSITE-INDEX',
    # 'NSE:NIFTYGS1115YR-INDEX',
    # 'NSE:NIFTYGS48YR-INDEX',
    # 'NSE:NIFTYGS10YRCLEAN-INDEX',
    # 'NSE:NIFTYGS813YR-INDEX',
    # 'NSE:NIFTYSMLCAP100-INDEX',
    # 'NSE:NIFTY100QLTY30-INDEX',
    # 'NSE:NIFTYPVTBANK-INDEX',
    # 'NSE:NIFTYPHARMA-INDEX',
    # 'NSE:NIFTYLARGEMID250-INDEX',
    # 'NSE:NIFTYGS15YRPLUS-INDEX',
    'NSE:NIFTYPSUBANK-INDEX',]

# Subscribe to initial symbols in a separate thread
threading.Thread(client.subscribe(symbols,'SymbolUpdate',channel=1,litemode=False)).start()
symbols = ['NSE:NIFTYBANK-INDEX','NSE:FINNIFTY-INDEX',    'NSE:ADANIGREEN-EQ','NSE:ABAN-EQ', 'NSE:AMARAJABAT-EQ', 'NSE:EMAMIPAP-EQ', 'NSE:FACT-EQ', 'NSE:GODREJCP-EQ', 'NSE:SCHAEFFLER-EQ', 'NSE:ORICONENT-EQ', 'NSE:SETFNIF50-EQ', 'NSE:BALKRISHNA-EQ', 'NSE:SHYAMCENT-EQ', 'NSE:ADANITRANS-EQ', 'NSE:FEDERALBNK-EQ', 'NSE:CONFIPET-EQ', 'NSE:SYNGENE-EQ', 'NSE:KAYA-EQ', 'NSE:NGLFINE-EQ', 'NSE:AYMSYNTEX-EQ', 'NSE:PPL-EQ', 'NSE:AARON-EQ', 'NSE:RAMASTEEL-EQ', 'NSE:AURUM-EQ', 'NSE:RADHIKAJWE-EQ', 'NSE:DGCONTENT-EQ', 'NSE:CSLFINANCE-EQ', 'NSE:FINCABLES-EQ', 'NSE:JISLJALEQS-EQ', 'NSE:SHAREINDIA-EQ', 'NSE:STEELCITY-EQ', 'NSE:FINPIPE-EQ', 'NSE:MUTHOOTCAP-EQ', 'NSE:DYCL-EQ', 'NSE:AXISBNKETF-EQ', 'NSE:LUPIN-EQ', 'NSE:MCDOWELL-N-EQ', 'NSE:SATIN-EQ', 'NSE:ARVSMART-EQ', 'NSE:POWERMECH-EQ', 'NSE:RAMRAT-EQ', 'NSE:MOHEALTH-EQ', 'NSE:UTINIFTETF-EQ', 'NSE:KOTAKCONS-EQ', 'NSE:UTISENSETF-EQ', 'NSE:UFLEX-EQ', 'NSE:SHARDAMOTR-EQ', 'NSE:NAVKARCORP-EQ', 'NSE:RAMAPHO-EQ', 'NSE:NIFTYBEES-EQ', 'NSE:KRBL-EQ', 'NSE:MPSLTD-EQ', 'NSE:MARKSANS-EQ', 'NSE:TCI-EQ', 'NSE:ICICIMOM30-EQ', 'NSE:SHREEPUSHK-EQ', 'NSE:LOYALTEX-EQ', 'NSE:GUJGASLTD-EQ', 'NSE:BHARTIARTL-EQ', 'NSE:HDFCNEXT50-EQ', 'NSE:HDFCNIF100-EQ', 'NSE:ASAL-EQ', 'NSE:OLECTRA-EQ', 'NSE:PONNIERODE-EQ', 'NSE:PNB-EQ', 'NSE:KOTAKMNC-EQ', 'NSE:NIFTYQLITY-EQ', 'NSE:MOMENTUM-EQ', 'NSE:SURANAT&P-EQ', 'NSE:TIMESGTY-EQ', 'NSE:ICICIINFRA-EQ', 'NSE:INDIAMART-EQ', 'NSE:FOSECOIND-EQ', 'NSE:SPORTKING-EQ', 'NSE:OFSS-EQ', 'NSE:UNIONBANK-EQ',    'NSE:ADANIPORTS-EQ',
    'NSE:ASIANPAINT-EQ',
    'NSE:AXISBANK-EQ',
    'NSE:BAJAJ-AUTO-EQ',
    'NSE:BAJFINANCE-EQ',
    'NSE:BAJAJFINSV-EQ',
    'NSE:BHARTIARTL-EQ',
    'NSE:BPCL-EQ',
    # 'NSE:CIPLA-EQ',
    # 'NSE:COALINDIA-EQ',
    # 'NSE:DIVISLAB-EQ',
    # 'NSE:DRREDDY-EQ',
    # 'NSE:EICHERMOT-EQ',
    # 'NSE:GRASIM-EQ',
    # 'NSE:HCLTECH-EQ',
    # 'NSE:HDFC-EQ',
    # 'NSE:HDFCBANK-EQ',
    # 'NSE:HDFCLIFE-EQ',
    # 'NSE:HEROMOTOCO-EQ',
    # 'NSE:HINDALCO-EQ',
    # 'NSE:HINDUNILVR-EQ',
    # 'NSE:ICICIBANK-EQ',
    # 'NSE:INDUSINDBK-EQ',
    # 'NSE:INFY-EQ',
    # 'NSE:IOC-EQ',
    # 'NSE:ITC-EQ',
    # 'NSE:JSWSTEEL-EQ',
    # 'NSE:KOTAKBANK-EQ',
    # 'NSE:LT-EQ',
    # 'NSE:M&M-EQ',
    # 'NSE:MARUTI-EQ',
    # 'NSE:NESTLEIND-EQ',
    # 'NSE:NTPC-EQ',
    # 'NSE:ONGC-EQ',
    # 'NSE:POWERGRID-EQ',
    # 'NSE:RELIANCE-EQ',
    # 'NSE:SBI-EQ',
    # 'NSE:SBILIFE-EQ',
    # 'NSE:SHREECEM-EQ',
    # 'NSE:SUNPHARMA-EQ',
    # 'NSE:TATAMOTORS-EQ',
    # 'NSE:TATASTEEL-EQ',
    # 'NSE:TCS-EQ',
    # 'NSE:TECHM-EQ',
    # 'NSE:TITAN-EQ',
    # 'NSE:ULTRACEMCO-EQ',
    # 'NSE:UPL-EQ',

    'NSE:NIFTY100LOWVOL30-INDEX',]
# time.sleep(5)
# threading.Thread(client.subscribe(symbols,'SymbolUpdate',channel=2)).start()
# threading.Thread(client.close_connection()).start()
# symbols = [    'NSE:EICHERMOT-EQ',
#     'NSE:GRASIM-EQ',
#     'NSE:HCLTECH-EQ',
#     'NSE:HDFC-EQ',
#     'NSE:HDFCBANK-EQ',
#     'NSE:HDFCLIFE-EQ',
#     'NSE:HEROMOTOCO-EQ',
#     'NSE:HINDALCO-EQ',
#     'NSE:HINDUNILVR-EQ',
#     'NSE:ICICIBANK-EQ',
#     'NSE:INDUSINDBK-EQ',
#     'NSE:INFY-EQ',
#     'NSE:IOC-EQ',]
# time.sleep(5)

# threading.Thread(client.subscribe(symbols,'SymbolUpdate',channel=1)).start()

# # client.keep_running()


# symbol_list = [ 
#     [ "NSE:SBIN-EQ", ],

#     [   "NSE:NIFTY50-INDEX", ],
    
# ]


# global lst 
# lst = []
# def custom_message(message):
#     print(message)
#     if message[0]['symbol'] not in lst:
#         lst.append(message[0]['symbol'])
#     print(len(lst))
    
# connection_pool = []

# def connect_and_subscribe(symbols,channel):
#     data_type = "orderUpdate"
#     # access_token=  "XC4EOD67IM-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODY4MDIxMzMsImV4cCI6MTY4Njg3NTQ1MywibmJmIjoxNjg2ODAyMTMzLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2lvN1Z2cjBjdzdOSzNGNjdIZnBIT3hSM3dPbklqem9oSG5qcDlRSEhyMzBfV21vSmo4dUZYUmJHSlR5b2VpejFHZ3JISTFNUGx1SVVobGJKNGtoUUZyZGUzT0M5dy1lXy15SFQ0by1NTGhvMTNTbz0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.sI4dPJZc60deQyTrxmWj2kD8tZeeb_i8NveCiGDHRho"
#     fs = FyersHsmSocket(access_token)
#     fs.websocket_data = custom_message
#     fs.subscribe(symbols,'SymbolUpdate',channel)
#     connection_pool.append(fs)
# channel = 0
# for symbols in symbol_list:
#     print(len(symbols))
#     channel += 1
#     thread = threading.Thread(target=connect_and_subscribe, args=(symbols,channel))
#     thread.start()

# for thread in threading.enumerate():
#     if thread != threading.current_thread():
#         thread.join()