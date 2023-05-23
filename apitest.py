import asyncio
from fyerstest.fyersApi import SessionModel, FyersModelv3
import time
import webbrowser
import sys
def api_call(token, client_id):
    # access_token = "your_access_token_from_generate_access_token_function" ## access_token from the rgenerate_access_token function
    # If you want to make asynchronous API calls then assign the below variable as True and then pass it in the functions, by default its value is False
    # is_async = True
    access_token = token
    fyers = FyersModelv3(client_id=client_id,
                         token=access_token, is_async=False)
    # data = {"symbol":"NSE:BANKNIFTY23MAY30500CE","resolution":"1","date_format":"0","range_from":"1679961600","range_to":"1680652800","cont_flag":"1"}
    # print(fyers.history(data))
    # print("")
    # print(fyers.quotes({"symbols":"NSE:ONGC-EQ,NSE:SBIN-EQ"}))
    # print("")

    # print(fyers.depth({"symbol":"NSE:SBIN-EQ","ohlcv_flag":"1"}))
    # print("")

    print(fyers.tradebook())
    # print("")

    # print(fyers.positions())
    print("")

    # print(fyers.holdings())
    # print("")

    # print(fyers.funds())
    # print("")

    # print(fyers.orderbook())
    # print("")

    # print(fyers.orderbook({'id':'23050200360880'}))
    # data = {"productType":"INTRADAY","side":1,"symbol":"NSE:IDEA-EQ","qty":1,"disclosedQty":0,"type":2,"validity":"DAY","filledQty":0,"limitPrice":0,"stopPrice":0,"offlineOrder":False}
    data = {"productType":"INTRADAY","side":-1,"symbol":"NSE:IDEA-EQ","qty":1,"disclosedQty":0,"type":2,"validity":"DAY","filledQty":0,"limitPrice":0,"stopPrice":0,"offlineOrder":False}
    # print(fyers.place_order(data))
    print(fyers.place_gttorder(data))

        # data = {"productType":"CNC","side":1,"symbol":"NSE:IDEA-EQ","qty":1,"disclosedQty":0,"type":2,"validity":"DAY","filledQty":0,"limitPrice":0,"stopPrice":0,"offlineOrder":False}
    # print(fyers.placeorder(data))
    # print(fyers.modify_orders({"id":"23050800167265", "qty":1,"limitPrice":6.50,"side":1,"type":1})) #modify instead of update
    # print(fyers.exit_positions({"id":"NSE:IDEA-EQ-INTRADAY"}))
    multi = [{"productType":"INTRADAY","side":1,"symbol":"NSE:IDEA-EQ","qty":1,"disclosedQty":0,"type":2,"LTP":6.7,"validity":"DAY","filledQty":0,"limitPrice":0,"stopPrice":0,"offlineOrder":False},
{"productType":"INTRADAY","side":1,"symbol":"NSE:IDEA-EQ","qty":1,"disclosedQty":0,"type":1,"LTP":6.75,"limitPrice":6.45,"validity":"DAY","filledQty":0,"stopPrice":0,"offlineOrder":False}]
    # print(fyers.cancel_orders({'id':'23050800168646'}))
    # print(fyers.place_basket_orders(data=multi))
    data = [
    {"id":"23050400000007", "type":1, "limitPrice": 6.22, "offlineOrder":"True"},
    {"id":"52009117325", "type":1, "limitPrice": 196, "offlineOrder":"True"}]
    # print(fyers.modify_basket_orders(data))   
    # print(fyers.get_profile())











#     print(fyers.place_basket_orders(multi))











def getauthToken(client_id, redirect_uri, response_type, scope, state, nonce):
    """
            The variable `generateTokenUrl` will have a url like
            https://uat-api.fyers.in/api/dev/generate-authcode?appId=B8PWLVH8T6&redirectUrl=https%3A%2F%2Fgoogle.com
             1. This function open this url in the browser.
             2. This will ask you to login and will ask you to approve the app if it is not approved already.
             3. Once that is done, it will redirect to a url (added while app creation) with the auth_code. The url will look like
                https://www.google.com/?auth_code=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTM1ODY2NzEsInN1YiI6ImF1dGhDb2RlIiwiYXBwX2lkIjoiQjhQV0xWSDhUNiIsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsImF1ZCI6WyJ4OjAiLCJ4OjEiLCJ4OjIiXSwidXVpZCI6ImZhOGNhYjE3ZWU4OTQzMGRhZjA1YWUxNDI2YWVkYzI4IiwiaXBBZGRyIjoiMjIzLjIzMy40Mi40NiIsImRpc3BsYXlfbmFtZSI6IkRQMDA0MDQiLCJpYXQiOjE1OTM1ODYzNzEsIm5iZiI6MTU5MzU4NjM3MX0.IMJHzQGHQgyXt_XN0AgDrMN1keR4qolFFKO6cyXTnTg&user_id=DP00404
             4. You have to take the auth_code from the url and use that token in your generate_access_token function.
    """
    appSession = SessionModel(client_id=client_id, redirect_uri=redirect_uri,
                              response_type=response_type, scope=scope, state=state, nonce=nonce)
    generateTokenUrl = appSession.generate_authcode()
    print((generateTokenUrl))
    webbrowser.open(generateTokenUrl, new=1)


