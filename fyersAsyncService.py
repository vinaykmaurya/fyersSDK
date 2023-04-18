
# class FyersAsyncService1:

#     def __init__(self):
#         self.content = 'application/json'    

#     async def postCall(api, header, data=None):
#         async with aiohttp.ClientSession(headers={'Authorization': header, 'Content-Type': self.content}) as session:
#             url = Config.Api + api
#             json_data = json.dumps(data) if data else None
#             async with session.post(url, data=json_data) as response:
#                 return await response.json()
        
#     async def getCall(api, header, data=""):

#         url_params = urllib.parse.urlencode(data) if data != "" else ''

#         if api in data_apis and url_params != "":
#             url = Config.Api + api + '?' + url_params
#         else:
#             url = Config.Api + api 

#         async with aiohttp.ClientSession(headers={'Authorization': header, 'Content-Type': self.content}) as session:
#             async with session.get(url) as response:
#                 return response.json()
   

#     async def deleteCall(api, header, data=None):
#         async with aiohttp.ClientSession(headers={'Authorization': header, 'Content-Type': self.content}) as session:
#             url = Config.Api + api
#             json_data = json.dumps(data) if data else None
#             async with session.delete(url, data=json_data) as response:
#                 return await response.json()

#     async def putCall(api, header, data):
#         async with aiohttp.ClientSession(headers={'Authorization': header, 'Content-Type': self.content}) as session:
#             url = Config.Api + api
#             async with session.put(url, json=data) as response:
#                 return await response.json()




# class FyersAsyncModel:

#     async def get_profile(self):
#         print("in async")
#         response = await self.service.getAsyncCall(Config.get_profile, self.header)
#         return response

#     async def tradebook_async(self, data=None):
#         response = await self.service.getCall(Config.tradebook, self.header, data=data)
#         return response
    

#     async def positions(self):
#         response = await self.service.getCall(Config.positions,  self.header)
#         return response
       

#     async def holdings(self, data=None):
#         response = await self.service.getCall(Config.holdings,  self.header, data=data)
#         return response
   

#     async def convert_position(self, data):
#         response = await self.service.putCall(Config.convertPosition,  self.header, data)
#         return response
      

#     async def funds(self, data=None):
#         response = await self.service.getCall(Config.funds, self.header, data=data)
#         return response
    
#     async def orderbook(self, data=None):
#         response = await self.service.getCall(Config.orders,  self.header, data=data)
#         return response
       

#     async def cancel_order(self, data):
#         response = await self.service.deleteCall(Config.orders,  self.header, data)
#         return response
        

#     async def place_order(self, data):
#         response = await self.service.postCall(Config.orders,  self.header, data)
#         return response
    
#     async def modify_order(self, data):
#         response = await self.service.putCall(Config.orders,  self.header, data)
#         return response
     

#     async def minquantity(self):
#         response = await self.service.getCall(Config.minquantity,  self.header)
#         return response
      

#     async def market_status(self):
#         response = await self.service.getCall(Config.marketStatus,  self.header)
#         return response
       
#     async def exit_positions(self, data=None):
#         response = await self.service.deleteCall(Config.exitPositions,  self.header, data)
#         return response

#     async def get_orders(self, data):
#         response = await self.service.getCall(Config.multi_orders,  self.header, data=data)
#         return response
      
#     async def cancel_basket_orders(self, data):
#         response = await self.service.deleteCall(Config.multi_orders,  self.header, data)
#         return response


#     async def place_basket_orders(self, data):
#         response = await self.service.postCall(Config.multi_orders,  self.header, data)
#         return response
      

#     async def modify_basket_orders(self, data):
#         response = await self.service.putCall(Config.multi_orders,  self.header, data)
#         return response
       

#     async def history(self, data=None):
#         response = await self.service.getCall(
#             Config.history,  self.header, data, data_flag=True
#         )
#         return response
     
#     async def quotes(self, data=None):
#         response = await self.service.getCall(
#             Config.quotes,  self.header, data, data_flag=True
#         )
#         return response
       

#     async def depth(self, data=None):
#         response = await self.service.getCall(
#             Config.market_depth,  self.header, data, data_flag=True
#         )
#         return response
       
    