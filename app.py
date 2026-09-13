import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ETF list with tickers and TERs
etfs = {
    "Satrix Top 40 (STX40.JO)": {"ticker": "STX40.JO", "TER": 0.0035},
    "Sygnia MSCI World (SYGWD.JO)": {"ticker": "SYGWD.JO", "TER": 0.0040},
    "Vanguard S&P 500 (VOO)": {"ticker": "VOO", "TER": 0.0009}
}

# Sidebar inputs
st.sidebar.header("TFSA Simulation Settings")
annual_contribution = st.sidebar.number_input("Annual Contribution (R)", value=36000, step=1000)
years = st.sidebar.slider("Investment Horizon (Years)", 5, 30, 20)
contribution_frequency = st.sidebar.selectbox("Contribution Frequency", ["Annual", "Monthly", "Quarterly"])

selected_etfs = st.sidebar.multiselect("Select ETFs", list(etfs.keys()), default=list(etfs.keys()))

# Functions
def get_etf_data(ticker):
    etf = yf.Ticker(ticker)
    hist = etf.history(period="5y")
    return hist

def calculate_cagr(hist):
    start_price = hist['Close'].iloc[0]
    end_price = hist['Close'].iloc[-1]
    years = len(hist) / 252
    cagr = ((end_price/start_price) ** (1/years) - 1)
    return cagr

def simulate_tfsa_growth(cagr, ter, annual_contribution, years, frequency):
    balance = 0
    periods = {"Annual": 1, "Quarterly": 4, "Monthly": 12}[frequency]
    contribution = annual_contribution / periods
    for y in range(years):
        for p in range(periods):
            balance = (balance + contribution) * (1 + (cagr - ter)/periods)
    return balance

# Main dashboard
st.title("ETF Comparison & TFSA Growth Simulator")

results = []
for name in selected_etfs:
    info = etfs[name]
    hist = get_etf_data(info["ticker"])
    cagr = calculate_cagr(hist)
    tfsa_growth = simulate_tfsa_growth(cagr, info["TER"], annual_contribution, years, contribution_frequency)
    results.append({
        "ETF": name,
        "CAGR (5Y)": f"{round(cagr*100,2)}%",
        "TER": f"{info['TER']*100:.2f}%",
        f"Projected TFSA ({years}Y)": f"R{tfsa_growth:,.0f}"
    })

df = pd.DataFrame(results)
st.dataframe(df)

# Chart visualization with vertical inside-bar labels
fig, ax = plt.subplots()
bars_values = [float(r[f"Projected TFSA ({years}Y)"].replace("R","").replace(",","")) for r in results]
bars = ax.bar([r["ETF"] for r in results], bars_values)

ax.set_ylabel("Projected TFSA Balance (R)")
ax.set_title(f"{years}-Year TFSA Growth Comparison")

# Add vertical ETF names inside each bar
for bar, label in zip(bars, [r["ETF"] for r in results]):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        height/2,
        label,
        ha='center', va='center',
        rotation=90,
        color='black',
        fontsize=8
    )

# Remove x-axis tick labels since names are inside bars
ax.set_xticks([])

st.pyplot(fig)
