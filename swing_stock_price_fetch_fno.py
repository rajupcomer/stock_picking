import yfinance as yf
import csv
from datetime import datetime, time
import time as t
import subprocess

import asyncio
from telegram.error import TelegramError
from telegram import Bot, error


# Function to fetch stock prices
def fetch_stock_prices(stock_names, live, file_name):
    
    for stock_info in stock_names:
        #print (stock_info)
        updated_rows = []
        stock_name, high_price, low_price, is_enable = stock_info
        try:
            if live:
            	stock_data = yf.download(stock_name, start=datetime.now(), end=datetime.now())
            else:
            	stock_data = yf.download(stock_name)
            if not stock_data.empty:
                print(f"Stock: {stock_name}, Price: {stock_data['Adj Close'].iloc[-1]}")
                #current_price = stock.history(period="1d")['Close'].iloc[-1]
                current_price = stock_data['Adj Close'].iloc[-1]
                
                
                is_enable = 'TRUE'
                if current_price >= float(high_price):
                    message = f"""  <b> {stock_name} </b> - Current price crossed the <b> HIGH </b> price of {high_price}  🟢 \U0001F31F """
                    send_notification(message)
                    asyncio.run(tgmain(message))
                    is_enable = 'FALSE'
                elif current_price <= float(low_price):
                    message = f""" <b> {stock_name} </b> - Current price crossed the <b> LOW </b> price of {low_price}  🟢⬆️  \U0001F31F """
                    send_notification(message)
                    asyncio.run(tgmain(message))
                    is_enable = 'FALSE'

                updated_rows.append([stock_name, high_price, low_price, is_enable])
            else:
                print(f"Stock: {stock_name}, Data not available")
                updated_rows.append([stock_name, high_price, low_price, is_enable])
                          
        except Exception as e:
            print(f"Error fetching data for {stock_name}: {e}")

    # Write the updated rows back to the CSV file, skipping the first line
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['SCRIP', 'High Price', 'Low Price', 'EnaBle'])  # Rewrite the header
        writer.writerows(updated_rows)
        file.writelines(lines[len(updated_rows)+1:])  # Write the skipped lines back to the file


# Function to read stock names from CSV file
def read_stock_names(file_name):
    stock_names = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first line
        for row in reader:
            #stock_names.extend(row)
            #print (row[3])
            if row[3] == 'TRUE':
            	stock_names.append(row)
    return stock_names

# Function to send notification
def send_notification(message):
    subprocess.Popen(['notify-send', 'Stock Alert', message])


# Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
bot_token = '7059155564:AAGT0jZsElWyAJ8ClP-8hqZTmjxC4bZR1A8'
# Replace 'YOUR_CHANNEL_ID' with your channel's username or ID (e.g., '@channelusername')
#channel_id = '@vrzonebof'
channel_id = '-1002033022952'
#channel_id = '1460012524'


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


# Main function
def main():
    # File containing stock names
    stock_file = 'swing_stock_fno_list.csv'

    # Read stock names from CSV file
    stock_names = read_stock_names(stock_file)

    # Run until 3:30 PM IST
    end_time = datetime.combine(datetime.now().date(), time(hour=15, minute=30))

    no_of_exec = 1
    while datetime.now() < end_time:
        message = f""" No of Execution for the day(Today) - {no_of_exec} """
        asyncio.run(tgmain(message))
        fetch_stock_prices(stock_names, live=True, file_name=stock_file)
        print ("\n\n===========================================")
        print ("==== Waiting for another 5 Minutes  ======")
        print ("===========================================\n\n")
        t.sleep(300)  # Wait for 5 minute before fetching again
        no_of_exec+=1
        
    print (" Market will open at 9:15 am ")
    print ("==== We will find our zone using today/yesterday closed price =====")
    fetch_stock_prices(stock_names, live=False, file_name=stock_file) 

if __name__ == "__main__":
    main()


"""  ApolloTyre  Balkrishna  """

