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
        self.resp = {}
        self.symDict = {}

    def TokenByteMsg(self):
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

    def channelArray(self):
        bits = 0
        for channel_num in self.channels:
            if 0 <= channel_num < 64:
                bits |= 1 << channel_num
        return bits
    
    def SetToFullMode(self):
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

    def SubscribeMsgByte(self):
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
        buffer = bytearray()
        buffer.extend(struct.pack(">H", dataLen))
        buffer.append(reqType)
        buffer.append(fieldCount)

        # Field-1
        buffer.append(1)
        buffer.extend(struct.pack(">H", len(self.scripsData)))
        buffer.extend(self.scripsData)

        # Field-2
        buffer.append(2) 
        buffer.extend(struct.pack(">H", 1))
        buffer.append(self.channelNum)

        return buffer
    
    def UnSubscribeByte(self,scrips):
        # self.channelNum = 1
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
        buffer = bytearray()
        buffer.extend(struct.pack(">H", dataLen))
        buffer.append(reqType)
        buffer.append(fieldCount)

        # Field-1
        buffer.append(1) 
        buffer.extend(struct.pack(">H", len(scripsData)))
        buffer.extend(scripsData)

        # Field-2
        buffer.append(2) 
        buffer.extend(struct.pack(">H", 1))
        buffer.append(self.channelNum)

        return buffer

    def ByteToJson(self , data):
        ValName = ["ltp","vol_traded_today" , "last_traded_time" , "ExFeedTime" , "bidSize" , "askSize" , "bidPrice" , "askPrice" , "last_traded_qty" , "tot_buy_qty" , "tot_sell_qty" ,"avg_trade_price","OI","low_price","high_price" ,"Yhigh", "Ylow", "lowCircuit" , "upCircuit" ,"open_price", "close_price"]

        depthvalue = ["bidPrice1","bidPrice2","bidPrice3","bidPrice4","bidPrice5",
                    "askPrice1", "askPrice2", "askPrice3", "askPrice4", "askPrice5", 
                    "bidsize1","bidsize2","bidsize3","bidsize4","bidsize5",
                    "askSize1","askSize2","askSize3","askSize4","askSize5",
                    "bidorder1","bidorder2","bidorder3","bidorder4","bidorder5",
                    "askorder1","askorder2","askorder3","askorder4","askorder5",]
        

        datasize, respType = struct.unpack('!HB', data[:3])

        if respType == 1: # Authentication response
            field_id = struct.unpack('!B', data[4:5])[0]
            field_length = struct.unpack('!H', data[5:7])[0]
            string_val = data[7:7+field_length].decode('utf-8')
            if string_val == "K":
                print("Authentication done")
            else:
                print("Authentication failed")
            field_id = struct.unpack('!B', data[7:8])[0]
            field_length = struct.unpack('!H', data[8:10])[0]
            self.ack_count = struct.unpack('>I', data[10+field_length:14+field_length])[0]
            json_obj = data[14+field_length:].decode()

        elif respType == 5: # Unsubsciption response

            fieldCount = struct.unpack('!B', data[3:4])[0]
            field_id = struct.unpack('!B', data[4:5])[0]
            string_val = data[7:9].decode('utf-8')
            if string_val == "K":
                print("Unsubs done")
            else:
                print("unsubs failed")

        elif respType == 12: # Full Mode Data Response

            fieldCount = struct.unpack('!B', data[3:4])[0]
            if fieldCount >= 1:
                field_id = struct.unpack('!B', data[4:5])[0]
                field_length = struct.unpack('!H', data[5:7])[0]
                string_val = data[7:7+field_length].decode('utf-8')
                if string_val == "K":
                    print("Full mode onn")
                else:
                    print("error in full mode connection")
        elif respType == 6: # Data Feed Response
            updateCount = 0

            if self.ack_count > 0:
                updateCount += 1
                msgNum = struct.unpack('>I', data[3:7])[0]
                if updateCount == self.ack_count:
                    # send acknoledgement 
                    updateCount = 0
            scripCount = struct.unpack('!H', data[7:9])[0]
            offset = 9
            for _ in range(scripCount):
                dataType = struct.unpack('B', data[offset:offset+1])[0]
                print("dataType",dataType)
                if dataType == 83: 
                    self.output = {}
                    offset += 1
                    topicId = struct.unpack('H', data[offset:offset+2])[0]
                    print("topicid",topicId)
                    offset += 2
                    topicNameLength = struct.unpack('B', data[offset:offset+1])[0]
                    offset += 1
                    topicName = data[offset:offset+topicNameLength].decode('utf-8')
                    offset += topicNameLength
                    self.symDict[topicId] = topicName
                    print("topic Name ------",topicName)
                    fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                    offset += 1
                    for index in range(fieldCount):
                        value = struct.unpack('>I', data[offset:offset+4])[0]
                        offset += 4
                        if fieldCount < 23:
                            self.output[ValName[index]] = value
                        else:
                            self.output[depthvalue[index]] = value                    

                    stringFieldLength = struct.unpack('H', data[offset:offset+2])[0]
                    offset += 2
                    multiplier = struct.unpack('H', data[offset:offset+2])[0]
                    # print("multiplier",multiplier)
                    offset += 2
                    precision = struct.unpack('B', data[offset:offset+1])[0]
                    # print("precision",precision)
                    self.output["precision"] = precision
                    offset += 1
                    val = ["EX", "ExToken","Symbol"]
                    for i in range(3):
                        stringLength = struct.unpack('B', data[offset:offset+1])[0]
                        offset += 1
                        stringData = data[offset:offset+stringLength].decode('utf-8')
                        self.output[val[i]] = stringData
                        if i == 2:
                            symb = stringData
                        offset += stringLength
                    
                    self.resp[self.symDict[topicId]] = self.output

                    print("======",self.symDict[topicId])
                    print("Response : ", self.output)
                    
                elif dataType == 85:
                    offset += 1
                    topicId = struct.unpack('H', data[offset:offset+2])[0]
                    print("topicId",topicId)
                    # self.output[self.symDict[topicId]] = {}
                    # self.output = {}
                    offset += 2
                    fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                    offset += 1
                    for index in range(fieldCount):
                        value = struct.unpack('>I', data[offset:offset+4])[0]
                        offset += 4
                        # print("--------------------",self.output[self.symDict[topicId]])
                        if fieldCount < 23:
                            self.resp[self.symDict[topicId]][ValName[index]] = value
                        else:
                            self.resp[self.symDict[topicId]][depthvalue[index]] = value

                    # self.output["symbol"] = self.symDict[topicId]
                    print("finalresponse :",self.symDict[topicId], "---" ,self.resp[self.symDict[topicId]])
                else:
                    print("Invalid Datatype Error : ", data)


    async def close(self, websocket_task):
        if not websocket_task.done():
            websocket = websocket_task.result()
            if not websocket.closed:
                await websocket.close()
    async def send_ping(self, websocket):
        await websocket.ping() 
        print("ping")
        asyncio.get_event_loop().call_later(10, lambda: asyncio.ensure_future(self.send_ping(websocket)))
    
    async def connectWS(self):
        async with websockets.connect("wss://socket.fydev.tech/hsm/v1-5/dev" ) as websocket:
            # message = bytearray(b'\x00W\x01\x04\x01\x0083fd5caefeb662931c6560cf5991b55e327f33ddf8ca0b2a1b0ed7165\x02\x00\x01N\x03\x00\x01\x01\x04\x00\x0fPythonSDK-1.0.0')
            message = self.TokenByteMsg()
            await websocket.send(message)
            print(f"Sent message: {message}")
            response = await websocket.recv()
            # print(response)
            self.ByteToJson(response)
            # message = b'\x00\x11\x0c\x02\x01\x00\x08\x00\x00\x00\x00\x00\x00\x12&\x02\x00\x01F'
            if not self.lite:
                message = self.SetToFullMode()
                await websocket.send(message)
                response = await websocket.recv()
                self.ByteToJson(response)
                
            # message = bytearray(b'\x00\xaf\x04\x02\x01\x00V\x00\x06\x0fsf|nse_cm|11536\x0fdp|nse_cm|11536\x0csf|nse_cm|25\x0cdp|nse_cm|25\x0csf|nse_cm|22\x0cdp|nse_cm|22\x02\x00\x01\x01')
            # message =bytearray(b'\x00{\x04\x02\x01\x00"\x00\x02\x0fsf|nse_cm|11536\x0fdp|nse_cm|11536\x02\x00\x01\x01')
            message = self.SubscribeMsgByte()
            await websocket.send(message)
            print(f"Sent message: {message}")
            asyncio.ensure_future(self.send_ping(websocket))
            x = 0
            while True:
                response = await websocket.recv()
                self.ByteToJson(response)
                # x += 1
                # print("-------------------------------",x)
                # if x == 10:
                #     scrips = ["sf|nse_cm|25","dp|nse_cm|25", "sf|nse_cm|22", "dp|nse_cm|22"]
                #     msg = self.UnSubscribeByte(scrips)
                #     await websocket.send(msg)
                #     response = await websocket.recv()
                #     self.ByteToJson(response)


    # async def main(self):
    #     ws_task = asyncio.create_task(self.connectWS())

    #     await ws_task
    def subscribe(self):
        loop = asyncio.get_event_loop()
        websocket_task = loop.create_task(self.connectWS())
        try:
            loop.run_until_complete(websocket_task)
        except KeyboardInterrupt:
            websocket_task.cancel()
            try:
                loop.run_until_complete(websocket_task)
            except asyncio.CancelledError:
                pass
            finally:
                loop.run_until_complete(self.close(websocket_task))
        finally:
            loop.close()
