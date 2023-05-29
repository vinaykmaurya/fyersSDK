import asyncio
import struct
import websockets


class FyersHsmSocket():

    def __init__(self,access_token,scrips, litemode = False):
        self.url = ""
        self.access_token = access_token
        self.Source = "PythonSDK-1.0.0"
        self.channelNum = 1
        self.scrips = scrips
        self.channels = [1,2,3,4,5]
        self.ackCount = None
        self.updateCount = 0
        self.lite = litemode
        self.output = {}
        self.literesp = {}
        self.resp = {}
        self.symDict = {}
        self.ack_bool = False
        self.dataVal = ["ltp","vol_traded_today" , "last_traded_time" , "ExFeedTime" , "bidSize" , "askSize" , "bidPrice" , "askPrice" , "last_traded_qty" , "tot_buy_qty" , "tot_sell_qty" ,"avg_trade_price","OI","low_price","high_price" ,"Yhigh", "Ylow", "lowCircuit" , "upCircuit" ,"open_price", "close_price"]
        self.indexVal = ['ltp', 'close_price', 'ExFeedTime', 'high_price', 'low_price', 'open_price']
        self.litename = ["ltp","vol_traded_today" , "last_traded_time" ]
        self.depthvalue = ["bidPrice1","bidPrice2","bidPrice3","bidPrice4","bidPrice5",
                    "askPrice1", "askPrice2", "askPrice3", "askPrice4", "askPrice5", 
                    "bidsize1","bidsize2","bidsize3","bidsize4","bidsize5",
                    "askSize1","askSize2","askSize3","askSize4","askSize5",
                    "bidorder1","bidorder2","bidorder3","bidorder4","bidorder5",
                    "askorder1","askorder2","askorder3","askorder4","askorder5"]

    def token_to_byte(self):
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
    
    def full_mode_msg(self):
        data = bytearray()

        data.extend(struct.pack('>H', 0))

        data.extend(struct.pack('B', 12))

        data.extend(struct.pack('B', 2))

        channel_bits = 0
        for channel_num in self.channels:
            if channel_num < 64 and channel_num > 0:
                channel_bits |= 1 << channel_num

        field_1 = bytearray()
        field_1.extend(struct.pack('B', 1))   
        field_1.extend(struct.pack('>H', 8))    
        field_1.extend(struct.pack('>Q', channel_bits))  
        data.extend(field_1)

        field_2 = bytearray()
        field_2.extend(struct.pack('B', 2))    
        field_2.extend(struct.pack('>H', 1))    
        field_2.extend(struct.pack('B', 70))   
        data.extend(field_2)

        data_length = len(data) - 2
        data[0] = (data_length >> 8) & 0xFF
        data[1] = data_length & 0xFF

        return data    

    def subscription_msg(self):
        self.scripsData = bytearray()
        self.scripsData.append(len(self.scrips) >> 8 & 0xFF)
        self.scripsData.append(len(self.scrips) & 0xFF)
        for scrip in self.scrips:
            scripBytes = scrip.encode("ascii")
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

    
    def unsubscription_msg(self,scrips):
        scripsData = bytearray()
        scripsData.append(len(scrips) >> 8 & 0xFF)
        scripsData.append(len(scrips) & 0xFF)
        for scrip in scrips:
            scripBytes = scrip.encode("ascii")
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

        return buffer_msg
    
    def ackowledgement_msg(self, messae_number):
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
        except:
            return "Error in auth"

    def unsubscribe_resp(self,response_msg):
        try:
            offset = 3
            field_count = struct.unpack('B', response_msg[offset:offset+1])[0]
            offset += 1
            field_id = struct.unpack('B', response_msg[offset:offset+1])[0]
            offset += 1
            field_length = struct.unpack('H', response_msg[offset:offset+2])[0]
            offset += 2
            string_val = response_msg[offset:offset+field_length].decode('utf-8')
            offset += field_length
            if string_val == 'K':
                return "Unsubscription done"
            else:
                return "Unsubscription failed"
        except:
            return "Error while Unsubcribe"
                       
    def full_mode_resp(self,response_msg):
        try:    
            offset = 3
            fieldCount = struct.unpack('!B', response_msg[offset:offset+1])[0]
            offset += 1
            if fieldCount >= 1:
                field_id = struct.unpack('!B', response_msg[offset:offset+1])[0]
                offset += 1

                field_length = struct.unpack('!H', response_msg[offset:offset+2])[0]
                offset += 2

                string_val = response_msg[offset:offset+field_length].decode('utf-8')
                offset += field_length

                if string_val == "K":
                    print("Full mode on")
                else:
                    print("error in full mode connection")
            else:
                print("error in full mode connection")
        except:
            return "Error"
    def datafeed_resp(self,response_msg):
        try:
            updateCount = 0
            if self.ack_count > 0:
                updateCount += 1
                msgNum = struct.unpack('>I', response_msg[3:7])[0]
                if updateCount == self.ack_count:
                    self.ack_bool = True
                    self.ack_msg = self.ackowledgement_msg(msgNum)
                    updateCount = 0
            scripCount = struct.unpack('!H', response_msg[7:9])[0]
            print('----------------------')               

            offset = 9
            for _ in range(scripCount):
                dataType = struct.unpack('B', response_msg[offset:offset+1])[0]
                print('--1--------------------')               

                if dataType == 83: 
                    self.output = {}
                    offset += 1
                    topicId = struct.unpack('H', response_msg[offset:offset+2])[0]
                    offset += 2
                    topicNameLength = struct.unpack('B', response_msg[offset:offset+1])[0]
                    offset += 1
                    topicName = response_msg[offset:offset+topicNameLength].decode('utf-8')
                    offset += topicNameLength
                    print('----------------------')               

                    # Maintaining dict - topicId : topicName
                    self.symDict[topicId] = topicName
                    fieldCount = struct.unpack('B', response_msg[offset:offset+1])[0]
                    offset += 1
                    for index in range(fieldCount):
                        value = struct.unpack('>I', response_msg[offset:offset+4])[0]
                        offset += 4
                        if fieldCount == 21:
                            self.output[self.dataVal[index]] = value
                        elif fieldCount == 6:
                            self.output[self.indexVal[index]] = value
                        else:
                            self.output[self.depthvalue[index]] = value     
                    print('----------------------')               
                    stringFieldLength = struct.unpack('H', response_msg[offset:offset+2])[0]
                    offset += 2
                    multiplier = struct.unpack('H', response_msg[offset:offset+2])[0]
                    self.output["multiplier"] = multiplier
                    offset += 2
                    precision = struct.unpack('B', response_msg[offset:offset+1])[0]
                    self.output["precision"] = precision
                    offset += 1
                    val = ["exch", "exch_token","symbol"]
                    for i in range(3):
                        stringLength = struct.unpack('B', response_msg[offset:offset+1])[0]
                        offset += 1
                        stringData = response_msg[offset:offset+stringLength].decode('utf-8')
                        self.output[val[i]] = stringData
                        offset += stringLength
                    
                    self.resp[self.symDict[topicId]] = self.output
                    print(self.resp[self.symDict[topicId]])
                    
                elif dataType == 85:
                    offset += 1
                    topicId = struct.unpack('H', response_msg[offset:offset+2])[0]
                    offset += 2
                    fieldCount = struct.unpack('B', response_msg[offset:offset+1])[0]
                    offset += 1
                    for index in range(fieldCount):
                        value = struct.unpack('>I', response_msg[offset:offset+4])[0]
                        offset += 4
                        if fieldCount == 21:

                            if index in [0,6,7,11,13,14,17,18,19,20]:
                                self.resp[self.symDict[topicId]][self.dataVal[index]] = value / (10 ** self.resp[self.symDict[topicId]]['precision'])
                            else:
                                self.resp[self.symDict[topicId]][self.dataVal[index]] = value
                        elif fieldCount == 6:
                            self.output[self.indexVal[index]] = value
                        else:
                            if 0 <= index <= 9:
                                self.resp[self.symDict[topicId]][self.depthvalue[index]] = value / (10 ** self.resp[self.symDict[topicId]]['precision'])
                            else:
                                self.resp[self.symDict[topicId]][self.depthvalue[index]] = value
                            
                    print(self.symDict[topicId] ,"-\n",self.resp[self.symDict[topicId]])
                    print('\n',self.symDict)
                elif dataType == 76:
                    offset += 1
                    topicId = struct.unpack('H', response_msg[offset:offset+2])[0]
                    offset += 2
                    print("topicID :",topicId)
                    self.literesp[self.symDict[topicId]] = {}

                    for index in range(3):
                        value = struct.unpack('>I', response_msg[offset:offset+4])[0]
                        offset += 4
                        self.literesp[self.symDict[topicId]][self.litename[index]] = value
                    self.literesp[self.symDict[topicId]]['symbol']  = self.resp[self.symDict[topicId]]['symbol']
                        # print(f"Field {index+1}: {value}")
                    print(self.symDict[topicId] ,"-\n", self.literesp[self.symDict[topicId]])
                else:
                    pass
        except:
            return "Error in Data"
    def response_msg(self , response_msg):
        try:
            datasize, respType = struct.unpack('!HB', response_msg[:3])
            if respType == 1: # Authentication response
                print(self.auth_resp(response_msg))
            elif respType == 5: # Unsubsciption response
                print(self.unsubscribe_resp(response_msg))
            elif respType == 12: # Full Mode Data Response
                print(self.full_mode_resp(response_msg))
            elif respType == 6: # Data Feed Response
                print(self.datafeed_resp(response_msg))
        except:
            print('error')


    async def close(self):
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
                if not self.lite:
                    message = self.full_mode_msg()
                    await websocket.send(message)
                    response = await websocket.recv()
                    self.response_msg(response)

                message = self.subscription_msg()
                await websocket.send(message)
                asyncio.create_task(self.send_ping())
                x = 0
                while True:
                    response = await websocket.recv()
                    # print(response)
                    self.response_msg(response)

                    if self.ack_bool:
                        await websocket.send(self.ack_msg)
                        self.ack_bool = False
        except Exception as e:
            print("Error While Connecting:", e)


    def subscribe(self):
        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(self.connectWS())
        except KeyboardInterrupt:
            tasks = asyncio.all_tasks(loop=loop)

            for task in tasks:
                task.cancel()
            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        finally:
            loop.close()


