import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd 

df = pd.read_excel("riska.xlsx")
df = df.fillna(0)
df["Repayment_amount"] = df['Repayment_amount'].astype(int)
Data = dict(zip(df['Collector'],df['Repayment_amount']))

nama = list(Data.keys())
values = list(Data.values())

plt.figure(figsize=(16, 12))

plt.barh(nama, values, color='teal') #color(red, pink, blue, green, cyan, black, yellow, orange, teal, aqua, lime, brown)

today = datetime.today().strftime('%d %B %Y')

plt.title(f"Report Daily {today} ( Target Rp 7.000.000 )", loc='center')
plt.xlabel("Repayment_amount (in units)")
plt.ylabel("Collector")

plt.xlim(0,max(values)* 1.1)

max_val = max(values)
for ninja, samurai in enumerate(values):
    if samurai > 0:

        threshold = max_val * 0.08

        if samurai >= threshold:
            plt.text(samurai - (max_val*0.01), ninja, f"Rp {samurai:,}", va='center', fontsize=10, ha='right', color='black')
        else:
            plt.text(samurai + (max_val*0.1), ninja, f"Rp {samurai:,}", va='center', fontsize=12, ha='right', color='black')

plt.subplots_adjust(left=0.35, right=0.95,bottom=0.05)
plt.tight_layout()
plt.savefig("grafik_bar_daily_payment.png", dpi=100)
plt.show()

df = pd.read_excel("risnur.xlsx")
df = df.fillna(0)

df["Recovery rate float"] = (
    df['Recovery rate']
    .astype(str)
    .str.replace(',', '.')
    .str.replace('%', '')
    .astype(float)
    )

df["Recovery rate str"] = df["Recovery rate float"].map(lambda x: f"{x:.3f}")

df["Label"] = df["Team"] + "("+ df["Recovery rate str"] + ")"

team = df["Label"].tolist()
rate = df["Recovery rate float"].tolist()

plt.figure(figsize=(8, 8))
today = datetime.today().strftime('%d %B %Y')

plt.title(f"Report Cycle S2 {today} ( Target 12.52% )", loc='center')

plt.pie(rate, labels=team, autopct='%1.2f%%', startangle=140, colors=plt.cm.tab20.colors)
plt.axis('equal') 
plt.tight_layout()
plt.savefig("grafik_Cycle_S2.png", dpi=100)
plt.show()

df = pd.read_excel("nurlita.xlsx")
df = df.fillna(0)
df["Pending Amount Recovery"] = df['Pending Amount Recovery'].astype(float)
Monthly = dict(zip(df['Collector'],df['Pending Amount Recovery']))

bulan = list(Monthly.keys())
hasil = list(Monthly.values())

plt.figure(figsize=(16, 12))
plt.barh(bulan, hasil, color='orange') #color(red, pink, blue, green, cyan, black, yellow, orange, teal, aqua, lime, brown)

plt.title("Report Mohtnly September 2025")
plt.xlabel("Pending Amount Recovery(in unit)")
plt.ylabel("Collector")

plt.xlim(0,max(hasil)* 1.2)

def format_number(lagos):
    return f"{lagos:.2f}".rstrip('0').rstrip('.') if isinstance(lagos, float) else str(lagos)

max_month = max(hasil)
for lagos, kilimanjaro in enumerate(hasil):
    if kilimanjaro > 0:
        threshold = max_month * 0.08
        label = format_number(kilimanjaro)

        if kilimanjaro > threshold:
            plt.text(kilimanjaro - (max_month*0.05), lagos, label, va='center', ha='left', color='black', fontsize=10, fontweight='bold')
        else:
            plt.text(kilimanjaro + (max_month*0.05), lagos, label, va='center', ha='left', color='black', fontsize=10, fontweight='bold')

plt.subplots_adjust(left=0.25, right=0.95, bottom=0.05)
plt.tight_layout()
plt.savefig("grafik_Monthly_Agustus.png", dpi=100)
plt.show()

Target = 7237417 
total_payment = 0
total_average = 0.0
average_result = 0

print("\n--------------------------------------------------------------------")
print("REPORT TEAM S2")
print(f"Target Daily : Rp {Target}")
print()

for name, payment in Data.items():
    status = "belum target" if payment<= Target else "Target"
    print(f"{name:<25}: Rp {payment:<18} {status}")

    total_payment += payment

highest_name = max(Data, key=Data.get)
highest_Payment = Data[highest_name]

print()
print(f"Total pembayaran hari ini : Rp {total_payment}")
print()
print(f"Pembayaran tertinggi: {highest_name} : Rp {highest_Payment}")
print("\n--------------------------------------------------------------------")

# Paid amount dan Total amount masih di isi manual.
Tim = {"Hansyah_s2l" : {f"Daily paid": total_payment, "Paid amount": 171981376, "Total amount": 3318720615 }}

print("PAYMENT TEAM S2 AGUSTUS")
print()
for hans, Tim in Tim.items():
    print(f"{hans}:")
    for key, value in Tim.items():
        print(f"    {key:<14}: Rp {value} ")

    print()

print("--------------------------------------------------------------------")
print("MONTHLY RECOVERY S2")
print()
print("Target 12.52%")
print()

for exe, paid in Monthly.items():
    print(f"{exe:<25}: {paid:<25}")

    total_average += paid

average_result = total_average / len(Monthly)

print()
print(f"Average Team : {average_result:.2f} %")
print("--------------------------------------------------------------------")

    

