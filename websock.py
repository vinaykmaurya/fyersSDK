import asyncio
import base64
import json
import struct
import threading
import aiohttp
import websockets
import requests


def ByteToJson( data):
    ValName = ["Ltp","TVol" , "Ltt" , "ExFeedTime" , "bidSize" , "askSize" , "bidPrice" , "askPrice" , "Ltq" , "TBuyQ" , "TSellQ" ,"AvgP","OI","low","high" ,"Yhigh", "Ylow", "lowCircuit" , "upCircuit" ,"open", "close"]
    depthvalue = ["bidPrice1","bidPrice2","bidPrice3","bidPrice4","bidPrice5",
  "askPrice1", "askPrice2", "askPrice3", "askPrice4", "askPrice5", 
 "bidsize1","bidsize2","bidsize3","bidsize4","bidsize5",
 "askSize1","askSize2","askSize3","askSize4","askSize5",
 "bidorder1","bidorder2","bidorder3","bidorder4","bidorder5",
 "askorder1","askorder2","askorder3","askorder4","askorder5",]
    

    finalresponse = {
    'Ltp': '',
    'TVol': '',
    'Ltt': '',
    'ExFeedTime': '',
    'bidSize': '',
    'askSize': '',
    'bidPrice': '',
    'askPrice': '',
    'Ltq': '',
    'TBuyQ': '',
    'TSellQ': '',
    'AvgP': '',
    'OI': '',
    'low': '',
    'high': '',
    'Yhigh': '',
    'Ylow': '',
    'lowCircuit': '',
    'upCircuit': '',
    'open': '',
    'close': '',
    'bidPrice1': '',
    'bidPrice2': '',
    'bidPrice3': '',
    'bidPrice4': '',
    'bidPrice5': '',
    'askPrice1': '',
    'askPrice2': '',
    'askPrice3': '',
    'askPrice4': '',
    'askPrice5': '',
    'bidsize1': '',
    'bidsize2': '',
    'bidsize3': '',
    'bidsize4': '',
    'bidsize5': '',
    'askSize1': '',
    'askSize2': '',
    'askSize3': '',
    'askSize4': '',
    'askSize5': '',
    'bidorder1': '',
    'bidorder2': '',
    'bidorder3': '',
    'bidorder4': '',
    'bidorder5': '',
    'askorder1': '',
    'askorder2': '',
    'askorder3': '',
    'askorder4': '',
    'askorder5': ''
}
    response = {}
    resp = {}
    dict1 = {}
    datasize, restype = struct.unpack('!HB', data[:3])

    if restype == 1:
        field_id = struct.unpack('!B', data[4:5])[0]
        field_length = struct.unpack('!H', data[5:7])[0]
        string_val = data[7:7+field_length].decode('utf-8')
        if string_val == "K":
            print("Authentication done")
        else:
            print("Authentication failed")
        field_id = struct.unpack('!B', data[7:8])[0]
        field_length = struct.unpack('!H', data[8:10])[0]
        ack_count = struct.unpack('>I', data[10+field_length:14+field_length])[0]

        ack_count = 64446846
        json_obj = data[14+field_length:].decode()
    elif restype == 4:
        pass #Subscription
    elif restype == 12:
        fieldCount = struct.unpack('!B', data[3:4])[0]
        if fieldCount >= 1:
            field_id = struct.unpack('!B', data[4:5])[0]
            field_length = struct.unpack('!H', data[5:7])[0]
            string_val = data[7:7+field_length].decode('utf-8')
            if string_val == "K":
                print("Full mode onn")
            else:
                print("error in full mode connection")
    elif restype == 6:
        ack_count = 64446846
        updateCount = 0
        if ack_count > 0:
            updateCount += 1
            msgNum = struct.unpack('>I', data[3:7])[0]
            if updateCount == ack_count:
                # send acknoledgement 
                updateCount = 0
        scripCount = struct.unpack('!H', data[7:9])[0]
        offset = 9
        for _ in range(scripCount):
            dataType = struct.unpack('B', data[offset:offset+1])[0]
            print("dataType",dataType)
            if dataType == 83: 
                offset += 1
                topicId = struct.unpack('H', data[offset:offset+2])[0]
                print("topicid",topicId)
                offset += 2
                topicNameLength = struct.unpack('B', data[offset:offset+1])[0]
                offset += 1
                topicName = data[offset:offset+topicNameLength].decode('utf-8')
                offset += topicNameLength
                fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                offset += 1
                for index in range(fieldCount):
                    value = struct.unpack('>I', data[offset:offset+4])[0]
                    offset += 4
                    if fieldCount < 23:
                        # resp[topicId][ValName[index]] = value
                        finalresponse[ValName[index]] = value
                    else:
                        # resp[topicId][depthvalue[index]] = value

                        finalresponse[depthvalue[index]] = value                    
                        # print(f"Field {index+1}: {value}")
                # print("Response : ", response)
                # resp[topicId] = response
                # print("topicResponse : ", resp)
                stringFieldLength = struct.unpack('H', data[offset:offset+2])[0]
                offset += 2
                multiplier = struct.unpack('H', data[offset:offset+2])[0]
                # print("multiplier",multiplier)
                offset += 2
                precision = struct.unpack('B', data[offset:offset+1])[0]
                # print("precision",precision)
                offset += 1
                val = ["ex", "num","symbol"]
                for i in range(3):
                    stringLength = struct.unpack('B', data[offset:offset+1])[0]
                    offset += 1
                    stringData = data[offset:offset+stringLength].decode('utf-8')
                    response[val[i]] = stringData
                    if val[i] == 2:
                        resp[stringData] = topicId
                        symb = stringData
                    offset += stringLength
                dict1[topicId] = response['symbol']

                # resp[symb][topicId] = response
                print(resp)
                
            elif dataType == 85:
                print(data)
                offset += 1
                topicId = struct.unpack('H', data[offset:offset+2])[0]
                # resp[dict1[topicId]] = {}

                print("topicId",topicId)
                response[dict1[topicId]] = finalresponse
                offset += 2
                fieldCount = struct.unpack('B', data[offset:offset+1])[0]
                offset += 1
                for index in range(fieldCount):
                    value = struct.unpack('>I', data[offset:offset+4])[0]
                    offset += 4
                    if fieldCount < 23:
                        response[dict1[topicId]][ValName[index]] = value
                    else:
                        response[dict1[topicId]][depthvalue[index]] = value
                print("finalresponse :",response)
 
            else:
                print("Invalid Datatype Error : ", data)
