import asyncio
import time
import requests
import urllib3
# from HsmSocket import FyersHsmSocket

from fyerstest.fyersApi import SessionModel, FyersModelv3
from HsmSocket import FyersHsmSocket
# class SymbolConverstion():
#     def symbol_to_token(symbols):
#         # if len(symbols) > 50:

#         symbols =','.join(symbols)
#         print(symbols)
#         datatype = 'symbolUpdate'
#         client_id = ""
#         access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODU1OTE2MTQsImV4cCI6MTY4NTY2NTgzNCwibmJmIjoxNjg1NTkxNjE0LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2VCWS0wRFoyQmxtUkdOWTZkXzRaTEVFcHZoNGlocGVTSFNJQUdVLVhqS2huVGp0UkJweHB4RG41eW00Qm9EMUMtaGFEcHYtU0RydFRtdGNWTzFEZk5YSHVVVDAwVU4tUXNkLUFtX2FvRlJSOFFlQT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.I401r_TqG1e1SHekNbo1APWiNP3P4IvA_IBJaoWMbKY'
#         fyers = FyersModelv3(token=access_token, is_async=False)
#         quotesData = fyers.quotes({"symbols": symbols})
#         datadict = {}
#         values ={}
#         index_dict = {
#             "NSE:NIFTY50-INDEX": "Nifty 50",
#             "NSE:NIFTY100MFG-INDEX": "Nifty India Manufacturing",
#             "NSE:NIFTY100ESG-INDEX": "Nifty100 ESG",
#             "NSE:NIFTYDIGITAL-INDEX": "Nifty India Digital",
#             "NSE:NIFTYMICRO250-INDEX": "Nifty Microcap 250",
#             "NSE:NIFTYCONSDUR-INDEX": "Nifty Consumer Durables",
#             "NSE:NIFTYHEALTH-INDEX": "Nifty Healthcare",
#             "NSE:NIFTYOILGAS-INDEX": "Nifty Oil and Gas",
#             "NSE:NIFTY100ESGSECLDR-INDEX": "Nifty100 ESG Sector Leaders",
#             "NSE:NIFTY200MOM30-INDEX": "Nifty200 Momentum 30",
#             "NSE:NIFTYALPHALOWVOL-INDEX": "Nifty Alpha Low Volatility",
#             "NSE:NIFTY200QLTY30-INDEX": "Nifty200 Quality 30",
#             "NSE:NIFTYSMLCAP50-INDEX": "Nifty Smallcap 50",
#             "NSE:NIFTYMIDSEL-INDEX": "Nifty Midcap Select",
#             "NSE:NIFTYMIDCAP150-INDEX": "Nifty Midcap 150",
#             "NSE:NIFTY100EQLWGT-INDEX": "Nifty100 Equal Weight",
#             "NSE:NIFTY50EQLWGT-INDEX": "Nifty50 Equal Weight",
#             "NSE:NIFTYGS200COMPOSITE-INDEX": "Nifty GS Composite",
#             "NSE:NIFTYGS1115YR-INDEX": "Nifty GS 11-15 Year",
#             "NSE:NIFTYGS48YR-INDEX": "Nifty GS 4-8 Year",
#             "NSE:NIFTYGS10YRCLEAN-INDEX": "Nifty GS 10 Year Clean",
#             "NSE:NIFTYGS813YR-INDEX": "Nifty GS 8-13 Year",
#             "NSE:NIFTYSMLCAP100-INDEX": "Nifty Smallcap 100",
#             "NSE:NIFTY100QLTY30-INDEX": "Nifty100 Quality 30",
#             "NSE:NIFTYPVTBANK-INDEX": "Nifty Private Bank",
#             "NSE:NIFTYPHARMA-INDEX": "Nifty Pharma",
#             "NSE:NIFTYLARGEMID250-INDEX": "Nifty LargeMidcap 250",
#             "NSE:NIFTYGS15YRPLUS-INDEX": "Nifty GS 15 Year Plus",
#             "NSE:NIFTYPSUBANK-INDEX": "Nifty PSU Bank",
#             "NSE:NIFTYSMLCAP250-INDEX": "Nifty Smallcap 250",
#             "NSE:NIFTYENERGY-INDEX": "Nifty Energy",
#             "NSE:NIFTYALPHA50-INDEX": "Nifty Alpha 50",
#             "NSE:NIFTYPSE-INDEX": "Nifty PSE",
#             "NSE:NIFTYFINSRV25_50-INDEX": "Nifty Financial Services 25/50",
#             "NSE:NIFTYFINSERVICE-INDEX": "Nifty Financial Services",
#             "NSE:NIFTYREALTY-INDEX": "Nifty Realty",
#             "NSE:NIFTY500-INDEX": "Nifty 500",
#             "NSE:NIFTY500MULTICAP-INDEX": "Nifty500 Multicap",
#             "NSE:NIFTYMIDCAP50-INDEX": "Nifty Midcap 50",
#             "NSE:NIFTYTOTALMKT-INDEX": "Nifty Total Market",
#             "NSE:NIFTY50PR2XLEVERAGE-INDEX": "Nifty50 PR 2x Leverage",
#             "NSE:INDIAVIX-INDEX": "India VIX",
#             "NSE:NIFTYDIVOPPS50-INDEX": "Nifty Dividend Opportunities 50",
#             "NSE:NIFTYMNC-INDEX": "Nifty MNC",
#             "NSE:NIFTY50VALUE20-INDEX": "Nifty50 Value 20",
#             "NSE:NIFTY50-INDEX": "Nifty 50",
#             "NSE:HANGSENGBEES-NAV": "Hang Seng BeES",
#             "NSE:NIFTY100LIQ15-INDEX": "Nifty100 Liquid 15",
#             "NSE:NIFTY50TR2XLEVERAGE-INDEX": "Nifty50 TR 2x Leverage",
#             "NSE:NIFTY100-INDEX": "Nifty 100",
#             "NSE:NIFTY100LOWVOL30-INDEX": "Nifty100 Low Volatility 30",
#             "NSE:NIFTYBANK-INDEX": "Nifty Bank",
#             "NSE:NIFTYFMCG-INDEX": "Nifty FMCG",
#             "NSE:NIFTYIT-INDEX": "Nifty IT",
#             "NSE:NIFTYGS10YR-INDEX": "Nifty GS 10 Year",
#             "NSE:NIFTYMIDCAP100-INDEX": "Nifty Midcap 100",
#             "NSE:NIFTYNEXT50-INDEX": "Nifty Next 50",
#             "NSE:NIFTYM150QLTY50-INDEX": "Nifty MidSmallcap 400",
#             "NSE:NIFTYSERVICESECTOR-INDEX": "Nifty Services Sector",
#             "NSE:NIFTYMIDSML400-INDEX": "Nifty Midcap Smallcap 400",
#             "NSE:NIFTYAUTO-INDEX": "Nifty Auto",
#             "NSE:NIFTYMETAL-INDEX": "Nifty Metal",
#             "NSE:NIFTYINFRA-INDEX": "Nifty Infrastructure",
#             "NSE:NIFTYMEDIA-INDEX": "Nifty Media",
#             "NSE:NIFTY50PR1XINVERSE-INDEX": "Nifty50 PR 1x Inverse",
#             "NSE:NIFTY200-INDEX": "Nifty 200",
#             "NSE:NIFTY50TR1XINVERSE-INDEX": "Nifty50 TR 1x Inverse",
#             "NSE:NIFTYCPSE-INDEX": "Nifty CPSE",
#             "NSE:NIFTYMIDLIQ15-INDEX": "Nifty Midcap Liquid 15",
#             "NSE:NIFTYCOMMODITIES-INDEX": "Nifty Commodities",
#             "NSE:NIFTYCONSUMPTION-INDEX": "Nifty Consumption",
#             "NSE:NIFTY50DIVPOINT-INDEX": "Nifty50 Dividend Points",
#             "NSE:NIFTYGROWSECT15-INDEX": "Nifty Growth Sector 15",
#             "BSE:LCTMCI-INDEX": "LCTMCI",
#             "BSE:DFRGRI-INDEX": "DFRGRI",
#             "BSE:BSEQUI-INDEX": "BSEQUI",
#             "BSE:BSEDSI-INDEX": "BSEDSI",
#             "BSE:SML250-INDEX": "SML250",
#             "BSE:MID150-INDEX": "MID150",
#             "BSE:ESG100-INDEX": "ESG100",
#             "BSE:SNXT50-INDEX": "SNXT50",
#             "BSE:SNSX50-INDEX": "SNSX50",
#             "BSE:UTILS-INDEX": "UTILS",
#             "BSE:GREENX-INDEX": "GREENX",
#             "BSE:SENSEX-INDEX": "SENSEX",
#             "BSE:REALTY-INDEX": "REALTY",
#             "BSE:BSEPBI-INDEX": "BSEPBI",
#             "BSE:CDGS-INDEX": "CDGS",
#             "BSE:OILGAS-INDEX": "OILGAS",
#             "BSE:ENERGY-INDEX": "ENERGY",
#             "BSE:POWER-INDEX": "POWER",
#             "BSE:BSE500-INDEX": "BSE500",
#             "BSE:BSE100-INDEX": "BSE100",
#             "BSE:BSEPSU-INDEX": "BSEPSU",
#             "BSE:BSE HC-INDEX": "BSE HC",
#             "BSE:MSL400-INDEX": "MSL400",
#             "BSE:BHRT22-INDEX": "BHRT22",
#             "BSE:BANKEX-INDEX": "BANKEX",
#             "BSE:ALLCAP-INDEX": "ALLCAP",
#             "BSE:INFRA-INDEX": "INFRA",
#             "BSE:BSE CD-INDEX": "BSE CD",
#             "BSE:MIDCAP-INDEX": "MIDCAP",
#             "BSE:AUTO-INDEX": "AUTO",
#             "BSE:BASMTR-INDEX": "BASMTR",
#             "BSE:BSE200-INDEX": "BSE200",
#             "BSE:FIN-INDEX": "FIN",
#             "BSE:BSE CG-INDEX": "BSE CG",
#             "BSE:BSEEVI-INDEX": "BSEEVI",
#             "BSE:TECK-INDEX": "TECK",
#             "BSE:METAL-INDEX": "METAL",
#             "BSE:CARBON-INDEX": "CARBON",
#             "BSE:MIDSEL-INDEX": "MIDSEL",
#             "BSE:SMEIPO-INDEX": "SMEIPO",
#             "BSE:BSEMOI-INDEX": "BSEMOI",
#             "BSE:TELCOM-INDEX": "TELCOM",
#             "BSE:CPSE-INDEX": "CPSE",
#             "BSE:LMI250-INDEX": "LMI250",
#             "BSE:SMLCAP-INDEX": "SMLCAP",
#             "BSE:BSE IT-INDEX": "BSE IT",
#             "BSE:MFG-INDEX": "MFG",
#             "BSE:INDSTR-INDEX": "INDSTR",
#             "BSE:BSELVI-INDEX": "BSELVI",
#             "BSE:LRGCAP-INDEX": "LRGCAP",
#             "BSE:BSEIPO-INDEX": "BSEIPO",
#             "BSE:BSEFMC-INDEX": "BSEFMC",
#             "BSE:SMLSEL-INDEX": "SMLSEL"
#         }
#         mapping = {"1010":'nse_cm' ,"1011": 'nse_fo', "1120" : 'mcx_fo' , "1210" :'bse_cm', "1012" : 'cde_fo'}
#         if 'd' in quotesData:
#             for data in quotesData['d']:
#                 # print(data)
#                 if data['s'] == 'ok':
#                     # datadict[data['n']] = {}
#                     values = {}
#                     # values['exch'] = data['v']['exchange']
#                     values['fyToken'] = data['v']['fyToken']
#                     values['symbol'] = data['v']['symbol']
#                     key = values['fyToken'][:4]
#                     values['segment'] = mapping[key]
#                     data = values['symbol'].split('-')
#                     print(data)

