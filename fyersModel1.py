moduleName = "fyersModel1"



import tracemalloc

import urllib.parse
import hashlib
import json
from urllib.parse import urlparse
import asyncio 
import subprocess
import sys
import requests
import json
import urllib
import aiohttp
import asyncio
import websockets
import json
from concurrent.futures import ThreadPoolExecutor

class Config:
    Api = "https://api-t1.fyers.in/trade/v3" 
    # Api = "https://api-t1.fydev.tech/trade/dev"
    historyDataUrl = "https://api.fyers.in/data-rest/v2"
    data_Api= "https://api-t1.fyers.in/api/v2/data"
    authUrl = "https://api.fyers.in/api/v2"
    get_profile = '/profile'
    tradebook = '/tradebook'
    positions = '/positions'
    holdings = '/holdings'
    convertPosition = '/positions'
    funds = '/funds'
    orders = '/orders'
    gttorders = '/gtt/orders'

    minquantity = '/minquantity'
    orderStatus = '/order-status'
    marketStatus = '/market-status'
    auth = '/generate-authcode'
    generateAccessToken = '/validate-authcode'
    exitPositions = '/positions'
    generateDataToken = '/data-token'

    dataVendorTD = "truedata-ws"

    multi_orders = '/multi-order'
    history = '/history'
    quotes = '/quotes/v2'
    market_depth = '/depth/v2'

class FyersServiceSync:

    def __init__(self):
        self.content = 'application/json'    

    def postCall(self, api, header, data=None):
        response = requests.post(Config.Api+api,headers={"Authorization":header, 'Content-Type': self.content}, data = data)
        return response.json()
    

    def getCall(self, api, header, data=None,data_flag=False):
        if data_flag:
            if api == '/history':
                URL = Config.historyDataUrl + api
            else:
                URL =  Config.data_Api +api
        else:
            URL = Config.Api + api


        if data is not None:
            url_params = urllib.parse.urlencode(data)
            URL = URL+ "?" + url_params
        print("url",URL)
        response = requests.get(url = URL,headers={"Authorization":header, 'Content-Type': self.content , "version":"V3"})      
        print("response",response)
        return response.json()

    def deleteCall(self,api, header, data):
        response =  requests.delete(url = Config.Api+api,data=json.dumps(data), headers={"Authorization":header, 'Content-Type': self.content})
        return response.json()

    def putCall(self,api,header,data):
        response = requests.put(url = Config.Api+api,headers={"Authorization":header, 'Content-Type': self.content},json=data)
        print(response)
        return response.json()

class FyersServiceAsync:

    def __init__(self):
        self.content = 'application/json'    


    async def postAsyncCall(self,api, header, data=None):
        async with aiohttp.ClientSession(headers={'Authorization': header, 'Content-Type': self.content}) as session:
            url = Config.Api + api
            async with session.post(url, data=json.dumps(data)) as response:
                    response = await response.text()
                    print(response)

                    return response

    async def getAsyncCall(self, api, header, params=None, data_flag=False):
        
        if data_flag:
            if api == '/history':
                URL = Config.historyDataUrl + api
            else:
                URL =  Config.data_Api +api
        else:
            URL = Config.Api + api


        async with aiohttp.ClientSession(headers={'Authorization': header, 'Content-Type': self.content}) as session:
            async with session.get(URL, params=params) as response:
                response_data = await response.json()
                return response_data


    async def deleteAsyncCall(self, api, header, data):
        async with aiohttp.ClientSession(headers={'Authorization': header, 'Content-Type': self.content}) as session:
            url = Config.Api + api
            async with session.delete(url, data=json.dumps(data)) as response:
                return await response.json()

    async def patchAsyncCall(self, api, header, data):
        async with aiohttp.ClientSession(headers={'Authorization': header, 'Content-Type': self.content}) as session:
            url = Config.Api + api
            json_data = json.dumps(data).encode('utf-8')

            async with session.patch(url,  data=json_data ) as response:
                return await response.json()


class SessionModel:
    def __init__(self, client_id=None, redirect_uri=None, response_type=None, scope=None, state=None, nonce=None, secret_key=None, grant_type=None):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.scope = scope
        self.state = state
        self.nonce = nonce
        self.secret_key = secret_key
        self.grant_type = grant_type

    def generate_authcode(self):
        data = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
            "state": self.state
        }
        if self.scope is not None:
            data["scope"] = self.scope
        if self.nonce is not None:
            data["nonce"] = self.nonce
        
        url_params = urllib.parse.urlencode(data)
        return f"{Config.authUrl}{Config.auth}?{url_params}"

    def get_hash(self):
        hash_val = hashlib.sha256(f"{self.client_id}:{self.secret_key}".encode())
        return hash_val

    def set_token(self, token):
        self.auth_token = token

    def generate_token(self):
        data = {
            "grant_type": self.grant_type,
            "appIdHash": self.get_hash().hexdigest(),
            "code": self.auth_token
        }
        service = FyersServiceSync()
        response = service.postCall(Config.generateAccessToken , "", data)
        return response


