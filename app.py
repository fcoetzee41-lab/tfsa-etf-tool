# --- Chart 1: Projected Balances ---
fig1, ax1 = plt.subplots()
fund_names = [r["ETF"] for r in results]
balances = [float(r[f"Projected TFSA ({years}Y)"].replace("R","").replace(",","")) for r in results]

bars_balance = ax1.bar(fund_names, balances, color="skyblue")
ax1.set_ylabel("Projected Balance (R)")
ax1.set_title(f"{years}-Year TFSA Projected Balances")

# Remove bottom labels
ax1.set_xticks([])

# Add vertical ETF names inside bars + values above bars
for bar, label in zip(bars_balance, fund_names):
    height = bar.get_height()
    # ETF name inside bar
    ax1.text(bar.get_x() + bar.get_width()/2, height/2,
             label, ha='center', va='center', rotation=90, color='black', fontsize=8)
    # Value above bar
    ax1.text(bar.get_x() + bar.get_width()/2, height,
             f"R{height:,.0f}", ha='center', va='bottom', fontsize=8, color='blue')

st.pyplot(fig1)

# --- Chart 2: TER and Net Returns ---
fig2, ax2 = plt.subplots()
ters = [float(r["TER"].replace("%","")) for r in results]
net_returns = [float(r["Net Return (CAGR - TER)"].replace("%","")) for r in results]

x = range(len(fund_names))
width = 0.35

bars_ter = ax2.bar([i - width/2 for i in x], ters, width, label="TER (%)", color="lightgreen")
bars_net = ax2.bar([i + width/2 for i in x], net_returns, width, label="Net Return (%)", color="salmon")

ax2.set_ylabel("Percentage (%)")
ax2.set_title("TER vs Net Return")

# Remove bottom labels
ax2.set_xticks([])

# Add vertical ETF names inside bars + values above bars
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

ax2.legend()
st.pyplot(fig2)