#                     if len(data) > 1 and data[-1] == "INDEX":
#                         if values['symbol'] in index_dict:
#                             values['exToken'] = index_dict[values['symbol']]
#                         else:
#                             values['exToken'] = values['symbol'].split(':')[1].split('-')[0]
#                         values['subSymbol'] = 'if'+ '|'+values['segment'] + '|'+values['exToken']
#                     elif datatype == 'depthUpdate':
#                         values['exToken'] = values['fyToken'][10:]
#                         values['subSymbol'] = 'dp'+ '|'+values['segment'] + '|'+values['exToken']

#                     else :
#                         values['exToken'] = values['fyToken'][10:]
#                         values['subSymbol'] = 'sf'+ '|'+values['segment'] + '|'+values['exToken']
                    


#                     datadict[values['subSymbol']] = values['symbol']
#             return datadict
        # print(datadict,'---------------')
        # access_token ="3fd5caefeb662931c6560cf5991b55e327f33ddf8ca0b2a1b0ed7165"
        # client = FyersHsmSocket(access_token,datadict)
        # # client.subscribe()
        # await client.connectWS()
        # await asyncio.sleep(10)

        # print('---------------------------------',list(datadict.keys())[:30])
        # await client.unsubscription_msg(list(datadict.keys())[:30])
        # # await client.close()
     
    # else:
    #     print(quotesData)
    #     return quotesData
    # print(datadict)
    # data = {'symbol' : 'NSE:NIFTY50-INDEX'}
