import pandas as pd
import time
import subprocess
from nsepython import nse_eq
from tvDatafeed import TvDatafeed, Interval

import asyncio
from telegram.error import TelegramError
from telegram import Bot, error

tv = TvDatafeed()

CSV_FILE = "option_fractal_levels_30min.csv"
tt = "\n\n #30min_option_data"

def send_notification(title, message):
    subprocess.run(['notify-send', title, message])


def get_current_price(symbol):
    try:
        # print("Scanning:", symbol)
        df = tv.get_hist(
            symbol=symbol,
            exchange="NSE",
            interval=Interval.in_1_minute,
            #            interval=Interval.in_daily,
            n_bars=1
        )


        if not df.empty :
            price = float(df['close'].iloc[-1])
            return price
        # data = nse_eq(symbol.upper())
        # price = float(data['priceInfo']['lastPrice'])
        # return price
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None


def monitor_stocks():
    upside_bo_msg_list = []
    downside_bo_msg_list = []

    df = pd.read_csv(CSV_FILE)

    for _, row in df.iterrows():
        symbol = row['Symbol']
        support = row['Support']
        resistance = row['Resistance']

        price = get_current_price(symbol)
        if price is None:
            continue

        print(f"{symbol}: Current = ₹{price}, Support = ₹{support}, Resistance = ₹{resistance}")

        if price <= support:
            message = f"""  <b> {symbol} </b> - crossed <b> LOW </b> price of {support} \n """
            upside_bo_msg_list.append(message)

        elif price >= resistance:
            message = f""" <b> {symbol} </b> - crossed  <b> High </b> price of {resistance} \n """
            downside_bo_msg_list.append(message)
    total_no_of_stock = len(upside_bo_msg_list) + len(downside_bo_msg_list)
    message_up = f""" No of Execution for the day - no_of_exec  \n\n""" + \
                 """ Total Instrument = """ + str(total_no_of_stock) + \
                 """ \n Low = """ + str(len(upside_bo_msg_list)) + """\n High = """ + str(
        len(downside_bo_msg_list)) + """ \n """ \
                                     """ \n\n ======Low Breakout====== \n\n """ + "\n".join(upside_bo_msg_list)
    message_down = """ \n ======High Breakout====== \n\n""" + "\n".join(downside_bo_msg_list)
    message = message_up + message_down + tt
    asyncio.run(tgmain(message))


# Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
bot_token = '7059155564:AAGT0jZsElWyAJ8ClP-8hqZTmjxC4bZR1A8'
# Replace 'YOUR_CHANNEL_ID' with your channel's username or ID (e.g., '@channelusername')
# channel_id = '@vrzonebof'
channel_id = '-1002033022952'


# channel_id = '1460012524'


async def tgmain(message):
    # Create a bot instance
    bot = Bot(token=bot_token)

    try:
        # Send a message to the channel
        await bot.send_message(chat_id=channel_id, text=message, parse_mode='HTML')
        print("Message sent successfully!")
    except error.BadRequest as e:
        print(f"Failed to send message: {e}")
    except error.Unauthorized as e:
        print(f"Bot is not authorized to send messages to the channel: {e}")
    except error.TelegramError as e:
        print(f"Failed to send message due to Telegram error: {e}")


if __name__ == "__main__":

    while True:
        print("\n🔄 Checking Options prices...")
        monitor_stocks()
        time.sleep(300)  # wait 5 minutes

