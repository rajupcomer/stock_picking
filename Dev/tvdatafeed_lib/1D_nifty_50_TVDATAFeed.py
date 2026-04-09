from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import time

tv = TvDatafeed()

# -----------------------------
# NIFTY 50 SYMBOLS
# -----------------------------
nifty50 = [
"RELIANCE","TCS","HDFCBANK","ICICIBANK","INFY","ITC","LT","SBIN","BHARTIARTL",
"KOTAKBANK","AXISBANK","ASIANPAINT","MARUTI","HCLTECH","SUNPHARMA","TITAN",
"ULTRACEMCO","NESTLEIND","BAJFINANCE","WIPRO","ONGC","NTPC","POWERGRID","M&M",
"TMPV","TECHM","INDUSINDBK","ADANIENT","ADANIPORTS","COALINDIA","GRASIM",
"JSWSTEEL","HINDALCO","EICHERMOT","HEROMOTOCO","BRITANNIA","DIVISLAB","DRREDDY",
"CIPLA","BAJAJFINSV","APOLLOHOSP","BPCL","SHREECEM","TATASTEEL","UPL",
"SBILIFE","HDFCLIFE","ICICIPRULI","BAJAJ_AUTO","HINDUNILVR"
]

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


# -----------------------------
# MAIN SCANNER
# -----------------------------
results = []

for symbol in nifty50:

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


# -----------------------------
# SAVE CSV
# -----------------------------
result_df = pd.DataFrame(results)

result_df.to_csv("nifty50_fractal_levels_1day.csv", index=False)



print("\nSaved to nifty50_fractal_levels.csv")
