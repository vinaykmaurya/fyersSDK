import requests
import urllib3
# from HsmSocket import FyersHsmSocket

from fyerstest.fyersApi import SessionModel, FyersModelv3
from HsmSocket import FyersHsmSocket

def symbol_name(symbols):
    symbols =','.join(symbols)
    datatype = 'symbolUpdate'
    client_id = ""
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODU0MjM1OTYsImV4cCI6MTY4NTQ5MzAxNiwibmJmIjoxNjg1NDIzNTk2LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2RZWHNIQ3Z4dVpDNHB5ZjBtbkx1OHlZQkRiNFFxNzVUazdDbjRRSFRCeTZJb1BDZDE5SFJoZ0VHbVVFX0hVbDV3WDdFa21vbm5MMlRqVEczZFI2UWpxRDA5X2NNVHFLTm1wODR2U2o3ZG1tRENOYz0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.BQ2qqE5QHeqKAQEiuBBwIQkRT9rXZBvGrAaWlFKEQLA'
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
        "NSE:NIFTYGROWSECT15-INDEX": "Nifty Growth Sector 15"
    }
    mapping = {"1010":'nse_cm' ,"1011": 'nse_fo', "1120" : 'mcx_fo' , "1210" :'bse_cm', "1012" : 'cde_fo'}
    if 'd' in quotesData:
        for data in quotesData['d']:
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

                if len(data) > 1 and data[1] == "INDEX":
                    values['exToken'] = index_dict[values['symbol']]
                    values['subSymbol'] = 'if'+ '|'+values['segment'] + '|'+values['exToken']
                elif datatype != 'depthUpdate':
                    values['exToken'] = values['fyToken'][10:]
                    values['subSymbol'] = 'dp'+ '|'+values['segment'] + '|'+values['exToken']

                else :
                    values['exToken'] = values['fyToken'][10:]
                    values['subSymbol'] = 'sf'+ '|'+values['segment'] + '|'+values['exToken']
                


                datadict[values['subSymbol']] = values['symbol']

        print(datadict,'---------------')
        access_token ="3fd5caefeb662931c6560cf5991b55e327f33ddf8ca0b2a1b0ed7165"
        client = FyersHsmSocket(access_token,datadict)
        client.subscribe()

    else:
        print(quotesData)
        return quotesData
    # print(datadict)
    # data = {'symbol' : 'NSE:NIFTY50-INDEX'}
symbols = ['NSE:NIFTYMIDCAP50-INDEX','NSE:NIFTY50-INDEX','MCX:CRUDEOIL23JUNFUT']
symbol_name(symbols)