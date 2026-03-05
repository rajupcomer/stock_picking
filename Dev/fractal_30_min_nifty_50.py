import yfinance as yf
import pandas as pd

# ---------------------------------
# NIFTY 50 SYMBOLS
# ---------------------------------
nifty50 = [
    "RELIANCE.NS","TCS.NS","HDFCBANK.NS","ICICIBANK.NS","INFY.NS",
    "ITC.NS","LT.NS","SBIN.NS","BHARTIARTL.NS","KOTAKBANK.NS",
    "AXISBANK.NS","ASIANPAINT.NS","MARUTI.NS","HCLTECH.NS","SUNPHARMA.NS",
    "TITAN.NS","ULTRACEMCO.NS","NESTLEIND.NS","BAJFINANCE.NS","WIPRO.NS",
    "ONGC.NS","NTPC.NS","POWERGRID.NS","M&M.NS","TATAMOTORS.NS",
    "TECHM.NS","INDUSINDBK.NS","ADANIENT.NS","ADANIPORTS.NS","COALINDIA.NS",
    "GRASIM.NS","JSWSTEEL.NS","HINDALCO.NS","EICHERMOT.NS","HEROMOTOCO.NS",
    "BRITANNIA.NS","DIVISLAB.NS","DRREDDY.NS","CIPLA.NS","BAJAJFINSV.NS",
    "APOLLOHOSP.NS","BPCL.NS","SHREECEM.NS","TATASTEEL.NS","UPL.NS",
    "SBILIFE.NS","HDFCLIFE.NS","ICICIPRULI.NS","BAJAJ-AUTO.NS","HINDUNILVR.NS"
]

# ---------------------------------
# DOWNLOAD ALL DATA AT ONCE
# ---------------------------------
print("Downloading NIFTY50 data (single request)...")

data = yf.download(
    tickers=nifty50,
    interval="30m",
    period="5d",
    group_by="ticker",
    threads=False,      # IMPORTANT → avoids rate limit
    progress=False
)

# ---------------------------------
# FRACTAL FUNCTION
# ---------------------------------
def calculate_fractals(df):

    df['Fractal_High'] = (
        (df['High'] > df['High'].shift(1)) &
        (df['High'] > df['High'].shift(2)) &
        (df['High'] > df['High'].shift(-1)) &
        (df['High'] > df['High'].shift(-2))
    )

    df['Fractal_Low'] = (
        (df['Low'] < df['Low'].shift(1)) &
        (df['Low'] < df['Low'].shift(2)) &
        (df['Low'] < df['Low'].shift(-1)) &
        (df['Low'] < df['Low'].shift(-2))
    )

    return df


# ---------------------------------
# SCAN EACH STOCK
# ---------------------------------
results = []

for symbol in nifty50:

    try:
        df = data[symbol].dropna()

        if df.empty:
            continue

        df = calculate_fractals(df)

        highs = df[df['Fractal_High']]
        lows = df[df['Fractal_Low']]

        last_high = highs['High'].iloc[-1] if not highs.empty else None
        last_low = lows['Low'].iloc[-1] if not lows.empty else None

        results.append([symbol, last_high, last_low])

        print(f"{symbol} → High: {last_high} | Low: {last_low}")

    except Exception as e:
        print(symbol, "Error:", e)

# ---------------------------------
# SAVE TO CSV
# ---------------------------------
result_df = pd.DataFrame(results, columns=["Symbol", "FractalHigh", "FractalLow"])
result_df.to_csv("nifty50_fractals.csv", index=False)

print("\n✅ Saved to nifty50_fractals.csv")
