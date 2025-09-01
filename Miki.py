import matplotlib.pyplot as plt

Data = {
        "Edi Supriyanto"            :1205405,
        "Annisa Putri Restu"        :2535144,
        "Riska Nurlita"             :1477195,
        "Syarla Putri Guna"         :552595,
        "Yandi Nugraha"             :601647,
        "Yolanda Oktaviani"         :595048,
        "Erick Ervan Dewanggga"     :0,
        "Azizah Rahmawati"          :0,
        "Aldi Taufik"               :677567,
        "Ika Juliasari"             :0,
        "Debora Retima Sihombing"   :1762000,
        "Romli"                     :750631,
        "Ridhoi Berkat Zebua"       :0,
        "Fadilah Damayanti"         :3039655,
        "Erlangga Hutama"           :596045,
        "Nur Halim"                 :3259599, 
        "Adistira Winditya P"       :5869259, 
        "Axl Wicaksono"             :732792
        }

nama = list(Data.keys())
values = list(Data.values())

plt.figure(figsize=(14, 10))

plt.barh(nama, values, color='orange')

plt.title("Report Daily 30 Agustus 2025")
plt.xlabel("Payment (in units)")
plt.ylabel("Name")

plt.xlim(0,max(values)* 1.1)

max_val = max(values)
for ninja, samurai in enumerate(values):
    if samurai > 0:

        threshold = max_val * 0.08

        if samurai >= threshold:
            plt.text(samurai - (max_val*0.01), ninja, f"Rp {samurai:,}", va='center', fontsize=10, ha='right', color='black')
        
        else:
            plt.text(samurai + (max_val*0.1), ninja, f"Rp {samurai:,}", va='center', fontsize=12, ha='right', color='black')

plt.subplots_adjust(left=0.3, right=0.95,bottom=0.05)
plt.tight_layout()
plt.savefig("grafik_bar_daily_payment.png", dpi=100)
plt.show()

Tim = {"Hansyah_s2l" : {f"Daily paid": 8547124, "Paid amount": 935512454, "Total amount": 9365024946 }}

Monthly = {
        "Edi Supriyanto"            :9.02,
        "Annisa Putri Restu"        :11.40,
        "Riska Nurlita"             :14.64,
        "Syarla Putri Guna"         :9.99,
        "Yandi Nugraha"             :9.31,
        "Yolanda Oktaviani"         :9.36,
        "Erick Ervan Dewanggga"     :11.02,
        "Azizah Rahmawati"          :9.61,
        "Aldi Taufik"               :7.99,
        "Ika Juliasari"             :10.00,
        "Debora Retima Sihombing"   :11.44,
        "Romli"                     :10.17,
        "Ridhoi Berkat Zebua"       :9.32,
        "Fadilah Damayanti"         :8.92,
        "Erlangga Hutama"           :7.28,
        "Nur Halim"                 :8.08, 
        "Adistira Winditya P"       :8.47, 
        "Axl Wicaksono"             :6.53
        }

bulan = list(Monthly.keys())
hasil = list(Monthly.values())

plt.figure(figsize=(14, 10))
plt.barh(bulan, hasil, color='orange')

plt.title("Report Montly Agustus 2025")
plt.xlabel("rate(in unit)")
plt.ylabel("Name")

plt.xlim(0,max(hasil)* 1.1)

max_month = max(hasil)
for riska, nurlita in enumerate(values):
    if nurlita > 0:
        plt.text(nurlita - (max_month*0.05), riska, f"{nurlita:.2f}", va='center', ha='left', color='black', fontsize=10, fontweight ='bold')
        

plt.subplots_adjust(left=0.2, right=0.95,bottom=0.05)
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
    print(f"{name:<24}: Rp {payment:<24} {status}")

    total_payment += payment

highest_name = max(Data, key=Data.get)
highest_Payment = Data[highest_name]

print()
print(f"Total pembayaran hari ini : Rp {total_payment}")
print()
print(f"Pembayaran tertinggi: {highest_name} : Rp {highest_Payment}")
print("\n--------------------------------------------------------------------")
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

for exe, paid in Monthly.items():
    print(f"{exe:<24}: {paid:<24}")

    total_average += paid

average_result = total_average / len(Monthly)

print()
print(f"Average Team : {average_result:.2f} %")
print("--------------------------------------------------------------------")