access_token ="3fd5caefeb662931c6560cf5991b55e327f33ddf8ca0b2a1b0ed7165"
# access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODMwMDE4OTgsImV4cCI6MTY4MzA3MzgzOCwibmJmIjoxNjgzMDAxODk4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa1VKSXFKLTNQMl9BSXFWWFNWUlg5UXlIVW5QWlpGRnFnNG5xRkNWRzYwQU5qX0F6T2hVWmxPZmtCNUV4ak03MXBMWVlqSEpjWXBsaVpVNWpFREQ1R3JFVkt4Rmx0SzR4RDh2SERVdkZndWgwUEVGRT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.MghUuBXEV3INDwH-buwTUvJDvBQ0HS37d69nwRCE7nE"
scrips =  ['sf|mcx_fo|251196','if|nse_cm|NIFTY LARGEMID250', 'if|nse_cm|NIFTY LARGEMID250']
# 'sf|nse_fo|50128',"sf|nse_cm|11536","sf|nse_cm|25","dp|nse_cm|25", "sf|nse_cm|22", "dp|nse_cm|22"
# scrips = ['if|nse_cm|26017']
client = FyersHsmSocket(access_token,scrips)

# result = asyncio.run(client.main())
client.subscribe()

                # x += 1
                # if x == 10:
                #     scrips = ["sf|nse_cm|25","dp|nse_cm|25","dp|nse_cm|22","sf|nse_cm|11536"]
                #     msg = self.unsubscription_msg(scrips)
                #     await websocket.send(msg)
                #     response = await websocket.recv()
                #     print("unsub response : ",response)
                #     self.response_msg(response)