def responsePrint(data):

    datasize, restype, fieldCount = struct.unpack('!HBB', data[:4])
    ack_count = 0
    if restype == 1:
        field_id = struct.unpack('!B', data[4:5])[0]

        field_length = struct.unpack('!H', data[5:7])[0]
        string_val = data[7:7+field_length].decode('utf-8')
        if string_val == "K":
            print("Authentication done")
        else:
            print("Authentication failed")
        field_id = struct.unpack('!B', data[7:8])[0]
        field_length = struct.unpack('!H', data[8:10])[0]
        ack_count = struct.unpack('>I', data[10+field_length:14+field_length])[0]
        print(ack_count)

        json_obj = data[14+field_length:].decode()
        # print("JSON object:", json_obj)
    elif restype == 4:
        if fieldCount >= 1:
            field_id = struct.unpack('!B', data[4:5])[0]
            field_length = struct.unpack('!H', data[5:7])[0]
            string_val = data[7:7+field_length].decode('utf-8')
            print(string_val)
            if string_val == "K":
                print("Subscribed")
            else:
                print("error in subscibe")
    else:
        updateCount = 0
        if ack_count > 0:
            updateCount += 1
            msgNum = struct.unpack('>I', data[0:4])[0]
            if updateCount == ack_count:
                # send acknoledgement 
                updateCount = 0
        scripCount = struct.unpack('!H', data[4:6])[0]
        for i in range(scripCount):
            dataType =  struct.unpack('!B', data[6:7])[0]
            print(dataType)
class MyClient:
    def __init__(self, access_token,data):
        self.access_token = access_token
        self.output = {}
        self.data = data
    async def connectWS(self):
        async with websockets.connect("wss://socket.fydev.tech/hsm/v1-5/dev" ) as websocket:
            message = bytearray(b'\x00W\x01\x04\x01\x0083fd5caefeb662931c6560cf5991b55e327f33ddf8ca0b2a1b0ed7165\x02\x00\x01N\x03\x00\x01\x01\x04\x00\x0fPythonSDK-1.0.0')
            # message = {"sessionid": "3fd5caefeb662931c6560cf5991b55e327f33ddf8ca0b2a1b0ed7165","type": "cn"} 
            await websocket.send(message)
            print(f"Sent message: {message}")
            response = await websocket.recv()
            # print(response)
            ByteToJson(response)
            message = b'\x00\x11\x0c\x02\x01\x00\x08\x00\x00\x00\x00\x00\x00\x12&\x02\x00\x01F'
            await websocket.send(message)
            # print(f"Sent message: {message}")
            response = await websocket.recv()
            ByteToJson(response)
            # print("full mode resp :  ",response)
            
            message =bytearray(b'\x00{\x04\x02\x01\x00"\x00\x02\x0fsf|nse_cm|11536\x0fdp|nse_cm|11536\x02\x00\x01\x01')
            # message =bytearray(b'\x00u\x04\x02\x01\x00\x1c\x00\x02\x0cnse_cm|11536\x0cnse_fo|84609\x02\x00\x01\x01')
            await websocket.send(message)
            print(f"Sent message: {message}")
          
            while True:
                # await asyncio.sleep(2)

                response = await websocket.recv()
                ByteToJson(response)
                # print(response)

