import asyncio
import logging
from logging.config import dictConfig
import os
import struct
import base64
# import SymbolConverstion
from fyerstest.fyersApi import SessionModel, FyersModelv3

import sys
import websockets 

class SymbolConverstion():
    def __init__(self,symbols,datatype):
        self.symbols = symbols
        self.datatype = datatype

    def symbol_to_token(self):
        # if len(symbols) > 50:

        symbols =','.join(self.symbols)
        print(symbols)
        client_id = ""
        access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODU1OTE2MTQsImV4cCI6MTY4NTY2NTgzNCwibmJmIjoxNjg1NTkxNjE0LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2VCWS0wRFoyQmxtUkdOWTZkXzRaTEVFcHZoNGlocGVTSFNJQUdVLVhqS2huVGp0UkJweHB4RG41eW00Qm9EMUMtaGFEcHYtU0RydFRtdGNWTzFEZk5YSHVVVDAwVU4tUXNkLUFtX2FvRlJSOFFlQT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.I401r_TqG1e1SHekNbo1APWiNP3P4IvA_IBJaoWMbKY'
        fyers = FyersModelv3(token=access_token, is_async=False)
        quotesData = fyers.quotes({"symbols": symbols})
        datadict = {}
        values ={}
        index_dict = {
            "NSE:NIFTY50-INDEX": "Nifty 50",
            "NSE:NIFTY100MFG-INDEX": "Nifty India Manufacturing",
            "NSE:NIFTY100ESG-INDEX": "Nifty100 ESG",
            "NSE:NIFTYDIGITAL-INDEX": "Nifty India Digital",
            "NSE:NIFTYMICRO250-INDEX": "Nifty Microcap 250",
            "NSE:NIFTYCONSDUR-INDEX": "Nifty Consumer Durables",
            "NSE:NIFTYHEALTH-INDEX": "Nifty Healthcare",
            "NSE:NIFTYOILGAS-INDEX": "Nifty Oil and Gas",
            "NSE:NIFTY100ESGSECLDR-INDEX": "Nifty100 ESG Sector Leaders",
            "NSE:NIFTY200MOM30-INDEX": "Nifty200 Momentum 30",
            "NSE:NIFTYALPHALOWVOL-INDEX": "Nifty Alpha Low Volatility",
            "NSE:NIFTY200QLTY30-INDEX": "Nifty200 Quality 30",
            "NSE:NIFTYSMLCAP50-INDEX": "Nifty Smallcap 50",
            "NSE:NIFTYMIDSEL-INDEX": "Nifty Midcap Select",
            "NSE:NIFTYMIDCAP150-INDEX": "Nifty Midcap 150",
            "NSE:NIFTY100EQLWGT-INDEX": "Nifty100 Equal Weight",
            "NSE:NIFTY50EQLWGT-INDEX": "Nifty50 Equal Weight",
            "NSE:NIFTYGS200COMPOSITE-INDEX": "Nifty GS Composite",
            "NSE:NIFTYGS1115YR-INDEX": "Nifty GS 11-15 Year",
            "NSE:NIFTYGS48YR-INDEX": "Nifty GS 4-8 Year",
            "NSE:NIFTYGS10YRCLEAN-INDEX": "Nifty GS 10 Year Clean",
            "NSE:NIFTYGS813YR-INDEX": "Nifty GS 8-13 Year",
            "NSE:NIFTYSMLCAP100-INDEX": "Nifty Smallcap 100",
            "NSE:NIFTY100QLTY30-INDEX": "Nifty100 Quality 30",
            "NSE:NIFTYPVTBANK-INDEX": "Nifty Private Bank",
            "NSE:NIFTYPHARMA-INDEX": "Nifty Pharma",
            "NSE:NIFTYLARGEMID250-INDEX": "Nifty LargeMidcap 250",
            "NSE:NIFTYGS15YRPLUS-INDEX": "Nifty GS 15 Year Plus",
            "NSE:NIFTYPSUBANK-INDEX": "Nifty PSU Bank",
            "NSE:NIFTYSMLCAP250-INDEX": "Nifty Smallcap 250",
            "NSE:NIFTYENERGY-INDEX": "Nifty Energy",
            "NSE:NIFTYALPHA50-INDEX": "Nifty Alpha 50",
            "NSE:NIFTYPSE-INDEX": "Nifty PSE",
            "NSE:NIFTYFINSRV25_50-INDEX": "Nifty Financial Services 25/50",
            "NSE:NIFTYFINSERVICE-INDEX": "Nifty Financial Services",
            "NSE:NIFTYREALTY-INDEX": "Nifty Realty",
            "NSE:NIFTY500-INDEX": "Nifty 500",
            "NSE:NIFTY500MULTICAP-INDEX": "Nifty500 Multicap",
            "NSE:NIFTYMIDCAP50-INDEX": "Nifty Midcap 50",
            "NSE:NIFTYTOTALMKT-INDEX": "Nifty Total Market",
            "NSE:NIFTY50PR2XLEVERAGE-INDEX": "Nifty50 PR 2x Leverage",
            "NSE:INDIAVIX-INDEX": "India VIX",
            "NSE:NIFTYDIVOPPS50-INDEX": "Nifty Dividend Opportunities 50",
            "NSE:NIFTYMNC-INDEX": "Nifty MNC",
            "NSE:NIFTY50VALUE20-INDEX": "Nifty50 Value 20",
            "NSE:NIFTY50-INDEX": "Nifty 50",
            "NSE:HANGSENGBEES-NAV": "Hang Seng BeES",
            "NSE:NIFTY100LIQ15-INDEX": "Nifty100 Liquid 15",
            "NSE:NIFTY50TR2XLEVERAGE-INDEX": "Nifty50 TR 2x Leverage",
            "NSE:NIFTY100-INDEX": "Nifty 100",
            "NSE:NIFTY100LOWVOL30-INDEX": "Nifty100 Low Volatility 30",
            "NSE:NIFTYBANK-INDEX": "Nifty Bank",
            "NSE:NIFTYFMCG-INDEX": "Nifty FMCG",
            "NSE:NIFTYIT-INDEX": "Nifty IT",
            "NSE:NIFTYGS10YR-INDEX": "Nifty GS 10 Year",
            "NSE:NIFTYMIDCAP100-INDEX": "Nifty Midcap 100",
            "NSE:NIFTYNEXT50-INDEX": "Nifty Next 50",
            "NSE:NIFTYM150QLTY50-INDEX": "Nifty MidSmallcap 400",
            "NSE:NIFTYSERVICESECTOR-INDEX": "Nifty Services Sector",
            "NSE:NIFTYMIDSML400-INDEX": "Nifty Midcap Smallcap 400",
            "NSE:NIFTYAUTO-INDEX": "Nifty Auto",
            "NSE:NIFTYMETAL-INDEX": "Nifty Metal",
            "NSE:NIFTYINFRA-INDEX": "Nifty Infrastructure",
            "NSE:NIFTYMEDIA-INDEX": "Nifty Media",
            "NSE:NIFTY50PR1XINVERSE-INDEX": "Nifty50 PR 1x Inverse",
            "NSE:NIFTY200-INDEX": "Nifty 200",
            "NSE:NIFTY50TR1XINVERSE-INDEX": "Nifty50 TR 1x Inverse",
            "NSE:NIFTYCPSE-INDEX": "Nifty CPSE",
            "NSE:NIFTYMIDLIQ15-INDEX": "Nifty Midcap Liquid 15",
            "NSE:NIFTYCOMMODITIES-INDEX": "Nifty Commodities",
            "NSE:NIFTYCONSUMPTION-INDEX": "Nifty Consumption",
            "NSE:NIFTY50DIVPOINT-INDEX": "Nifty50 Dividend Points",
            "NSE:NIFTYGROWSECT15-INDEX": "Nifty Growth Sector 15",
            "BSE:LCTMCI-INDEX": "LCTMCI",
            "BSE:DFRGRI-INDEX": "DFRGRI",
            "BSE:BSEQUI-INDEX": "BSEQUI",
            "BSE:BSEDSI-INDEX": "BSEDSI",
            "BSE:SML250-INDEX": "SML250",
            "BSE:MID150-INDEX": "MID150",
            "BSE:ESG100-INDEX": "ESG100",
            "BSE:SNXT50-INDEX": "SNXT50",
            "BSE:SNSX50-INDEX": "SNSX50",
            "BSE:UTILS-INDEX": "UTILS",
            "BSE:GREENX-INDEX": "GREENX",
            "BSE:SENSEX-INDEX": "SENSEX",
            "BSE:REALTY-INDEX": "REALTY",
            "BSE:BSEPBI-INDEX": "BSEPBI",
            "BSE:CDGS-INDEX": "CDGS",
            "BSE:OILGAS-INDEX": "OILGAS",
            "BSE:ENERGY-INDEX": "ENERGY",
            "BSE:POWER-INDEX": "POWER",
            "BSE:BSE500-INDEX": "BSE500",
            "BSE:BSE100-INDEX": "BSE100",
            "BSE:BSEPSU-INDEX": "BSEPSU",
            "BSE:BSE HC-INDEX": "BSE HC",
            "BSE:MSL400-INDEX": "MSL400",
            "BSE:BHRT22-INDEX": "BHRT22",
            "BSE:BANKEX-INDEX": "BANKEX",
            "BSE:ALLCAP-INDEX": "ALLCAP",
            "BSE:INFRA-INDEX": "INFRA",
            "BSE:BSE CD-INDEX": "BSE CD",
            "BSE:MIDCAP-INDEX": "MIDCAP",
            "BSE:AUTO-INDEX": "AUTO",
            "BSE:BASMTR-INDEX": "BASMTR",
            "BSE:BSE200-INDEX": "BSE200",
            "BSE:FIN-INDEX": "FIN",
            "BSE:BSE CG-INDEX": "BSE CG",
            "BSE:BSEEVI-INDEX": "BSEEVI",
            "BSE:TECK-INDEX": "TECK",
            "BSE:METAL-INDEX": "METAL",
            "BSE:CARBON-INDEX": "CARBON",
            "BSE:MIDSEL-INDEX": "MIDSEL",
            "BSE:SMEIPO-INDEX": "SMEIPO",
            "BSE:BSEMOI-INDEX": "BSEMOI",
            "BSE:TELCOM-INDEX": "TELCOM",
            "BSE:CPSE-INDEX": "CPSE",
            "BSE:LMI250-INDEX": "LMI250",
            "BSE:SMLCAP-INDEX": "SMLCAP",
            "BSE:BSE IT-INDEX": "BSE IT",
            "BSE:MFG-INDEX": "MFG",
            "BSE:INDSTR-INDEX": "INDSTR",
            "BSE:BSELVI-INDEX": "BSELVI",
            "BSE:LRGCAP-INDEX": "LRGCAP",
            "BSE:BSEIPO-INDEX": "BSEIPO",
            "BSE:BSEFMC-INDEX": "BSEFMC",
            "BSE:SMLSEL-INDEX": "SMLSEL"
        }
        mapping = {"1010":'nse_cm' ,"1011": 'nse_fo', "1120" : 'mcx_fo' , "1210" :'bse_cm', "1012" : 'cde_fo'}
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
                    print(data)

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
            return datadict
        

