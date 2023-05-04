import asyncio
import json
import threading
import aiohttp
import websockets
import requests

from fyersModel1 import Config

class MyClient:
    def __init__(self, access_token,data):
        self.access_token = access_token
        self.output = {}
        self.data = data
    async def connectWS(self):
        async with websockets.connect(
            "wss://socket.fyers.in/trade/v3",
            extra_headers={"authorization": self.access_token}
        ) as websocket:
            message = json.dumps({"T": "SUB_ORD", "SLIST": ["orders"], "SUB_T": 1})
            await websocket.send(message)
            print(f"Sent message: {message}")

            while True:
                await asyncio.sleep(2)

                response = await websocket.recv()
                # print(f"Received response: {response}")
                response = json.loads(response)
                # self.output.append(response)
                
                if "orders" in response:
                    # self.output.append(response)
                    # print(response)
                    self.output[response["orders"]["id_fyers"]] = response["orders"]["id"]
                    # return
                #     self.output["0"] = response

                # else:
                    # self.output["1"] = response
    
    async def postAsyncCall(self, data=None):
        async with aiohttp.ClientSession(headers={'Authorization': self.access_token, 'Content-Type':'application/json'}) as session:
            url = Config.Api + "/orders"
            async with session.post(url, data=json.dumps(data)) as response:
                    response = await response.text()
                    print(response)
                    return response

    async def main(self):
        ws_task = asyncio.create_task(self.connectWS())
        await asyncio.sleep(2)
        api_task = asyncio.create_task(self.postAsyncCall(self.data))
        # await ws_task
        api_response = await api_task
        await asyncio.sleep(3)
        print("222222", api_response)

        # await asyncio.sleep(5)
        return self.output


access_token ="XC4EOD67IM-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODMxNzM1MTIsImV4cCI6MTY4MzI0NjY1MiwibmJmIjoxNjgzMTczNTEyLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa1V6Q0lHQk1iWVhfcnBVX3JHbDdjb1ZyaDY4TlIwOHRkcDkxWTJ5SGlVeGFucFVtX2RqOFNycTNpRkpBWDVaZ2MyVm5vbl8yWGRlelRfOEJmY1hXWE1TTnZTOU42YWZ3VUpfR3VyTVY1M0Fsck4ycz0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.TUlu1VX_zyNCrwvbhS4nGmGQprjcVfOKn85guw8zi3s"

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
print(result)