# bytearray(b'\x01-\x06\x00\x00\x00\x02\x00\x02S\x00\x01\x0fdp|nse_cm|11536\x1e\x00\x05{\xde\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x003\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17\x00\x01\x02\x06nse_cm\x0511536\x06TCS-EQS\x00\x00\x0fsf|nse_cm|11536\x15\x00\x05{\xde\x00\x01<\x81d_>\xffd_?~\x00\x00\x003\x00\x00\x00\x00\x00\x05{\xde\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x003\x00\x00\x00\x00\x00\x05s\x8b\x80\x00\x00\x00\x00\x04\xaf8\x00\x05}x\x80\x00\x00\x00\x80\x00\x00\x00\x00\x04L\xaa\x00\x05A<\x00\x04\xb7l\x00\x05{\xde\x00\x17\x00\x01\x02\x06nse_cm\x0511536\x06TCS-EQ')
    async def main(self):
        ws_task = asyncio.create_task(self.connectWS())

        await ws_task

access_token ="XC4EOD67IM-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODMyNTk5MzEsImV4cCI6MTY4MzMzMzAxMSwibmJmIjoxNjgzMjU5OTMxLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa1ZJSWJRd0t5ZW5QYy1WbDNMNGtpdy1pNVozYUhzS1c1MWxMQkwtM3hVYlAyczEzR2c5dG5wTG96c0IzX21qaVpwREdJYU1yMkp5S2lRNnozRXJ4QWVQRHFyOV9aTmRCcEhkMG1aZkxfUnRpWUtYRT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.RVZ8IJXtuDLgPCh6H7skASmwUglzootvgkinBnpfs90"

# data = {
#         "symbol":"NSE:IRFC-EQ",
#         "qty":1,
#         "type":2,
#         "side":1,
#         "productType":"CNC",
#         "limitPrice":0,
#         "stopPrice":0,
#         "disclosedQty":0,
#         "validity":"DAY",
#         "offlineOrder":False,
#         "stopLoss":0,
#         "takeProfit":0
#         }
data = {"noConfirm":True,"productType":"INTRADAY","side":1,"symbol":"NSE:DEEPAKNTR-EQ","qty":1,"disclosedQty":0,"type":2,"LTP":1935.8,"validity":"DAY","filledQty":0,"limitPrice":0,"stopPrice":0,"offlineOrder":False}

client = MyClient(access_token,data)

result = asyncio.run(client.main())
# print(result)



# ["Exfeedtime" ,"TotalVolume" ]

# # ["Ltp","TVol" , "Ltt" , "ExFeedTime" , "bidSize" , "askSize" , "bidPrice" , "askPrice" , "Ltq" , "TBuyQ" , "TSellQ" ,"high" , "lowCircuit" , "upCircuit" ,"open", "close"]


# ["bidPrice1","bidPrice2","bidPrice3","bidPrice4","bidPrice5",
#   "askPrice1", "askPrice2", "askPrice3", "askPrice4", "askPrice5", 
#  "bidsize1","bidsize2","bidsize3","bidsize4","bidsize5",
#  "askSize1","askSize2","askSize3","askSize4","askSize5",
#  "bidorder1","bidorder2","bidorder3","bidorder4","bidorder5",
#  "askorder1","askorder2","askorder3","askorder4","askorder5",]


# resp ={}

# offset += 1
# topicId = struct.unpack('H', data[offset:offset+2])[0]
# # print("topicId",topicId)
# offset += 2
# fieldCount = struct.unpack('B', data[offset:offset+1])[0]
# # print(fieldCount)
# offset += 1
# for index in range(fieldCount):
#     value = struct.unpack('>I', data[offset:offset+4])[0]
#     offset += 4
#     if fieldCount < 23:
#         response[ValName[index]] = value
#     else:
#         response[depthvalue[index]] = value
# resp[topicId]