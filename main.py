import requests
import os
from twilio.rest import Client
# from datetime import date, timedelta

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_key = "***"
news_api_key = "***"

account_sid = "***"
auth_token = "***"

#today = date.today()
# yesterday = today - timedelta(days=1)
#today = str(today)
#yesterday = str(yesterday)

# Haftasonuna denk geldiği için manule vericem yada index numarasına göre denicem
#print(today)
#print(yesterday)



# Stocks API Connection
stock_params={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":stock_api_key
}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()
# print(stock_data["Time Series (Daily)"])
# print(stock_data["Time Series (Daily)"]["2022-02-25"]["4. close"])

# List Comprehention    ## hafta sonuna denk geldiği için date time üzerinden bugünü ve dünü almak yerine json verisi sıralı zaten bunu listeye çeviricem yada inde numarası atayacağım
stock_data_list = [float(value["4. close"].replace("'", "")) for (key, value) in stock_data["Time Series (Daily)"].items()] # .items dict iterable olması için gerekli

#print(stock_data_list)
#print(type(stock_data_list[0]))

percentage_diff = ((abs(stock_data_list[0]-stock_data_list[1]))/stock_data_list[0])*100 # eğer yüzde 5 den büyükse

if percentage_diff >= 1:
    print("Get News")
##################################################### News ###################################################
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": news_api_key,
        "language": "en",
        "sortBy": "publishedAt",
        "from_param": "2022-01-01"
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()

    first_three_article = news_data["articles"][:3]
    news_list = [f"Headline: {each['title']}. \n Brief: {each['description']}" for each in first_three_article]
    print(news_list)


################################################ Send Sms-Twillio#####################################################

    client = Client(account_sid, auth_token)
    for article in news_list:
        message = client.messages\
            .create(
            body=article,
            from_="+***",
            to="+***"
        )


####################################################### End ######

