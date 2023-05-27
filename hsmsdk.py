import requests
import urllib3
from HsmSocket import FyersHsmSocket

from fyerstest.fyersApi import SessionModel, FyersModelv3


# def symbol_name(self , symbol)
client_id = "XC4EOD67IM-100"
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODUwODM4NDMsImV4cCI6MTY4NTE0NzQ0MywibmJmIjoxNjg1MDgzODQzLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2NGYkRlUDVvWloxWDBBeWZrR1hMTVd4VjZlV1lKQUNRNThoODJIOHBuQVB6a0NxNE9KWGp0Z2pvalI0TlFLOU4yLWgzVjI2SjV0RElZbExrd3B2WkxyaHBqOGtrR3B2ZTdXbFpaVmtDdXRXbU5fcz0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.Yavy8qKce6ZI38RdIKz1geipr3l8jX4b-7LeLmCnwgk'
fyers = FyersModelv3(token=access_token, is_async=False, client_id=client_id)
quotesData = fyers.quotes({"symbols":"NSE:NIFTY50-INDEX,NSE:ONGC-EQ,NSE:SBIN-EQ"})
# print(quotesData,'\n')
datadict = {}
values ={}
if 'd' in quotesData:
    for data in quotesData['d']:
        if data['s'] == 'ok':
            # datadict[data['n']] = {}
            values = {}
            # values['exch'] = data['v']['exchange']
            values['fyToken'] = data['v']['fyToken']
            values['symbol'] = data['v']['symbol']
            data = values['symbol'].split('-')
            if data[1] == "INDEX":
                values['exToken'] = values['symbol'].split(':')[1].split('-')[0]
            else:
                values['exToken'] = values['fyToken'][10:]
            mapping = {"1010":'nse_cm' ,"1011": 'nse_fo', "1120" : 'mcx_fo' , "1210" :'bse_cm', "1012" : 'cde_fo'}
            key = values['fyToken'][:4]
            # print(key)
            values['segment'] = mapping[key]

            values['subSymbol'] = 'sf'+ '|'+values['segment'] + '|'+values['exToken']
            datadict[values['symbol']] = values
            print(datadict)
else:
    print(quotesData)
# print(datadict)
# data = {'symbol' : 'NSE:NIFTY50-INDEX'}
