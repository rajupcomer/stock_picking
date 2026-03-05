import yfinance as yf
import pandas as pd

# ---------------------------
# Download 30-minute data
# ---------------------------
symbol = "RELIANCE.NS"

df = yf.download(
    symbol,
    interval="30m",
    period="5d"   # last 5 days data
)

df = df.dropna()

# ---------------------------
# Fractal Calculation
# ---------------------------

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

# ---------------------------
# Extract Levels
# ---------------------------

fractal_highs = df[df['Fractal_High']]
fractal_lows = df[df['Fractal_Low']]

print("\nFractal Highs:")
print(fractal_highs[['High']])

print("\nFractal Lows:")
print(fractal_lows[['Low']])
