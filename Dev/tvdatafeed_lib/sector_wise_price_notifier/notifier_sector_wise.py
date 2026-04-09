import pandas as pd
import time
import subprocess
from nsepython import nse_eq

import asyncio
from telegram.error import TelegramError
from telegram import Bot, error

base_dir = "/home/rajkumar/Documents/code_stock_alert_VRZ/stock_picking/Dev/tvdatafeed_lib/sector_wise_price_notifier/"

sector_files = {
    "NIFTY AUTO": base_dir + "niftyauto_fractal_levels_1day.csv",
    "NIFTY_BANK" : base_dir + "niftybank_fractal_levels_1day.csv",
    "NIFTY FMCG": base_dir + "niftyfmcg_fractal_levels_1day.csv",
    "NIFTY_IT" : base_dir + "niftyit_fractal_levels_1day.csv",
    "NIFTY_MEDIA" : base_dir + "niftymedia_fractal_levels_1day.csv",
    "NIFTY_METAL" : base_dir + "niftymetal_fractal_levels_1day.csv",
    "NIFTY_PHARMA" : base_dir + "niftypharma_fractal_levels_1day.csv",
    "NIFTY_REALITY" : base_dir + "niftyrealty_fractal_levels_1day.csv",
}

def send_notification(title, message):
    subprocess.run(['notify-send', title, message])


def get_current_price(symbol):
    try:
        data = nse_eq(symbol.upper())
        price = float(data['priceInfo']['lastPrice'])
        return price
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
    message = message_up + message_down
    asyncio.run(tgmain(message))
    return message

def monitor_sector_wise():

    final_message = ""

    for sector_name, file in sector_files.items():

        upside_bo_msg_list = []
        downside_bo_msg_list = []

        df = pd.read_csv(file)

        for _, row in df.iterrows():

            symbol = row['Symbol']
            support = row['Support']
            resistance = row['Resistance']

            price = get_current_price(symbol)
            if price is None:
                continue

            print(f"{symbol}: Current = ₹{price}, Support = ₹{support}, Resistance = ₹{resistance}")

            if price <= support:
                msg = f"""  <b> {symbol} </b> - crossed <b> LOW </b> price of {support} \n """
                upside_bo_msg_list.append(msg)

            elif price >= resistance:
                msg = f"""  <b> {symbol} </b> - crossed <b> HIGH </b> price of {support} \n """
                downside_bo_msg_list.append(msg)

        total = len(upside_bo_msg_list) + len(downside_bo_msg_list)

        # Build sector summary
        sector_summary = f""" \n\n
<b>{sector_name}</b> 
Total: {total}  Low: {len(upside_bo_msg_list)} High: {len(downside_bo_msg_list)} 
""" + """ \n ======Low Breakout====== \n """ + "\n".join(upside_bo_msg_list) + \
                         """ \n ======High Breakout====== \n""" + "\n".join(downside_bo_msg_list)

        final_message += sector_summary

    #final_message += tt

    asyncio.run(tgmain(final_message))


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
    monitor_sector_wise()
    # while True:
    #     print("\n🔄 Checking stock prices...")
    #     #monitor_stocks()
    #     monitor_sector_wise()
    #     time.sleep(300)  # wait 5 minutes

