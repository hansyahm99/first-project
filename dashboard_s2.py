import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ------------------- SETUP -------------------
st.set_page_config(page_title="Dashboard S2", layout="wide")
st.title("📊 Dashboard Report S2")

today = datetime.today().strftime('%d %B %Y')

# ===================== DAILY REPORT =====================
st.header(f"📅 Report Daily - {today}")
df_daily = pd.read_excel("riska.xlsx")[['Collector', 'Repayment_amount']].fillna(0)
df_daily["Repayment_amount"] = (
    df_daily['Repayment_amount'].astype(str)
    .str.replace(',', '')
    .str.replace('.00', '')
    .astype(int)
)

Data = dict(zip(df_daily['Collector'], df_daily['Repayment_amount']))
nama = list(Data.keys())
values = list(Data.values())

# Bar Chart
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.barh(nama, values, color='teal')
ax1.set_title(f"Report Daily {today} (Target Rp 7.000.000)", fontweight='bold')
ax1.set_xlim(0, max(values)*1.1)
ax1.set_xlabel("Repayment Amount")
ax1.get_xaxis().set_visible(False)
ax1.set_ylabel("Collector")

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)

max_val = max(values)
for i, val in enumerate(values):
    if val > 0:
        threshold = max_val * 0.08
        if val >= threshold:
            ax1.text(val - (max_val*0.01), i, f"Rp {val:,}", va='center', fontsize=6, ha='right', color='black')
        else:
            ax1.text(val + (max_val*0.1), i, f"Rp {val:,}", va='center', fontsize=8, ha='right', color='black')

ax1.invert_yaxis()

df_daily.index = df_daily.index + 1
st.pyplot(fig1)
st.dataframe(df_daily.rename(columns={"Repayment_amount": "Repayment Amount"}))

# ===================== CYCLE REPORT =====================
st.header(f"🔁 Report Cycle S2 - {today}")
df_cycle = pd.read_excel("riskuy.xlsx")[['Team', 'Recovery rate']].fillna(0)

df_cycle["Recovery rate float"] = (
    df_cycle['Recovery rate']
    .astype(str)
    .str.replace(',', '.')
    .str.replace('%', '')
    .astype(float)
)

df_cycle["Recovery rate str"] = df_cycle["Recovery rate float"].map(lambda x: f"{x:.3f}")
df_cycle["Label"] = df_cycle["Team"] + " (" + df_cycle["Recovery rate str"] + "%)"
team = df_cycle["Label"].tolist()
rate = df_cycle["Recovery rate float"].tolist()

# Pie Chart
fig2, ax2 = plt.subplots(figsize=(2.5, 2.5), dpi=200)
pacthes, texts, autotexts = ax2.pie(rate, autopct='%1.2f%%', startangle=140, colors=plt.cm.tab20.colors, textprops={'fontsize': 6})
ax2.set_title(f"Cycle S2 Recovery Rate (Target: 0.12)", fontsize= 7,  fontweight='bold')
ax2.axis('equal')

ax2.legend(pacthes, team, loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=6, ncol=3)

df_cycle.index = df_cycle.index + 1
st.pyplot(fig2)
st.dataframe(df_cycle[['Team', 'Recovery rate']])

# ===================== MONTHLY REPORT =====================
st.header("📆 Report Monthly - September 2025")
df_monthly = pd.read_excel("nurlita.xlsx")[['Collector', 'Pending Amount Recovery']].fillna(0)
df_monthly = df_monthly[df_monthly['Collector'] != 'Hansyah Martha Kusuma D']
df_monthly["Pending Amount Recovery"] = df_monthly['Pending Amount Recovery'].astype(float)

Monthly = dict(zip(df_monthly['Collector'], df_monthly['Pending Amount Recovery']))
bulan = list(Monthly.keys())
hasil = list(Monthly.values())

# Bar Chart
fig3, ax3 = plt.subplots(figsize=(12, 6))
ax3.barh(bulan, hasil, color='orange')
ax3.set_title("Monthly Pending Recovery (Target: 12.52%)", fontweight='bold')
ax3.set_xlabel("Pending Amount Recovery")
ax3.get_xaxis().set_visible(False)
ax3.set_ylabel("Collector")
ax3.set_xlim(0, max(hasil)*1.2)

for spine in ax3.spines.values():
    spine.set_visible(False)

def format_number(val):
    return f"{val:.2f}%".rstrip('0').rstrip('.') if isinstance(val, float) else str(val)

max_month = max(hasil)
for i, val in enumerate(hasil):
    if val > 0:
        label = format_number(val)
        if val > 1:
            ax3.text(val - 0.3, i, label, va='center', ha='right', fontsize=10, color='black')
        else:
            ax3.text(val + 0.3, i, label, va='center', ha='right', fontsize=10, color='black')

ax3.invert_yaxis()

df_monthly.index = df_monthly.index + 1
st.pyplot(fig3)
st.dataframe(df_monthly)

#====================== RANK AGENT ==================
st.header(f"🔁 Report Cycle S2 - {today}")
df_rank = pd.read_excel("risnur.xlsx")[['Team', 'Collector', 'Monthly Pending Total(Rp)', 'Repayment', 'Recovery rate']].fillna(0)

df_rank['_sort_rate']= (
    df_rank['Recovery rate']
    .astype(str)
    .str.replace(',', '.')
    .str.replace('%', '')
    .astype(float)
)

df_rank_sorted= df_rank.sort_values(by="_sort_rate", ascending=False).drop(columns="_sort_rate")
df_rank_sorted.index = df_rank_sorted.index + 1

st.subheader("📈 Rank Agent Table (sorted by Recovery Rate)")
st.dataframe(df_rank_sorted)

# ===================== SUMMARY =====================
st.header("📌 Summary Report")

Target = 7237417 
total_payment = sum(Data.values())
highest_name = max(Data, key=Data.get)
highest_payment = Data[highest_name]

st.subheader("🎯 Daily Payment Summary")
st.write(f"**Target Harian :** Rp {Target:,}")
st.write(f"**Total Pembayaran Hari Ini :** Rp {total_payment:,}")
st.write(f"**Pembayaran Tertinggi :** {highest_name} - Rp {highest_payment:,}")

# Status Per Collector
st.write("### Status Collector and Target:")
status_data = []
for name, val in Data.items():
    status = "✅ Target" if val > Target else "❌ Belum Target"
    status_data.append({"Collector": name, "Pembayaran": val, "Status": status})

df_status = pd.DataFrame(status_data)
df_status.index = df_status.index + 1
st.dataframe(df_status)

# Monthly Recovery Summary
st.subheader("📊 Monthly Recovery Summary")
st.write("**Target Recovery :** 12.52%")
average_result = sum(hasil) / len(hasil)
st.write(f"**Rata-rata Recovery Tim :** {average_result:.2f} %")

hansyah_data = df_rank[df_rank['Team']=='Hansyah_S2l'].copy()
hansyah_data['Repayment'] = hansyah_data['Repayment'].astype(str).str.replace(',', '').astype(float)
hansyah_data['Monthly Pending Total(Rp)'] = hansyah_data['Monthly Pending Total(Rp)'].astype(str).str.replace(',', '').astype(float)
total_repayment_hansyah = hansyah_data['Repayment'].sum()
total_unpaid_hansyah = hansyah_data['Monthly Pending Total(Rp)'].sum()

st.write(f"**Total Repayment :** Rp {total_repayment_hansyah:,.0f}")
st.write(f"**Total Unpaid :** Rp {total_unpaid_hansyah:,.0f}")

