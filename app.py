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
        "Net Return (CAGR - TER)": f"{(cagr - info['TER'])*100:.2f}%",
        f"Projected TFSA ({years}Y)": f"R{tfsa_growth:,.0f}"
    })

df = pd.DataFrame(results)
st.dataframe(df)

# --- Chart 1: Projected Balances ---
fund_names = [r["ETF"] for r in results]
balances = [float(r[f"Projected TFSA ({years}Y)"].replace("R","").replace(",","")) for r in results]

fig1, ax1 = plt.subplots()
bars_balance = ax1.bar(fund_names, balances, color="skyblue")
ax1.set_ylabel("Projected Balance (R)")
ax1.set_title(f"{years}-Year TFSA Projected Balances")

# Remove bottom labels completely
ax1.set_xticks([])
ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

for bar, label in zip(bars_balance, fund_names):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height/2,
             label, ha='center', va='center', rotation=90, color='black', fontsize=8)
    ax1.text(bar.get_x() + bar.get_width()/2, height,
             f"R{height:,.0f}", ha='center', va='bottom', fontsize=8, color='blue')

st.pyplot(fig1)

# --- Chart 2: TER and Net Returns ---
ters = [float(r["TER"].replace("%","")) for r in results]
net_returns = [float(r["Net Return (CAGR - TER)"].replace("%","")) for r in results]

fig2, ax2 = plt.subplots()
x = range(len(fund_names))
width = 0.35

bars_ter = ax2.bar([i - width/2 for i in x], ters, width, label="TER (%)", color="lightgreen")
bars_net = ax2.bar([i + width/2 for i in x], net_returns, width, label="Net Return (%)", color="salmon")

ax2.set_ylabel("Percentage (%)")
ax2.set_title("TER vs Net Return")

# 🚫 Remove bottom labels completely
ax2.set_xticks([])
ax2.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

# ✅ Add ETF names inside bars + values above bars
for bar, label in zip(bars_ter, fund_names):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height/2,
             label, ha='center', va='center', rotation=90, color='black', fontsize=8)
    ax2.text(bar.get_x() + bar.get_width()/2, height,
             f"{height:.2f}%", ha='center', va='bottom', fontsize=8, color='green')

for bar, label in zip(bars_net, fund_names):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height/2,
             label, ha='center', va='center', rotation=90, color='black', fontsize=8)
    ax2.text(bar.get_x() + bar.get_width()/2, height,
             f"{height:.2f}%", ha='center', va='bottom', fontsize=8, color='red')

# Legend moved to bottom
ax2.legend(loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=2)

st.pyplot(fig2)

# --- Numeric Summary Table ---
summary_data = pd.DataFrame({
    "ETF": fund_names,
    "Projected Balance (R)": balances,
    "TER (%)": ters,
    "Net Return (%)": net_returns
})
st.subheader("Numeric Summary")
st.table(summary_data.style.format({
    "Projected Balance (R)": "R{:,.0f}",
    "TER (%)": "{:.2f}%",
    "Net Return (%)": "{:.2f}%"
}))
