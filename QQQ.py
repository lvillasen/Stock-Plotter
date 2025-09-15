import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, timedelta, datetime
import numpy as np

######## Select ticker, initial date, final date, initial amount, periodic amount to invest and periodicity in week days
ticker = "QQQ.MX"
initial_date = date(2024,9,15)
final_date = date.today()
df = yf.download(ticker,initial_date,final_date, progress=False, auto_adjust=False)
df.columns = df.columns.droplevel(1)
##############################


df['SMA_20'] = df['Close'].rolling(window=20).mean()
df['STD_20'] = df['Close'].rolling(window=20).std()
df['BB_upper'] = df['SMA_20'] + 2 * df['STD_20']
df['BB_lower'] = df['SMA_20'] - 2 * df['STD_20']

df['SMA_200'] = df['Close'].rolling(window=200).mean()


fig = make_subplots(rows=1, cols=1, shared_xaxes=True,
                    vertical_spacing=0.05, subplot_titles=('OHLC con Bandas de Bollinger y SMA 200'),
                    row_width=[1])  # Volumen más pequeño en la segunda fila

fig.add_trace(go.Candlestick(
    x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
    name="OHLC"
), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=df['BB_upper'], line=dict(color='blue', width=1), name='Upper Band'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], line=dict(color='orange', width=1), name='20-Day MA'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['BB_lower'], line=dict(color='blue', width=1), name='Lower Band'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], line=dict(color='purple', width=2, dash='dot'), name='SMA 200'), row=1, col=1)




fig.update_layout(title=f"Análisis de {ticker} con Bandas de Bollinger, SMA 200 y Volumen",
                  xaxis_rangeslider_visible=False,
                  showlegend=True)

fig.show()

