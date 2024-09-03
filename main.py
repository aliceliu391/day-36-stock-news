import requests
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Keys and info for the various APIs
STOCK_API = "INSERT HERE"
NEWS_API = "INSERT HERE"
ACCOUNT_SID = "INSERT HERE"
AUTH_TOKEN = "INSERT HERE"


def get_date(n):
    """Gets the date n days ago"""
    date = (today - timedelta(days=n)).date()
    return date


# Getting the dates of the two most recent business days
today = datetime.now()
yesterday = get_date(1)
day_before_yesterday = get_date(2)

# Making sure not to get the date of a weekend
if yesterday.weekday() == 6:
    yesterday = get_date(3)
    day_before_yesterday = get_date(4)
elif yesterday.weekday() == 0:
    day_before_yesterday = get_date(4)

# Getting the stock information for the relevant stock
parameters = {
    "from": day_before_yesterday,
    "to": yesterday,
    "apikey": STOCK_API,
}

response = requests.get(url=f"https://financialmodelingprep.com/api/v3/historical-chart/4hour/{STOCK}",
                        params=parameters)
response.raise_for_status()
stock_data = response.json()

# Closing numbers
yesterday_close = stock_data[0]["close"]
day_before_yesterday_close = stock_data[2]["close"]
percentage_diff = (abs(yesterday_close - day_before_yesterday_close) / day_before_yesterday_close) * 100
print(yesterday_close, day_before_yesterday_close, percentage_diff)


if yesterday_close > day_before_yesterday_close:
    increase = True
else:
    increase = False

# If there is a considerable difference in stock price, send a message to user to inform them of the reason(s) behind it
if percentage_diff >= 5:

    # Getting news about the relevant stock
    to_date = get_date(30)
    parameters2 = {
        "q": COMPANY_NAME,
        "from": to_date,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API,

    }
    response2 = requests.get(url=f"https://newsapi.org/v2/everything", params=parameters2)
    response2.raise_for_status()

    news_data = response2.json()["articles"][:3]
    news_list = [f"Headline:{article["title"]}\nBrief:{article["description"]}" for article in news_data]

    # Sending an SMS message with the news articles
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    for news in news_list:
        if increase:
            message = client.messages.create(
                from_='YOUR_PHONE',
                body=f"{STOCK}: 🔺{round(percentage_diff, 1)}%\n{news}",
                to='YOUR_PHONE'
            )
            print(message.status)
        else:
            message = client.messages.create(
                from_='YOUR_PHONE',
                body=f"{STOCK}: 🔺{round(percentage_diff, 1)}%\n{news}",
                to='YOUR_PHONE'
            )
            print(message.status)