# symbols = ['NSE:NIFTYMIDCAP50-INDEX','NSE:NIFTY50-INDEX', 'NSE:IDEA-EQ','NSE:NIFTYBANK-INDEX','NSE:ADANIENT-EQ','NSE:ACC-EQ',]


# print(len(symbols))

# asyncio.run(symbol_name(symbols))



async def main():
    symbols =[
    'NSE:ADANIPORTS-EQ',
    'NSE:ASIANPAINT-EQ',
    'NSE:AXISBANK-EQ',
    'NSE:BAJAJ-AUTO-EQ',
    'NSE:BAJFINANCE-EQ',
    'NSE:BAJAJFINSV-EQ',
    'NSE:BHARTIARTL-EQ',
    'NSE:BPCL-EQ',
    'NSE:CIPLA-EQ',
    'NSE:COALINDIA-EQ',
    'NSE:DIVISLAB-EQ',
    'NSE:DRREDDY-EQ',
    'NSE:EICHERMOT-EQ',
    'NSE:GRASIM-EQ',
    'NSE:HCLTECH-EQ',
    'NSE:HDFC-EQ',
    'NSE:HDFCBANK-EQ',
    'NSE:HDFCLIFE-EQ',
    'NSE:HEROMOTOCO-EQ',
    'NSE:HINDALCO-EQ',
    'NSE:HINDUNILVR-EQ',
    'NSE:ICICIBANK-EQ',
    'NSE:INDUSINDBK-EQ',
    'NSE:INFY-EQ',
    'NSE:IOC-EQ',
    'NSE:ITC-EQ',
    'NSE:JSWSTEEL-EQ',
    'NSE:KOTAKBANK-EQ',
    'NSE:LT-EQ',
    'NSE:M&M-EQ',
    'NSE:MARUTI-EQ',
    'NSE:NESTLEIND-EQ',
    'NSE:NTPC-EQ',
    'NSE:ONGC-EQ',
    'NSE:POWERGRID-EQ',
    'NSE:RELIANCE-EQ',
    'NSE:SBI-EQ',
    'NSE:SBILIFE-EQ',
    'NSE:SHREECEM-EQ',
    'NSE:SUNPHARMA-EQ',
    'NSE:TATAMOTORS-EQ',
    'NSE:TATASTEEL-EQ',
    'NSE:TCS-EQ',
    'NSE:TECHM-EQ',
    'NSE:TITAN-EQ',
    'NSE:ULTRACEMCO-EQ',
    'NSE:UPL-EQ',
    'NSE:WIPRO-EQ',
    'NSE:NIFTY5-INDEX',
    'NSE:NIFTYBANK-INDEX',
    'NSE:ADANIENT-EQ',
    'NSE:ADANIGREEN-EQ',
    'NSE:AARTIIND-EQ',
    'NSE:ADANITRANS-EQ',
    'NSE:DEEPAKNTR-EQ',
    'NSE:IRFC-EQ',
    'NSE:IDEA-EQ',
    'NSE:TATACOMM-EQ',
    'NSE:ZOMATO-EQ',
    'NSE:PNB-EQ',
    'NSE:BFINVEST-EQ',
    'NSE:RECLTD-EQ',
    'NSE:ZEEL-EQ',
    'NSE:BRITANNIA-EQ',
    'NSE:NIFTY50-INDEX',
    'NSE:NIFTY100MFG-INDEX',
    'NSE:NIFTY100ESG-INDEX',
    'NSE:NIFTYDIGITAL-INDEX',
    'NSE:NIFTYMICRO250-INDEX',
    'NSE:NIFTYCONSDUR-INDEX',
    'NSE:NIFTYHEALTH-INDEX',
    'NSE:NIFTYOILGAS-INDEX',
    'NSE:NIFTY100ESGSECLDR-INDEX',
    'NSE:NIFTY200MOM30-INDEX',
    'NSE:NIFTYALPHALOWVOL-INDEX',
    'NSE:NIFTY200QLTY30-INDEX',
    'NSE:NIFTYSMLCAP50-INDEX',
    'NSE:NIFTYMIDSEL-INDEX',
    'NSE:NIFTYMIDCAP150-INDEX',
    'NSE:NIFTY100EQLWGT-INDEX',
    'NSE:NIFTY50EQLWGT-INDEX',
    'NSE:NIFTYGS200COMPOSITE-INDEX',
    'NSE:NIFTYGS1115YR-INDEX',
    'NSE:NIFTYGS48YR-INDEX',
    'NSE:NIFTYGS10YRCLEAN-INDEX',
    'NSE:NIFTYGS813YR-INDEX',
    'NSE:NIFTYSMLCAP100-INDEX',
    'NSE:NIFTY100QLTY30-INDEX',
    'NSE:NIFTYPVTBANK-INDEX',
    'NSE:NIFTYPHARMA-INDEX',
    'NSE:NIFTYLARGEMID250-INDEX',
    'NSE:NIFTYGS15YRPLUS-INDEX',
    'NSE:NIFTYPSUBANK-INDEX',
    'NSE:NIFTYSMLCAP250-INDEX',
    'NSE:NIFTYENERGY-INDEX',
    'NSE:NIFTYALPHA50-INDEX',
    'NSE:NIFTYPSE-INDEX',
    'NSE:NIFTYFINSRV25_50-INDEX',
    'NSE:NIFTYFINSERVICE-INDEX',
    'NSE:NIFTYREALTY-INDEX',
    'NSE:NIFTY500-INDEX',
    'NSE:NIFTY500MULTICAP-INDEX',
    'NSE:NIFTYMIDCAP50-INDEX',
    'NSE:NIFTYTOTALMKT-INDEX',
    'NSE:NIFTY50PR2XLEVERAGE-INDEX',
    'NSE:INDIAVIX-INDEX',
    'NSE:NIFTYDIVOPPS50-INDEX',
    'NSE:NIFTYMNC-INDEX',
    'NSE:NIFTY50VALUE20-INDEX',
    'NSE:NIFTY50-INDEX',
    'NSE:HANGSENGBEES-NAV',
    'NSE:NIFTY100LIQ15-INDEX',
    'NSE:NIFTY50TR2XLEVERAGE-INDEX',
    'NSE:NIFTY100-INDEX',
    'NSE:NIFTY100LOWVOL30-INDEX',
    'NSE:NIFTYBANK-INDEX',
    'NSE:NIFTYFMCG-INDEX',
    'NSE:NIFTYIT-INDEX',
    'NSE:NIFTYGS10YR-INDEX',
    'NSE:NIFTYMIDCAP100-INDEX',
    'NSE:NIFTYNEXT50-INDEX',
    'NSE:NIFTYM150QLTY50-INDEX',
    'NSE:NIFTYSERVICESECTOR-INDEX',
    'NSE:NIFTYMIDSML400-INDEX',
    'NSE:NIFTYAUTO-INDEX',
    'NSE:NIFTYMETAL-INDEX',
    'NSE:NIFTYINFRA-INDEX',
    'NSE:NIFTYMEDIA-INDEX',
    'NSE:NIFTY50PR1XINVERSE-INDEX',
    'NSE:NIFTY200-INDEX',
    'NSE:NIFTY50TR1XINVERSE-INDEX',
    'NSE:NIFTYCPSE-INDEX',
    'NSE:NIFTYMIDLIQ15-INDEX',
    'NSE:NIFTYCOMMODITIES-INDEX',
    'NSE:NIFTYCONSUMPTION-INDEX',
    'NSE:NIFTY50DIVPOINT-INDEX',
    'NSE:NIFTYGROWSECT15-INDEX'
]
    client_id = "XC4EOD67IM-100"
    access_token=  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODU2Nzg2MzgsImV4cCI6MTY4NTc1MjI1OCwibmJmIjoxNjg1Njc4NjM4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2VXb3VRNUhBU0w4X1NMWDlaZG1MX0p4MTJlZ1otS3AxRExfaS1lV1lxSno0dmVEME9QQUtmM2M2ZVhiWFVEV0xrTm9BM0stc09jX01ETXo5aVlvYkZlR1ZubUEtVVpaM3ltVmE0ZzRnVnB3T0N0TT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.nln2BZNoMBp30QtuAlfgja1Tqm33PIOO9QSTXyBBYb8"

    # access_token ="3fd5caefeb662931c6560cf5991b55e327f33ddf8ca0b2a1b0ed7165"
    # datadict = symbol_name(symbols)
    # symbols = ['NSE:BHARTIARTL-EQ',"BSE:100LARGECAPTMC-INDEX",]
    client = FyersHsmSocket(access_token, litemode=False)
    connect_task = asyncio.create_task(client.subscribe(symbols,'SymbolUpdate'))
    await asyncio.sleep(10)
    symbols = ['NSE:KOTAKBANK-EQ']
    connect_task = asyncio.create_task(client.subscribe(symbols,'depthUpdate'))

    # await fyers.close()
    # print('---------------------------------',list(datadict.keys())[:35])
    # await client.unsubscription_msg(symbols[:10])
    await asyncio.sleep(10)

    # await client.close()
    await connect_task

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
asyncio.run(main())