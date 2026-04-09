import streamlit as st
import subprocess
import pandas as pd
from datetime import datetime

base_dir = "/home/rajkumar/Documents/code_stock_alert_VRZ/stock_picking/Dev/tvdatafeed_lib/"

st.title("📊 Nifty 50 Stocks BOF Dashboard")


#--------------------- Notifier CODE  -------------
import pandas as pd
import time
import subprocess
from nsepython import nse_eq

import asyncio
from telegram.error import TelegramError
from telegram import Bot, error

sector_files = {
    "NIFTY50_STOCKS": base_dir + "nifty50_fractal_levels_30min.csv",
    # "NIFTY_BANK" : base_dir + "niftybank_fractal_levels_1day.csv",
    # "NIFTY FMCG": base_dir + "niftyfmcg_fractal_levels_1day.csv",
    # "NIFTY_IT" : base_dir + "niftyit_fractal_levels_1day.csv",
    # "NIFTY_MEDIA" : base_dir + "niftymedia_fractal_levels_1day.csv",
    # "NIFTY_METAL" : base_dir + "niftymetal_fractal_levels_1day.csv",
    # "NIFTY_PHARMA" : base_dir + "niftypharma_fractal_levels_1day.csv",
    # "NIFTY_REALITY" : base_dir + "niftyrealty_fractal_levels_1day.csv",
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

def monitor_sector_wise():

    final_message = ""
    data_list = []
    for sector_name, file in sector_files.items():

        upside_bo_msg_list = []
        downside_bo_msg_list = []
        upside_symb = []
        downside_symb = []

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
                upside_symb.append(symbol)

            elif price >= resistance:
                msg = f"""  <b> {symbol} </b> - crossed <b> HIGH </b> price of {resistance} \n """
                downside_bo_msg_list.append(msg)
                downside_symb.append(symbol)

        total = len(upside_bo_msg_list) + len(downside_bo_msg_list)

        # Build sector summary
        sector_summary = f""" \n\n
                    <b>{sector_name}</b> 
                    Total: {total}  Low: {len(upside_bo_msg_list)} High: {len(downside_bo_msg_list)} 
                    """ + """ \n ======Low Breakout====== \n """ + "\n".join(upside_bo_msg_list) + \
                         """ \n ======High Breakout====== \n""" + "\n".join(downside_bo_msg_list)

        msg_summary = f""" \n **=Low Breakout==** \n """ + \
                      "\n".join(upside_symb) + \
                         """ \n **=High Breakout=** \n""" + \
                      "\n".join(downside_symb)

        final_message += sector_summary
        sect_dict = {"name": sector_name, 'tot': total, "high": len(downside_bo_msg_list),
                     "low": len(upside_bo_msg_list), 'msg':msg_summary}
        data_list.append((sect_dict))
    #final_message += tt

    asyncio.run(tgmain(final_message))
    return data_list

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


# ---------------- BUTTONS ----------------

if st.button("Fetch 30 Minute Data"):
    st.write("Running data fetch 30 minute...")
    subprocess.run(["python3", base_dir + "30min_nifty_50_TVDATAFeed.py"])
    st.success("Data updated!")

if st.button("Run Notifier"):
    st.write("Running notifier...")
    # subprocess.run(["python3", base_dir+"notifier_sector_wise.py"])
    out_msg = monitor_sector_wise()
    st.success("Notification sent!")
    #st.write(out_msg)
    for i in out_msg:
        # st.write("\n")
        # Header bar
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader(i['name'])
        with col2:
            now = datetime.now()
            formatted_time = now.strftime("%H:%M:%S")
            st.success("Updated on: {} ".format(formatted_time), icon=None)
        # Metric cards section
        col1, col2, col3, col4 = st.columns(4, gap="small")

        with col1:
            st.success("""
            ### Total
            # {}
            """. format(i['tot']), icon=None)

        with col2:
            with st.container(border=True):
                st.subheader("High")
                st.title(":red[{}]".format(i['high']))

        with col3:
            with st.container(border=True):
                st.subheader("Low")
                st.title(":green[{}]".format(i['low']))

        with col4:
            # with st.container(border=True):
                st.success(i['msg'], icon=None)