def generate_access_token(auth_code, client_id, redirect_uri, secret_key, grant_type):
    """
    :param auth_code: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTM1ODY2NzEsInN1YiI6ImF1dGhDb2RlIiwiYXBwX2lkIjoiQjhQV0xWSDhUNiIsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsImF1ZCI6WyJ4OjAiLCJ4OjEiLCJ4OjIiXSwidXVpZCI6ImZhOGNhYjE3ZWU4OTQzMGRhZjA1YWUxNDI2YWVkYzI4IiwiaXBBZGRyIjoiMjIzLjIzMy40Mi40NiIsImRpc3BsYXlfbmFtZSI6IkRQMDA0MDQiLCJpYXQiOjE1OTM1ODYzNzEsIm5iZiI6MTU5MzU4NjM3MX0.IMJHzQGHQgyXt_XN0AgDrMN1keR4qolFFKO6cyXTnTg"
    :param app_id: "B8PWLVH8T6"
    :param secret_key: "575XQDKGN0"
    :param redirect_url: "https://google.com"
    :return: access_token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTM1ODgzNzMsIm5iZiI6MTU5MzU4ODM3MywiZXhwIjoxNTkzNjQ5ODEzLCJpc3MiOiJhcGkuZnllcnMuaW4iLCJzdWIiOiJhY2Nlc3MiLCJhdWQiOiJ4OjAseDoxLHg6MiIsImF0X2hhc2giOiJnQUFBQUFCZV9EcVZIZExMMTAzTVpVN1NYSkZfR2p5R3hidzMtTVVhb0VEMGI0QUVvNjFsR24tREY2OFU5cXhuNzd0UXVoOVVJalYtNm9MVXhINVFfWE1WTEJfRXpROGV2clJmUzlNUXB0Y2J5c2ltN1drWllZTT0iLCJkaXNwbGF5X25hbWUiOiJQSVlVU0ggUkFKRU5EUkEgS0FQU0UiLCJmeV9pZCI6IkRQMDA0MDQifQ.cAfrj2TxAyb8A_9DfiCb1hLIZg_mH-xvP3Ybnj3a4AE"

    1.this function takes the param and return the access_token
    2.the access_token created will be used further .(in fyersModel)]
    3. one can get the auth_code from the url generated by getauthToken function (from auth_code= ..... &user_Id=xxxxxx before &)
    """
    # import ipdb;
    # ipdb.set_trace()
    appSession = SessionModel(client_id=client_id, redirect_uri=redirect_uri,
                              secret_key=secret_key, grant_type=grant_type)
    appSession.set_token(auth_code)
    access_token = appSession.generate_token()
    return access_token



def main():

    redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
    client_id = "XC4EOD67IM-100"
    secret_key = "5O0CK73DM8"
    grant_type = "authorization_code"
    response_type = "code"
    state = "sample_state"
    nonce = "baka"
    scope = "openid"
    # getauthToken(client_id, redirect_uri,response_type,scope,state,nonce)
    auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2ODM3ODAyNzgsImV4cCI6MTY4MzgxMDI3OCwibmJmIjoxNjgzNzc5Njc4LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYVjIwOTg2Iiwib21zIjoiSzEiLCJub25jZSI6ImJha2EiLCJhcHBfaWQiOiJYQzRFT0Q2N0lNIiwidXVpZCI6IjdhZWQwYTI4YjM3ZTQ3MDc5NDdjYmNkNDQ2NTk1ZTJjIiwiaXBBZGRyIjoiMC4wLjAuMCIsInNjb3BlIjoib3BlbmlkIn0.7oCFSPr_C4Lj2O8RAnp7y8kzPYT8Z9QtoqmDyejq-uw"

    # print(generate_access_token(auth_code, client_id, redirect_uri,secret_key,grant_type))

    # access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODMwMDE4OTgsImV4cCI6MTY4MzA3MzgzOCwibmJmIjoxNjgzMDAxODk4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa1VKSXFKLTNQMl9BSXFWWFNWUlg5UXlIVW5QWlpGRnFnNG5xRkNWRzYwQU5qX0F6T2hVWmxPZmtCNUV4ak03MXBMWVlqSEpjWXBsaVpVNWpFREQ1R3JFVkt4Rmx0SzR4RDh2SERVdkZndWgwUEVGRT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.MghUuBXEV3INDwH-buwTUvJDvBQ0HS37d69nwRCE7nE"
    access_token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODQ3MzgzMjUsImV4cCI6MTY4NDgwMTgwNSwibmJmIjoxNjg0NzM4MzI1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa2F4RVZLSWZPVGVUNkZtYmw4b29wLW9sTU1JaG0waU1IOGIzZmNESlVxNjI1andudnM1LXdTTnA0RTR0TmY1aGxDWWNFUm56QXlnNWVmWFFTUVFiR0M2Y0NaMVVKN3hkc2ptZ3FMZkxOejhsa3FWZz0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.8GfqzLmubDCX-FCcjIppkzurYhz4wakgaeeD5Ryk30s"
    api_call(access_token, client_id)


if __name__ == '__main__':
    main()
