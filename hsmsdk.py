import asyncio
import time
import requests
import urllib3
# from HsmSocket import FyersHsmSocket

from fyerstest.fyersApi import SessionModel, FyersModelv3
from HsmSocket import FyersHsmSocket
class SymbolConverstion():

    def __init__(self,access_token,symbols,datatype):
        self.symbols = symbols
        self.datatype = datatype
        self.access_token = access_token


    def symbol_to_token(self):   

        symbols =','.join(self.symbols)
        print(len(self.symbols))
        client_id = ""
        
        fyers = FyersModelv3(token=self.access_token, is_async=False)
        quotesData = fyers.quotes({"symbols": symbols})
        datadict = {}
        values ={}
        index_dict = {
            "NSE:NIFTY50-INDEX": "Nifty 50",
            "NSE:NIFTYINDIAMFG-INDEX": "Nifty India Manufacturing",
            "NSE:NIFTY100ESG-INDEX": "Nifty100 ESG",
            "NSE:NIFTYINDDIGITAL-INDEX": "Nifty India Digital",
            "NSE:NIFTYMICROCAP250-INDEX": "Nifty Microcap 250",
            "NSE:NIFTYCONSRDURBL-INDEX": "Nifty Consumer Durables",
            "NSE:NIFTYHEALTHCARE-INDEX": "Nifty Healthcare",
            "NSE:NIFTYOILANDGAS-INDEX": "Nifty Oil and Gas",
            "NSE:NIFTY100ESGSECLDR-INDEX": "Nifty100 ESG Sector Leaders",
            "NSE:NIFTY200MOMENTM30-INDEX": "Nifty200 Momentum 30",
            "NSE:NIFTYALPHALOWVOL-INDEX": "Nifty Alpha Low Volatility",
            "NSE:NIFTY200QUALTY30-INDEX": "Nifty200 Quality 30",
            "NSE:NIFTYSMLCAP50-INDEX": "Nifty Smallcap 50",
            "NSE:NIFTYMIDSELECT-INDEX": "Nifty Midcap Select",
            "NSE:NIFTYMIDCAP150-INDEX": "Nifty Midcap 150",
            "NSE:NIFTY100 EQL WGT-INDEX": "Nifty100 Equal Weight",
            "NSE:NIFTY50 EQL WGT-INDEX": "Nifty50 Equal Weight",
            "NSE:NIFTYGSCOMPSITE-INDEX": "Nifty GS Composite",
            "NSE:NIFTYGS1115YR-INDEX": "Nifty GS 11-15 Year",
            "NSE:NIFTYGS48YR-INDEX": "Nifty GS 4-8 Year",
            "NSE:NIFTYGS10YRCLN-INDEX": "Nifty GS 10 Year Clean",
            "NSE:NIFTYGS813YR-INDEX": "Nifty GS 8-13 Year",
            "NSE:NIFTYSMLCAP100-INDEX": "Nifty Smallcap 100",
            "NSE:NIFTYQUALITY30-INDEX": "Nifty100 Quality 30",
            "NSE:NIFTYPVTBANK-INDEX": "Nifty Private Bank",
            "NSE:NIFTYPHARMA-INDEX": "Nifty Pharma",
            "NSE:NIFTYLARGEMID250-INDEX": "Nifty LargeMidcap 250",
            "NSE:NIFTYGS15YRPLUS-INDEX": "Nifty GS 15 Year Plus",
            "NSE:NIFTYPSUBANK-INDEX": "Nifty PSU Bank",
            "NSE:NIFTYSMLCAP250-INDEX": "Nifty Smallcap 250",
            "NSE:NIFTYENERGY-INDEX": "Nifty Energy",
            "NSE:NIFTYALPHA50-INDEX": "Nifty Alpha 50",
            "NSE:NIFTYPSE-INDEX": "Nifty PSE",
            "NSE:NIFTYFINSRV2550-INDEX": "Nifty Financial Services 25/50",
            "NSE:FINNIFTY-INDEX": "Nifty Fin Service",
            "NSE:NIFTYREALTY-INDEX": "Nifty Realty",
            "NSE:NIFTY500-INDEX": "Nifty 500",
            "NSE:NIFTY500MULTICAP-INDEX": "Nifty500 Multicap",
            "NSE:NIFTYMIDCAP50-INDEX": "Nifty Midcap 50",
            "NSE:NIFTYTOTALMKT-INDEX": "Nifty Total Market",
            "NSE:NIFTY50PR2XLEV-INDEX": "Nifty50 PR 2x Leverage",
            "NSE:INDIAVIX-INDEX": "India VIX",
            "NSE:NIFTYDIVOPPS50-INDEX": "Nifty Dividend Opportunities 50",
            "NSE:NIFTYMNC-INDEX": "Nifty MNC",
            "NSE:NIFTY50VALUE20-INDEX": "Nifty50 Value 20",
            "NSE:NIFTY50-INDEX": "Nifty 50",
            "NSE:HANGSENG BEES-NAV-INDEX": "Hang Seng BeES",
            "NSE:NIFTY100LIQ15-INDEX": "Nifty100 Liquid 15",
            "NSE:NIFTY50TR2XLEV-INDEX": "Nifty50 TR 2x Leverage",
            "NSE:NIFTY100-INDEX": "Nifty 100",
            "NSE:NIFTY100 LOWVOL30-INDEX": "Nifty100 Low Volatility 30",
            "NSE:NIFTYBANK-INDEX": "Nifty Bank",
            "NSE:NIFTYFMCG-INDEX": "Nifty FMCG",
            "NSE:NIFTYIT-INDEX": "Nifty IT",
            "NSE:NIFTYGS10YR-INDEX": "Nifty GS 10 Year",
            "NSE:NIFTYMIDCAP100-INDEX": "Nifty Midcap 100",
            "NSE:NIFTYNEXT50-INDEX": "Nifty Next 50",
            "NSE:NIFTYM150QLTY50-INDEX": "Nifty MidSmallcap 400",
            "NSE:NIFTYSERVSECTOR-INDEX": "Nifty Services Sector",
            "NSE:NIFTYMIDSML400-INDEX": "Nifty Midcap Smallcap 400",
            "NSE:NIFTYAUTO-INDEX": "Nifty Auto",
            "NSE:NIFTYMETAL-INDEX": "Nifty Metal",
            "NSE:NIFTYINFRA-INDEX": "Nifty Infrastructure",
            "NSE:NIFTYMEDIA-INDEX": "Nifty Media",
            "NSE:NIFTY50PR1XINV-INDEX": "Nifty50 PR 1x Inverse",
            "NSE:NIFTY200-INDEX": "Nifty 200",
            "NSE:NIFTY50TR1XINV-INDEX": "Nifty50 TR 1x Inverse",
            "NSE:NIFTYCPSE-INDEX": "Nifty CPSE",
            "NSE:NIFTYMIDLIQ15-INDEX": "Nifty Midcap Liquid 15",
            "NSE:NIFTYCOMMODITIES-INDEX": "Nifty Commodities",
            "NSE:NIFTYCONSUMPTION-INDEX": "Nifty Consumption",
            "NSE:NIFTY50DIVPOINT-INDEX": "Nifty50 Dividend Points",
            "NSE:NIFTYGROWSECT15-INDEX": "Nifty Growth Sector 15",
            "BSE:100LARGECAPTMC-INDEX": "LCTMCI",
            "BSE:DFRG-INDEX": "DFRGRI",
            "BSE:QUALITY-INDEX": "BSEQUI",
            "BSE:DIVIDENDSTABILITY-INDEX": "BSEDSI",
            "BSE:250SMALLCAP-INDEX": "SML250",
            "BSE:150MIDCAP-INDEX": "MID150",
            "BSE:ESG100-INDEX": "ESG100",
            "BSE:SNXT50-INDEX": "SNXT50",
            "BSE:SNSX50-INDEX": "SNSX50",
            "BSE:UTILS-INDEX": "UTILS",
            "BSE:GREENEX-INDEX": "GREENX",
            "BSE:SENSEX-INDEX": "SENSEX",
            "BSE:REALTY-INDEX": "REALTY",
            "BSE:PRIVATEBANKS-INDEX": "BSEPBI",
            "BSE:CDGS-INDEX": "CDGS",
            "BSE:OILGAS-INDEX": "OILGAS",
            "BSE:ENERGY-INDEX": "ENERGY",
            "BSE:POWER-INDEX": "POWER",
            "BSE:500-INDEX": "BSE500",
            "BSE:100-INDEX": "BSE100",
            "BSE:PSU-INDEX": "BSEPSU",
            "BSE:HC-INDEX": "BSE HC",
            "BSE:400MIDSMALLCAP-INDEX": "MSL400",
            "BSE:BHRT22-INDEX": "BHRT22",
            "BSE:BANKEX-INDEX": "BANKEX",
            "BSE:ALLCAP-INDEX": "ALLCAP",
            "BSE:INFRA-INDEX": "INFRA",
            "BSE:CD-INDEX": "BSE CD",
            "BSE:MIDCAP-INDEX": "MIDCAP",
            "BSE:AUTO-INDEX": "AUTO",
            "BSE:BASMTR-INDEX": "BASMTR",
            "BSE:200-INDEX": "BSE200",
            "BSE:FIN-INDEX": "FIN",
            "BSE:CG-INDEX": "BSE CG",
            "BSE:ENHANCEDVALUE-INDEX": "BSEEVI",
            "BSE:TECK-INDEX": "TECK",
            "BSE:METAL-INDEX": "METAL",
            "BSE:CARBONEX-INDEX": "CARBON",
            "BSE:MIDSEL-INDEX": "MIDSEL",
            "BSE:SME IPO-INDEX": "SMEIPO",
            "BSE:MOMENTUM-INDEX": "BSEMOI",
            "BSE:TELCOM-INDEX": "TELCOM",
            "BSE:CPSE-INDEX": "CPSE",
            "BSE:250LARGEMIDCAP-INDEX": "LMI250",
            "BSE:SMLCAP-INDEX": "SMLCAP",
            "BSE:IT-INDEX": "BSE IT",
            "BSE:INDIAMANUFACTURING-INDEX": "MFG",
            "BSE:INDSTR-INDEX": "INDSTR",
            "BSE:LOWVOLATILITY-INDEX": "BSELVI",
            "BSE:LRGCAP-INDEX": "LRGCAP",
            "BSE:IPO-INDEX": "BSEIPO",
            "BSE:FMC-INDEX": "BSEFMC",
            "BSE:SMLSEL-INDEX": "SMLSEL"
        }
        mapping = {"1010":'nse_cm' ,"1011": 'nse_fo', "1120" : 'mcx_fo' , "1210" :'bse_cm', "1012" : 'cde_fo'}
        # print(quotesData)
        wrong_symbol =[]
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
                    # print(data)

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
                elif data['s'] == 'error':
                    wrong_symbol.append(data['n'])

            return [wrong_symbol , datadict]
        else:
            return [quotesData,{}]
                

        #     print(wrong_symbol)

        #     return datadict
        # else:
        #     return quotesData
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
    'NSE:NIFTY50-INDEX',
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

]
    symbols = ['NSE:ABAN-EQ', 'NSE:AMARAJABAT-EQ', 'NSE:EMAMIPAP-EQ', 'NSE:FACT-EQ', 'NSE:GODREJCP-EQ', 'NSE:SCHAEFFLER-EQ', 'NSE:ORICONENT-EQ', 'NSE:SETFNIF50-EQ', 'NSE:BALKRISHNA-EQ', 'NSE:SHYAMCENT-EQ', 'NSE:ADANITRANS-EQ', 'NSE:FEDERALBNK-EQ', 'NSE:CONFIPET-EQ', 'NSE:SYNGENE-EQ', 'NSE:KAYA-EQ', 'NSE:NGLFINE-EQ', 'NSE:AYMSYNTEX-EQ', 'NSE:PPL-EQ', 'NSE:AARON-EQ', 'NSE:RAMASTEEL-EQ', 'NSE:AURUM-EQ', 'NSE:RADHIKAJWE-EQ', 'NSE:DGCONTENT-EQ', 'NSE:CSLFINANCE-EQ', 'NSE:FINCABLES-EQ', 'NSE:JISLJALEQS-EQ', 'NSE:SHAREINDIA-EQ', 'NSE:STEELCITY-EQ', 'NSE:FINPIPE-EQ', 'NSE:MUTHOOTCAP-EQ', 'NSE:DYCL-EQ', 'NSE:AXISBNKETF-EQ', 'NSE:LUPIN-EQ', 'NSE:MCDOWELL-N-EQ', 'NSE:SATIN-EQ', 'NSE:ARVSMART-EQ', 'NSE:POWERMECH-EQ', 'NSE:RAMRAT-EQ', 'NSE:MOHEALTH-EQ', 'NSE:UTINIFTETF-EQ', 'NSE:KOTAKCONS-EQ', 'NSE:UTISENSETF-EQ', 'NSE:UFLEX-EQ', 'NSE:SHARDAMOTR-EQ', 'NSE:NAVKARCORP-EQ', 'NSE:RAMAPHO-EQ', 'NSE:NIFTYBEES-EQ', 'NSE:KRBL-EQ', 'NSE:MPSLTD-EQ', 'NSE:MARKSANS-EQ', 'NSE:TCI-EQ', 'NSE:ICICIMOM30-EQ', 'NSE:SHREEPUSHK-EQ', 'NSE:LOYALTEX-EQ', 'NSE:GUJGASLTD-EQ', 'NSE:BHARTIARTL-EQ', 'NSE:HDFCNEXT50-EQ', 'NSE:HDFCNIF100-EQ', 'NSE:ASAL-EQ', 'NSE:OLECTRA-EQ', 'NSE:PONNIERODE-EQ', 'NSE:PNB-EQ', 'NSE:KOTAKMNC-EQ', 'NSE:NIFTYQLITY-EQ', 'NSE:MOMENTUM-EQ', 'NSE:SURANAT&P-EQ', 'NSE:TIMESGTY-EQ', 'NSE:ICICIINFRA-EQ', 'NSE:INDIAMART-EQ', 'NSE:FOSECOIND-EQ', 'NSE:SPORTKING-EQ', 'NSE:OFSS-EQ', 'NSE:UNIONBANK-EQ',    'NSE:ADANIPORTS-EQ',
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
    'NSE:NIFTY50-INDEX',
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
    ]

    # symbols = ['NSE:FINNIFTY-INDEX'  ,
    # 'NSE:TITAN-EQ',
    # 'NSE:ULTRACEMCO-EQ',
    # ]
    client_id = "XC4EOD67IM-100"
    access_token=  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODYyODYxMzQsImV4cCI6MTY4NjM1NzA1NCwibmJmIjoxNjg2Mjg2MTM0LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2dxODJKU1ljcTNyeXVMQkU1V21aUzJkRzZjWWhVaHg3MW9pWWxJVnMwRC1ncHVWaGZfWjdwZ0I5VFIwdHZlc18xT0ptUHV6ZG1pMHM1ckV2WEFOYWkzYmtnNER0OUMzSXhYSF9iOEhSaFB5S1lsND0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.wty6GXA27EZNTZtk_dWiPKr8BA2B4MwJg-uvepymJzg"

    # access_token ="3fd5caefeb662931c6560cf5991b55e327f33ddf8ca0b2a1b0ed7165"
    # datadict = symbol_name(symbols)
    # symbols = ['NSE:BHARTIARTL-EQ',"BSE:100LARGECAPTMC-INDEX",]
    def custom_message(msg):
        # print(msg[0]["ltp"])
        print (f"Customqwdaaseaev:{msg}") 
    # if len(msg) > 1:
    client = FyersHsmSocket(access_token)
    # client.error_data = custom_message
    # connect_task = asyncio.create_task(client.subscribe(symbols,'SymbolUpdate'))
    # await asyncio.sleep(10)
    symbols = [    'NSE:IRFC-EQ',
    'NSE:IDEA-EQ',
    'NSE:TATACOMM-EQ',
    'NSE:ZOMATO-EQ',
    'NSE:PNB-EQ',
    'NSE:BFINVEST-EQ',
    ]
    connect_task = asyncio.create_task(client.subscribe(symbols,'depthUpdate', channel=2))
    # # # connect_task = asyncio.create_task(client.channesl_pause_msg())
    await asyncio.sleep(5)
    symbols = [    'NSE:USDINR23609FUT',    'NSE:NIFTYPHARMA-INDEX',]
    connect_task = asyncio.create_task(client.subscribe(symbols,'SymbolUpdate',channel=3))
    # # await asyncio.sleep(10)
    # # await fyers.close()
    # print('---------------------------------',list(datadict.keys())[:35])
    # await client.unsubscription_msg(symbols[:50])

    # await client.close()
    await connect_task

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
asyncio.run(main())
symbols =[    'NSE:NIFTYBANK-INDEX',
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
    'NSE:ADANIPRTS-EQ',
    'NSE:ASIANPAINT-EQ'   'NSE:NIFTYMIDCAP150-INDEX',
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
symbols = ['NSE:FINNIFTY-INDEX']
client_id = "XC4EOD67IM-100"
access_token=  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODYwMjUyMTgsImV4cCI6MTY4NjA5NzgxOCwibmJmIjoxNjg2MDI1MjE4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2ZyUUNYQ1ctaWR0bE1HZ05RQTFtdVRwdmhCbWxKSHl0T3NMVHlxLW42ZURtYS1ldndqQUN2TTB2cG1WX0UtSmZfMnNWSEVMYVR3cUFSZkZjTDh6b3phWFh1NTBCd1M3UWhHZUNaUUt0Z2dhOG51UT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.6Myh68174ZB05aedLIRf62xDq7HRYV4xgRIxTm2fCig"


# quotes = SymbolConverstion(access_token,symbols,'orderUpdate')
# symbol_token = quotes.symbol_to_token()[0]
# error_msg = {}
# if 's' in symbol_token and symbol_token['s'] == 'error':
#     # serror_flag = True
#     error_msg['code'] = -1600
#     error_msg['s'] = 'error'
#     error_msg['message'] = 'Could not authenticate the user '
#     print(error_msg)
# elif type(symbol_token) == list:

#     error_msg['code'] = -300
#     error_msg['s'] = 'error'
#     error_msg['message'] = 'Please provide a valid symbol'
#     error_msg['Wrong_symbols'] = symbol_token

#     print(error_msg)




    # def check_auth_and_symbol(self):

    #     conv = SymbolConverstion(self.access_token, self.symbols, self.datatype)
    #     error_msg = {}
    #     self.symbol_token = conv.symbol_to_token()
    #     if 's' in self.symbol_token[0] and self.symbol_token[0]['s'] == 'error':
    #         self.error_flag = True
    #         error_msg['code'] = -1600
    #         error_msg['s'] = 'error'
    #         error_msg['message'] = 'Could not authenticate the user '
    #         print(error_msg)
    #     elif type(self.symbol_token[0]) == list:
    #         error_msg['code'] = -300
    #         error_msg['s'] = 'error'
    #         error_msg['message'] = 'Please provide a valid symbol'
    #         error_msg['symbols'] = self.symbol_token[0]
    #         print(error_msg)
    #     return self.symbol_token[1]