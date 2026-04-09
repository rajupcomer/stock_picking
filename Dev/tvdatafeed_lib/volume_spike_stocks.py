from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import subprocess
import time

tv = TvDatafeed()

symbols = [
"RELIANCE","TCS","HDFCBANK","ICICIBANK","INFY","HINDUNILVR","ITC","SBIN",
"BHARTIARTL","KOTAKBANK","LT","HCLTECH","ASIANPAINT","AXISBANK","MARUTI",
"SUNPHARMA","TITAN","ULTRACEMCO","NESTLEIND","WIPRO","NTPC","POWERGRID",
"M&M","TECHM","TMPV","BAJFINANCE","BAJAJFINSV","JSWSTEEL","ONGC",
"ADANIENT","ADANIPORTS","GRASIM","COALINDIA","INDUSINDBK","DRREDDY",
"EICHERMOT","HINDALCO","BPCL","HEROMOTOCO","BRITANNIA","CIPLA","DIVISLAB",
"APOLLOHOSP","TATASTEEL","BAJAJAUTO","UPL","SBILIFE","HDFCLIFE",
"ICICIPRULI","SHREECEM"
]


def send_notification(stocks):

    count = len(stocks)

    message = "\n".join(stocks)

    subprocess.run([
        "notify-send",
        f"Nifty Volume Spike ({count})",
        message
    ])


def scan():

    alerts = []

    for stock in symbols:

        try:

            data = tv.get_hist(
                symbol=stock,
                exchange='NSE',
                interval=Interval.in_5_minute,
               # interval=Interval.in_daily,
                n_bars=25
            )

            if data is None or len(data) < 21:
                continue

            current_volume = data['volume'].iloc[-1]
            avg_volume = data['volume'].iloc[-21:-1].mean()

            if current_volume > avg_volume * 1.7:
                alerts.append(stock)

        except Exception as e:
            print(stock, "error:", e)

    if alerts:
        print (alerts)
        send_notification(alerts)


while True:

    print("Scanning Nifty50...")

    scan()

    time.sleep(300)