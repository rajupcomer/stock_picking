from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

tv = TvDatafeed()
base_dir = "/home/rajkumar/Documents/code_stock_alert_VRZ/stock_picking/Dev/tvdatafeed_lib/sector_wise_price_notifier/"
# -----------------------------
# sector Index  SYMBOLS
# -----------------------------

sector_map ={
"niftyauto" : [
    "ASHOKLEY","BAJAJ-AUTO","BHARATFORG","BOSCHLTD","EICHERMOT",
    "EXIDEIND","HEROMOTOCO","M&M","MARUTI","MOTHERSON",
    "SONACOMS","TVSMOTOR","TMPV","TIINDIA","UNOMINDA"
],
"niftybank" : [
    "AUBANK","AXISBANK","BANKBARODA","CANBK","FEDERALBNK",
    "HDFCBANK","ICICIBANK","IDFCFIRSTB","INDUSINDBK","KOTAKBANK",
    "PNB","SBIN","UNIONBANK","YESBANK"
],
"niftyfmcg"  : [
    "BRITANNIA","COLPAL","DABUR","EMAMILTD","GODREJCP",
    "HINDUNILVR","ITC","MARICO","NESTLEIND","PATANJALI",
    "RADICO","TATACONSUM","UBL","UNITDSPR","VBL"
],
"niftyit" : [
    "COFORGE","HCLTECH","INFY","LTM","MPHASIS",
    "OFSS","PERSISTENT","TCS","TECHM","WIPRO"
],
"niftymedia" : [
    "DBCORP","HATHWAY","NAZARA","NETWORK18","PVRINOX",
    "PFOCUS","SAREGAMA","SUNTV","TIPSMUSIC","ZEEL"
],
"niftymetal" : [
    "APLAPOLLO","ADANIENT","HINDALCO","HINDCOPPER","HINDZINC",
    "JSWSTEEL","JSL","JINDALSTEL","LLOYDSME","NMDC",
    "NATIONALUM","SAIL","TATASTEEL","VEDL","WELCORP"
],
"niftypharma" : [
    "ABBOTINDIA","AJANTPHARM","ALKEM","AUROPHARMA","BIOCON",
    "CIPLA","DIVISLAB","DRREDDY","GLAND","GLENMARK",
    "IPCALAB","JBCHEPHARM","LAURUSLABS","LUPIN","MANKIND",
    "PPLPHARMA","SUNPHARMA","TORNTPHARM","WOCKPHARMA","ZYDUSLIFE"
],
"niftyrealty" : [
    "ANANTRAJ","BRIGADE","DLF","GODREJPROP","LODHA",
    "OBEROIRLTY","PHOENIXLTD","PRESTIGE","SIGNATURE","SOBHA"
] }


# -----------------------------
# FRACTAL DETECTION
# -----------------------------
def calculate_fractals(df):

    df['fractal_high'] = (
        (df['high'] > df['high'].shift(1)) &
        (df['high'] > df['high'].shift(2)) &
        (df['high'] > df['high'].shift(-1)) &
        (df['high'] > df['high'].shift(-2))
    )

    df['fractal_low'] = (
        (df['low'] < df['low'].shift(1)) &
        (df['low'] < df['low'].shift(2)) &
        (df['low'] < df['low'].shift(-1)) &
        (df['low'] < df['low'].shift(-2))
    )

    return df


# -----------------------------
# UNMITIGATED LEVEL LOGIC
# -----------------------------
def get_unmitigated_levels(df):

    fractal_highs = df[df['fractal_high']]
    fractal_lows = df[df['fractal_low']]

    resistance = None
    support = None

    # check resistance
    for idx in fractal_highs.index[::-1]:

        level = df.loc[idx, 'high']
        future = df.loc[idx:]

        if future['high'].max() <= level:
            resistance = level
            break

    # check support
    for idx in fractal_lows.index[::-1]:

        level = df.loc[idx, 'low']
        future = df.loc[idx:]

        if future['low'].min() >= level:
            support = level
            break

    return support, resistance

def generate_sector_csv(symbols, filename):

    results = []

    for symbol in symbols:

        try:
            print("Scanning:", symbol)

            df = tv.get_hist(
                symbol=symbol,
                exchange="NSE",
                interval=Interval.in_daily,
                n_bars=300
            )

            if df is None or df.empty:
                continue

            df = calculate_fractals(df)

            support, resistance = get_unmitigated_levels(df)

            results.append({
                "Symbol": symbol,
                "Support": support,
                "Resistance": resistance
            })

            time.sleep(0.5)

        except Exception as e:
            print(symbol, "error:", e)

    result_df = pd.DataFrame(results)
    result_df.to_csv(filename, index=False)

    print(f"\nSaved to {filename}")

for sector_name, symbols in sector_map.items():

    file_name = base_dir + f"{sector_name}_fractal_levels_1day.csv"

    print(f"\n📊 Processing {sector_name}...")

    generate_sector_csv(symbols, file_name)