class FyersHsmSocket():

    def __init__(self,access_token, log_path = None , litemode = False):
        self.url = ""
        self.access_token = str(access_token)
        self.log_path = log_path
        self.Source = "PythonSDK-1.0.0"
        self.channelNum = 1
        self.channels = [1,2,3,4,5]
        self.datatype = None
        self.ackCount = None
        self.updateCount = 0
        self.lite = litemode
        self.output = {}
        self.literesp = {}
        self.logger_setup()
        self.logger.info("Initiate socket object")
        self.logger.debug('access_token ' + self.access_token)
        self.logger.error('No error',)
        self.resp = {}
        self.symDict = {}
        self.extra_data = {}
        self.ack_bool = False
        self.dataVal = ["ltp","vol_traded_today" , "last_traded_time" , "ExFeedTime" , "bidSize" , "askSize" , "bidPrice" , "askPrice" , "last_traded_qty" 
                        , "tot_buy_qty" , "tot_sell_qty" ,"avg_trade_price","OI","low_price","high_price" ,"Yhigh", "Ylow", "lowCircuit" , "upCircuit" ,"open_price", "close_price",'symbol']
        self.indexVal = ['ltp', 'close_price', 'ExFeedTime', 'high_price', 'low_price', 'open_price', 'symbol']
        self.litename = ["ltp","vol_traded_today" , "last_traded_time" ]
        self.depthvalue = ["bidPrice1","bidPrice2","bidPrice3","bidPrice4","bidPrice5",
                        "askPrice1", "askPrice2", "askPrice3", "askPrice4", "askPrice5", 
                        "bidsize1","bidsize2","bidsize3","bidsize4","bidsize5",
                        "askSize1","askSize2","askSize3","askSize4","askSize5",
                        "bidorder1","bidorder2","bidorder3","bidorder4","bidorder5",
                        "askorder1","askorder2","askorder3","askorder4","askorder5",'symbol']

    def token_to_byte(self):
        try:
            buffer_size = 18 + len(self.access_token) + len(self.Source)
            byte_buffer = bytearray(buffer_size)
            data_len = buffer_size - 2  
            struct.pack_into("!H", byte_buffer, 0, data_len)
            # ReqType
            byte_buffer[2] = 1 
            # FieldCount
            byte_buffer[3] = 4  
            # Field-1: AuthToken
            field1_id = 1
            field1_size = len(self.access_token)
            struct.pack_into("!B", byte_buffer, 4, field1_id)
            struct.pack_into("!H", byte_buffer, 5, field1_size)
            struct.pack_into(f"!{field1_size}s", byte_buffer, 7, self.access_token.encode())

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
            self.logger.error("Error While packing Token msg", e)


    def full_mode_msg(self):
        try:
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
            self.logger.error("Error While packing Full mode msg", e)
            return
        
    def subscription_msg(self):
        try:
            # self.scrips = self.symbol_token.keys()
            print(len(self.scrips))
            self.scripsData = bytearray()
            self.scripsData.append(len(self.scrips) >> 8 & 0xFF)
            self.scripsData.append(len(self.scrips) & 0xFF)
            for scrip in self.scrips:
                scripBytes = str(scrip).encode("ascii")
                self.scripsData.append(len(scripBytes))
                self.scripsData.extend(scripBytes)

            dataLen = 18 + len(self.scripsData) + len(self.access_token) + len(self.Source)
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
            self.logger.error("Error While packing Subscription msg", e)
            return 
        

    async def unsubscription_msg(self,symbols):
        try:
            conv = SymbolConverstion(symbols,self.datatype)
            scrips = list(conv.symbol_to_token().keys())
            scripsData = bytearray()
            scripsData.append(len(scrips) >> 8 & 0xFF)
            scripsData.append(len(scrips) & 0xFF)
            for scrip in scrips:
                scripBytes = str(scrip).encode("ascii")
                scripsData.append(len(scripBytes))
                scripsData.extend(scripBytes)

            dataLen = 18 + len(scripsData) + len(self.access_token) + len(self.Source)
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

            await self.websocket.send(buffer_msg)

            return buffer_msg
        
        except Exception as e:
            self.logger.error("Error While packing Unsubscription msg", e)
            return 
        

    def ackowledgement_msg(self, messae_number):
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
            self.logger.error("Error While packing Ackowledgement msg", e)
            return

    def auth_resp(self,response_msg):
        try:
            offset = 4
            field_id = struct.unpack('!B', response_msg[offset:offset+1])[0]
            offset += 1
            field_length = struct.unpack('!H', response_msg[offset:offset+2])[0]
            offset += 2
            string_val = response_msg[offset:offset+field_length].decode('utf-8')
            offset += field_length

            if string_val == "K":
                print("Authentication done")
            else:
                print("Authentication failed")

            field_id = struct.unpack('!B', response_msg[offset:offset+1])[0]
            offset += 1
            field_length = struct.unpack('!H', response_msg[offset:offset+2])[0]
            offset += 2
            self.ack_count = struct.unpack('>I', response_msg[offset:offset+4])[0]
            offset += 4
            json_obj = response_msg[offset:].decode()
            
        except Exception as e:
            self.logger.error("Error While Unpacking Auth msg", e)
            return



    def unsubscribe_resp(self,response_msg):
        try:
            print(response_msg)
            offset = 3
            field_count = struct.unpack('B', response_msg[offset:offset+1])[0]
            offset += 1
            field_id = struct.unpack('B', response_msg[offset:offset+1])[0]
            offset += 1
            field_length = struct.unpack('H', response_msg[offset:offset+2])[0]
            offset += 2
            print(offset)
            # string_val = bytes(response_msg[offset:offset+field_length]).decode('latin-1')
            string_val = response_msg[offset:offset+1].decode('latin-1')
            offset += field_length
            print(string_val)
            if string_val == 'K':
                print("Unsubscription done")
            else:
                print("Unsubscription failed")

            return
        except Exception as e:
            self.logger.error("Error While Unpacking unsubscribe msg", e)
            return
                       
    def full_mode_resp(self, response_msg):
        try:
            offset = 3

            # Unpack the field count
            field_count = struct.unpack('!B', response_msg[offset:offset + 1])[0]
            offset += 1

            if field_count >= 1:
                # Unpack the field ID
                field_id = struct.unpack('!B', response_msg[offset:offset + 1])[0]
                offset += 1

                # Unpack the field length
                field_length = struct.unpack('!H', response_msg[offset:offset + 2])[0]
                offset += 2

                # Extract the string value and decode it
                string_val = response_msg[offset:offset + field_length].decode('utf-8')
                offset += field_length

                if string_val == "K":
                    print("Full mode on")
                else:
                    print("Error in full mode connection")
            else:
                print("No fields found in the response")

        except struct.error as e:
            self.logger.error("Error while unpacking Full Mode message: %s", e)
        except UnicodeDecodeError as e:
            self.logger.error("Error decoding string value in Full Mode message: %s", e)
        except Exception as e:
            self.logger.error("Unexpected error in Full Mode response: %s", e)


            
    def response_output(self,data):
        dataResp = data
        # print("-------precision-------",dataResp )
        response = {}
        if 'bidPrice1' in dataResp:

            for i , val in enumerate(self.depthvalue):
                if val in dataResp and i < 10:
                    response[val] = dataResp[val] / (10 ** dataResp['precision']) 
                else:
                    response[val] = dataResp[val]
        elif 'askSize' in dataResp:
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
                if val in dataResp and i in [0]:
                    response[val] = dataResp[val] / (10 ** dataResp['precision']) 
                else:
                    response[val] = dataResp[val]
        
            # if 'OI' in response:
            #     response.pop('OI')
            # if 'Yhigh' in response:
            #     response.pop('Yhigh')
            # if 'Ylow' in response:
            #     response.pop('Ylow')
            # response = dataResp
        print("")
        print(response)

    def datafeed_resp(self,data):
        try:
            updateCount = 0
            if self.ack_count > 0:
                updateCount += 1
                msgNum = struct.unpack('>I', data[3:7])[0]
                if updateCount == self.ack_count:
                    self.ack_bool = True
                    self.ack_msg = self.ackowledgement_msg(msgNum)
                    updateCount = 0
            scripCount = struct.unpack('!H', data[7:9])[0]

            offset = 9
            for _ in range(scripCount):
                dataType = struct.unpack('B', data[offset:offset+1])[0]
                if dataType == 83: #Snapshot datafeed
                    self.output = {} 
                    # self.extra_data = {}
                    offset += 1
                    topicId = struct.unpack('H', data[offset:offset+2])[0]
                    offset += 2
                    topicNameLength = struct.unpack('B', data[offset:offset+1])[0]
                    offset += 1

                    topicName = data[offset:offset+topicNameLength].decode('utf-8')
                    offset += topicNameLength

                    # Maintaining dict - topicId : topicName
                    self.symDict[topicId] = topicName
                    # fieldCount - 21 in scrips , 25 in depth , 6 in index
                    fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                    offset += 1

                    for index in range(fieldCount):
                        value = struct.unpack('>I', data[offset:offset+4])[0]
                        offset += 4
                        if fieldCount == 21:
                            self.output[self.dataVal[index]] = value

                        elif fieldCount == 6:
                            self.output[self.indexVal[index]] = value

                        else:
                            self.output[self.depthvalue[index]] = value 

                    stringFieldLength = struct.unpack('H', data[offset:offset+2])[0]
                    offset += 2

                    multiplier = struct.unpack('H', data[offset:offset+2])[0]
                    self.output["multiplier"] = multiplier
                    offset += 2

                    precision = struct.unpack('B', data[offset:offset+1])[0]
                    self.output["precision"] = precision
                    offset += 1

                    val = ["exchange", "exchange_token", "symbol"]
                    for i in range(3):
                        stringLength = struct.unpack('B', data[offset:offset+1])[0]
                        offset += 1
                        stringData = data[offset:offset+stringLength].decode('utf-8')
                        self.output[val[i]] = stringData
                        offset += stringLength
                    self.output['symbol'] = self.symbol_token[self.symDict[topicId]]
                    self.resp[self.symDict[topicId]] = self.output

                    self.response_output(self.resp[self.symDict[topicId]])
                    
                elif dataType == 85: #Full mode darafeed

                    offset += 1
                    topicId = struct.unpack('H', data[offset:offset+2])[0]
                    offset += 2

                    fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                    offset += 1
                    
                    for index in range(fieldCount):
                        value = struct.unpack('>I', data[offset:offset+4])[0]
                        offset += 4
                        if fieldCount == 21:

                            self.resp[self.symDict[topicId]][self.dataVal[index]] = value
                        elif fieldCount == 6:
                            self.resp[self.symDict[topicId]][self.indexVal[index]] = value
                        else:
                            self.resp[self.symDict[topicId]][self.depthvalue[index]] = value
                            
                    self.response_output(self.resp[self.symDict[topicId]])
                    
                elif dataType == 76: #lite mode datafeed

                    offset += 1
                    topicId = struct.unpack('H', data[offset:offset+2])[0]
                    offset += 2

                    # self.literesp[self.symDict[topicId]] = {}

                    for index in range(3):
                        value = struct.unpack('>I', data[offset:offset+4])[0]
                        offset += 4
                        if index == 0:
                            self.literesp[self.symDict[topicId]][self.litename[index]] = value / 10 ** self.resp[self.symDict[topicId]]['precision']

                    self.literesp[self.symDict[topicId]]['symbol']  = self.literesp[self.symDict[topicId]]['symbol']

                    self.response_output(self.literesp[self.symDict[topicId]])
                else:
                    pass
                
        except Exception as e:
            # pass
            # print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("payload_creation :: ERR : -> Line:{} Exception:{}".format(exc_tb.tb_lineno, str(e)))
            # self.logger.error("Error While Unpacking datafeed", e)
    




    def response_msg(self , data):

        datasize, respType = struct.unpack('!HB', data[:3])
        if respType == 1: # Authentication response
             print(self.auth_resp(data))

        elif respType == 5: # Unsubsciption response

           print(self.unsubscribe_resp(data))

        elif respType == 12: # Full Mode Data Response

            print(self.full_mode_resp(data))

        elif respType == 6: # Data Feed Response
            self.datafeed_resp(data)
        
        elif respType == 5:
            self.unsubscribe_resp()

         
    async def close(self):
        print(f"WebSocket object: {self.websocket}")
        print(f"WebSocket closed state: {self.websocket.closed}")

        if self.websocket and not self.websocket.closed:
            await self.websocket.close()
            
    async def send_ping(self):
        await self.websocket.ping()
        asyncio.get_event_loop().call_later(10, lambda: asyncio.create_task(self.send_ping()))
    
    async def connectWS(self):
        try:
            async with websockets.connect("wss://socket.fydev.tech/hsm/v1-5/dev" ) as websocket:
                self.websocket = websocket
                message = self.token_to_byte()
                await websocket.send(message)
                response = await websocket.recv()
                self.response_msg(response)
                # self.lite = True
                if not self.lite:
                    message = self.full_mode_msg()
                    await websocket.send(message)
                    response = await websocket.recv()
                    self.response_msg(response)

                message = self.subscription_msg()
                await websocket.send(message)
                asyncio.create_task(self.send_ping())
                while True:
                    response = await websocket.recv()
                    # print(response)
                    self.response_msg(response)

                    if self.ack_bool:
                        print('ack---------------------------------------')
                        await websocket.send(self.ack_msg)
                        self.ack_bool = False
                
        except Exception as e:
            # print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error("payload_creation :: ERR : -> Line:{} Exception:{}".format(exc_tb.tb_lineno, str(e)))

        # except KeyboardInterrupt:
        #    self.websocket.close()

    async def subscribe(self,symbols, datatype):

        try:
            self.datatype = datatype
            conv = SymbolConverstion(symbols,datatype)
            self.symbol_token = conv.symbol_to_token()
            self.scrips = list(self.symbol_token.keys())

            await self.connectWS()
        except KeyboardInterrupt:
            tasks = asyncio.all_tasks()

            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)




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

# datadict = ["sf|nse_cm|11536","sf|nse_cm|25","dp|nse_cm|25", "sf|nse_cm|22", "dp|nse_cm|22"]
# access_token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODMwMDE4OTgsImV4cCI6MTY4MzA3MzgzOCwibmJmIjoxNjgzMDAxODk4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa1VKSXFKLTNQMl9BSXFWWFNWUlg5UXlIVW5QWlpGRnFnNG5xRkNWRzYwQU5qX0F6T2hVWmxPZmtCNUV4ak03MXBMWVlqSEpjWXBsaVpVNWpFREQ1R3JFVkt4Rmx0SzR4RDh2SERVdkZndWgwUEVGRT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.MghUuBXEV3INDwH-buwTUvJDvBQ0HS37d69nwRCE7nE"
# client = FyersHsmSocket(access_token,datadict)
# client.subscribe()