# access_token ="3fd5caefeb662931c6560cf5991b55e327f33ddf8ca0b2a1b0ed7165"
# access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLmZ5ZXJzLmluIiwiaWF0IjoxNjg0NzMwNDA2LCJleHAiOjE2ODQ4MDE4MDYsIm5iZiI6MTY4NDczMDQwNiwiYXVkIjpbIng6MCJdLCJzdWIiOiJhY2Nlc3NfdG9rZW4iLCJhdF9oYXNoIjoiZ0FBQUFBQmthdkltdGMtQUFueTVnR2liMGRtVHdXeko5TmFuTUtEVlBzYTVHRnRFaUdCczN1OTh2ZE01UFlZanNOc3Bfd2szbEpYcUU5cXJTQVQ2eXJDZTh0R0pBcnlFcFJtaWhaSVMtSVBPZmY1VkVlX3M3U0U9IiwiZGlzcGxheV9uYW1lIjoiVklOQVkgS1VNQVIgTUFVUllBIiwiZnlfaWQiOiJYVjIwOTg2IiwiYXBwVHlwZSI6IiIsIm9tcyI6IksxIiwicG9hX2ZsYWciOiJOIiwiaHNtX2tleSI6IjNmZDVjYWVmZWI2NjI5MzFjNjU2MGNmNTk5MWI1NWUzMjdmMzNkZGY4Y2EwYjJhMWIwZWQ3MTY1In0.8I11EvKNf-Z4dHn8nd6gSM0AhN0D4zf0-e59GWaEP_8"
# access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODQ3MzgzMjUsImV4cCI6MTY4NDgwMTgwNSwibmJmIjoxNjg0NzM4MzI1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2F4RVZLSWZPVGVUNkZtYmw4b29wLW9sTU1JaG0waU1IOGIzZmNESlVxNjI1andudnM1LXdTTnA0RTR0TmY1aGxDWWNFUm56QXlnNWVmWFFTUVFiR0M2Y0NaMVVKN3hkc2ptZ3FMZkxOejhsa3FWZz0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.8GfqzLmubDCX-FCcjIppkzurYhz4wakgaeeD5Ryk30s"
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODMwMDE4OTgsImV4cCI6MTY4MzA3MzgzOCwibmJmIjoxNjgzMDAxODk4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa1VKSXFKLTNQMl9BSXFWWFNWUlg5UXlIVW5QWlpGRnFnNG5xRkNWRzYwQU5qX0F6T2hVWmxPZmtCNUV4ak03MXBMWVlqSEpjWXBsaVpVNWpFREQ1R3JFVkt4Rmx0SzR4RDh2SERVdkZndWgwUEVGRT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.MghUuBXEV3INDwH-buwTUvJDvBQ0HS37d69nwRCE7nE"
scrips =  ["sf|nse_cm|11536","sf|nse_cm|25","dp|nse_cm|25", "sf|nse_cm|22", "dp|nse_cm|22"]
client = FyersHsmSocket(access_token,scrips)

# result = asyncio.run(client.main())
client.subscribe()