class FyersModelv3():

    """
    A class that provides methods for making API calls synchronously or asynchronously.

    Attributes:
    ----------
    is_async (bool): A boolean indicating whether API calls should be made asynchronously.
    service (object): An object that provides methods for making API calls.
    header (dict): A dictionary containing header information for making API calls.
    data (dict, optional): A dictionary containing the data to be sent in the request.

    Notes:
    -----
    If `is_async` is True, the call is made asynchronously using `asyncio.run()`. Otherwise, it is made synchronously.
    The response is returned as a dictionary.
    """

    def __init__(self, is_async=False, client_id="", token=""):
        self.client_id = client_id
        self.token = token
        self.is_async = is_async
        self.header = "{}:{}".format(self.client_id, self.token)
        if is_async:
            print("FyersAsyncService1")
            self.service = FyersServiceAsync()
        else:
            print("FyersServiceSYnc")
            self.service = FyersServiceSync()



    def get_profile(self):
        """
        Retrieves the user profile information.

        """
        if self.is_async:
            print("Tradebook async")
            response = asyncio.run(self.service.getAsyncCall(Config.get_profile, self.header))
        else:
            print("Tradebook SYnc profile")
            response = self.service.getCall(Config.get_profile, self.header)
        return response
        
    def tradebook(self, data=None):

        """
        Retrieves daily trade details of the day

        """
        if self.is_async:
            print("Tradebook async")
            response = asyncio.run(self.service.getAsyncCall(Config.tradebook, self.header , params=data))
        else:
            print("Tradebook SYnc")
            response = self.service.getCall(Config.tradebook, self.header, data=data)
        return response
    
    def funds(self, data=None):
        """
        Retrieves funds details

        """

        if self.is_async:
            print("innnnns7777777")

            response = asyncio.run(self.service.getCall(Config.funds, self.header))
        else:
            print("innnnns888888")

            response = self.service.getCall(Config.funds, self.header, data=data)
        return response
   
    def positions(self):
        """
        Retrieves information about current open positions

        """

        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.getAsyncCall(Config.positions, self.header))
        else:
            print("innnnns888888")
            response = self.service.getCall(Config.positions, self.header)
        return response
   

    def holdings(self, data=None):
        """
        Retrieves information about current open positions

        """

        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.getAsyncCall(Config.holdings, self.header, params=data))
        else:
            print("innnnns888888")
            response = self.service.getCall(Config.holdings, self.header, data=data)
        return response
    
    def get_orders(self, data):

        """
        Retrieves order details by Id

        """

        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.getAsyncCall(Config.multi_orders, self.header, params=data))
        else:
            print("innnnns888888")
            response = self.service.getCall(Config.multi_orders, self.header, data=data)
        return response

    
    def orderbook(self, data=None):

        """
        Retrieves the order information.

        """
        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.getAsyncCall(Config.orders, self.header, params=data))
        else:
            print("innnnns888888")
            response = self.service.getCall(Config.orders, self.header, data=data)
        return response


    def minquantity(self):
        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.getAsyncCall(Config.minquantity, self.header))
        else:
            print("innnnns888888")
            response = self.service.getCall(Config.minquantity, self.header)
        return response

    def market_status(self):
        """
        Retrieves market status
        
        """
        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.getAsyncCall(Config.marketStatus, self.header))
        else:
            print("innnnns888888")
            response = self.service.getCall(Config.marketStatus, self.header)
        return response



    def convert_position(self, data):
        """
        Convert position

        """
        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.patchAsyncCall(Config.convertPosition, self.header, data))
        else:
            response = self.service.putCall(Config.convertPosition, self.header, data)
        return response
      


    def cancel_order(self, data):
        """
        cancel position

        """
        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.deleteAsyncCall(Config.orders, self.header, data))
        else:
            response = self.service.deleteCall(Config.orders, self.header, data)
        return response
    
    def placeorder(self,data):    
        async def place_orders(data):
            """
            Order Placement
            """
            # connect to the WebSocket
            async with websockets.connect(
                "wss://socket.fyers.in/trade/v3",
                extra_headers={"authorization": self.header}
            ) as websocket:
                # subscribe to order updates
                message = json.dumps({"T": "SUB_ORD", "SLIST": ["orders"], "SUB_T": 1})
                await websocket.send(message)
                print(f"Sent message: {message}")
                self.orderResponse ={}
                response = self.service.postCall(Config.orders, self.header, data=data)
                print("resp order :",response)
                while True:
                    response_ws = await websocket.recv()
                    response_ws = json.loads(response_ws)
                    print(response_ws)
                    if "orders" in response_ws:
                        print("in---------------",response_ws)
                        id= response_ws['orders']["id"]
                        self.orderResponse["s"] = response["s"]
                        self.orderResponse["code"] = response["code"]
                        self.orderResponse["id"] = response_ws['orders']["id"]
                        self.orderResponse["message"] = f"Order Submitted Successfully. Your Order Ref. No. {id}"
                        return self.orderResponse
                    else:
                        pass
        resp = asyncio.run(place_orders(data))
        return resp

    
    def modify_orders(self, data):
        """
        Modify order
        
        """
        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.patchAsyncCall(Config.orders, self.header, data))
        else:   
            response = self.service.putCall(Config.orders, self.header, data)
        return response
     

    
    def exit_positions(self, data=None):
        """
        Exit by id or exit all
        """
        if self.is_async:
            response = asyncio.run(self.service.deleteAsyncCall(Config.exitPositions, self.header, data))
        else:
            response = self.service.deleteCall(Config.exitPositions, self.header, data)
        return response
    
    def place_gttorder(self, data):
        """
        Order Placement

        """
        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.postAsyncCall(Config.gttorders, self.header, data))
        else:  
            response = self.service.postCall(Config.gttorders, self.header, data)
        return response
    
    def get_gttorders(self, data):

        """
        Retrieves order details by Id

        """

        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.getAsyncCall(Config.gttorders, self.header, params=data))
        else:
            print("innnnns888888")
            response = self.service.getCall(Config.gttorders, self.header, data=data)
        return response
    
    def modify_gttorder(self, data):
            """
            Modify order
            
            """
            if self.is_async:
                print("innnnns7777777")
                response = asyncio.run(self.service.patchAsyncCall(Config.gttorders, self.header, data))
            else:   
                response = self.service.putCall(Config.gttorders, self.header, data)
            return response
        

    def cancel_gttorder(self, data):
        """
        cancel position

        """
        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.deleteAsyncCall(Config.gttorders, self.header, data))
        else:
            response = self.service.deleteCall(Config.gttorders, self.header, data)
        return response
        


    def generate_data_token(self, data):
        allPackages = subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze"]
        )
        installed_packages = [
            r.decode().split("==")[0] for r in allPackages.split()
        ]
        if Config.dataVendorTD not in installed_packages:
            print("Please install truedata package | pip install truedata-ws")
        response = self.service.postCall(
            Config.generateDataToken, self.header, data
        )
        return response



    
    def cancel_basket_orders(self, data):
        """
        Cancel basket order

        """
        if self.is_async:
            response = asyncio.run(self.service.deleteAsyncCall(Config.multi_orders, self.header, data))
        else:
            response = self.service.deleteCall(Config.multi_orders, self.header, data)
        return response


    def place_basket_orders(self, data):

        """
        Place basket order 

        """

        if self.is_async:
            response = asyncio.run(self.service.postAsyncCall(Config.multi_orders, self.header, data))
        else:
            response = self.service.postCall(Config.multi_orders, self.header, data)
        return response
      

    def modify_basket_orders(self, data):

        """
        Modify basket orders

        """
        if self.is_async:
            response = asyncio.run(self.service.patchAsyncCall(Config.multi_orders, self.header, data))
        else:
            response = self.service.putCall(Config.multi_orders, self.header, data)
        return response
       

    def history(self, data=None):
        """
        Retrieves history data 
        """
        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.getAsyncCall(Config.history, self.header, data, data_flag=True))
        else:
            print("innnnns888888")
            response = self.service.getCall(Config.history, self.header, data, data_flag=True)
        return response
    
    def quotes(self, data=None):

        """
        Retrieves Quotes data

        """
        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.getAsyncCall( Config.quotes, self.header, data, data_flag=True))
        else:
            print("innnnns888888")
            response = self.service.getCall( Config.quotes, self.header, data, data_flag=True)
        return response

    def depth(self, data=None):

        """
        Retrieves Market Depth
        
        """
        if self.is_async:
            print("innnnns7777777")
            response = asyncio.run(self.service.getAsyncCall(Config.market_depth, self.header, data, data_flag=True))
        else:
            print("innnnns888888")
            response = self.service.getCall(Config.market_depth, self.header, data, data_flag=True)
        return response
    

