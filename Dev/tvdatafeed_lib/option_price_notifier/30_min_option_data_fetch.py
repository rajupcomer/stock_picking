from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import time

tv = TvDatafeed()

# -----------------------------
# NIFTY 50 SYMBOLS
# -----------------------------
niftyCE = [
"NIFTY260428C23000",
"NIFTY260428C23100",
"NIFTY260428C23200",
"NIFTY260428C23300",
"NIFTY260428C23400",
"NIFTY260428C23500",
"NIFTY260428C23600",
"NIFTY260428C23700",
"NIFTY260428C23800",
"NIFTY260428C23900",
"NIFTY260428C24000",
"NIFTY260428C24100",
"NIFTY260428C24200",
"NIFTY260428C24300",
"NIFTY260428C24400",
"NIFTY260428C24500",
"NIFTY260428C24600",
"NIFTY260428C24700",
"NIFTY260428C24800",
"NIFTY260428C24900",
"NIFTY260428C25000"
]

niftyPE = [
"NIFTY260428P23000",
"NIFTY260428P23100",
"NIFTY260428P23200",
"NIFTY260428P23300",
"NIFTY260428P23400",
"NIFTY260428P23500",
"NIFTY260428P23600",
"NIFTY260428P23700",
"NIFTY260428P23800",
"NIFTY260428P23900",
"NIFTY260428P24000",
"NIFTY260428P24100",
"NIFTY260428P24200",
"NIFTY260428P24300",
"NIFTY260428P24400",
"NIFTY260428P24500",
"NIFTY260428P24600",
"NIFTY260428P24700",
"NIFTY260428P24800",
"NIFTY260428P24900",
"NIFTY260428P25000"
]
nifty50 = niftyCE + niftyPE
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
            interval=Interval.in_30_minute,
#            interval=Interval.in_daily,
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

base_dir = "/home/rajkumar/Documents/code_stock_alert_VRZ/stock_picking/Dev/tvdatafeed_lib/option_price_notifier/"
result_df.to_csv(base_dir+"option_fractal_levels_30min.csv", index=False)
#result_df.to_csv("nifty50_fractal_levels_1day.csv", index=False)



print("\nSaved to option_fractal_levels.csv")
