import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Page Configuration ---
st.set_page_config(page_title="NexusTrade Dashboard", layout="wide")

st.title("📊 NexusTrade: Digital Economy Intelligence")
st.markdown("""
*Developed by **Hamit Buyukguzel** | Inspired by Stanford Digital Economy Research.*
This dashboard provides a multi-dimensional view of market data to mitigate information asymmetry.
""")

# --- Sidebar Inputs ---
st.sidebar.header("Control Panel")
ticker = st.sidebar.text_input("Enter Asset Ticker (e.g., BTC-USD, AAPL)", "BTC-USD")
timeframe = st.sidebar.selectbox("Select Analysis Period", ["1mo", "3mo", "6mo", "1y", "max"])
technical_indicator = st.sidebar.multiselect("Overlay Indicators", ["SMA 20", "EMA 50", "Bollinger Bands"], ["SMA 20"])

# --- Data Fetching ---
@st.cache_data
def load_data(symbol, period):
    data = yf.download(symbol, period=period)
    return data

data = load_data(ticker, timeframe)

# --- Main Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Price Action & Technical Analysis: {ticker}")
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'], name="Market Price")])
    
    # Simple Moving Average Logic
    if "SMA 20" in technical_indicator:
        sma = data['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(x=data.index, y=sma, name="SMA 20", line=dict(color='orange')))
        
    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Digital Economy Insights")
    # Risk Metrics
    volatility = data['Close'].pct_change().std() * (252**0.5)
    st.metric("Annualized Volatility", f"{volatility:.2%}")
    
    st.info("**Research Note:** According to Digital Economy principles, high volatility clusters often precede shifts in platform-mediated liquidity.")
    
    # Statistical Summary
    st.write("Recent Summary Statistics")
    st.dataframe(data['Close'].tail(10).describe())

# --- Macro Correlation Section ---
st.divider()
st.subheader("🔗 Macro-Economic Correlation")
# Compare with S&P 500
spy_data = load_data("SPY", timeframe)['Close']
correlation = data['Close'].corr(spy_data)
st.write(f"Correlation with S&P 500 (Traditional Markets): **{correlation:.2f}**")

# Footer
st.markdown("---")
st.caption("Disclaimer: This tool is for educational purposes under the scope of Data Science and Digital Economics.")
