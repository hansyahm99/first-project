#def Team():
    #Data = {
        #"Edi": {"Daily Payment": 831944, "Recovery": 5.22},
        #"Annisa": {"Daily Payment": 0, "Recovery": 11.44},
        #"Riska": {"Daily Payment": 0, "Recovery": 14.94},
        #"Syarla": {"Daily Payment": 417535, "Recovery": 10.01},
        #"Yandi": {"Daily Payment": 0, "Recovery": 9.84},
        #"Yolanda": {"Daily Payment": 0, "Recovery": 8.85},
        #"Erick": {"Daily Payment": 1016867, "Recovery": 10.86},
        #"Azizah": {"Daily Payment": 0, "Recovery": 10.00},
        #"Aldi": {"Daily Payment": 0, "Recovery": 6.90},
        #"Ika": {"Daily Payment": 0, "Recovery": 9.60},
        #"Debora": {"Daily Payment": 2565358, "Recovery": 10.64},
        #"Romli": {"Daily Payment": 4331792, "Recovery": 9.88},
        #"Ridhoi": {"Daily Payment": 0, "Recovery": 8.35},
        #"Fadilah": {"Daily Payment": 1472732, "Recovery": 7.33},
        #"Erlangga": {"Daily Payment": 1459348, "Recovery": 6.68},
        #"Nur": {"Daily Payment": 1013743, "Recovery": 7.40},
        #"Adistira": {"Daily Payment": 0, "Recovery": 7.60},
        #"Axl": {"Daily Payment": 2142137, "Recovery": 5.22}
        #}
    #for key, value in Data.items():
        #print(f"{key}: {value}\n")
#Team() 

Data = {
        "Edi Supriyanto"            :1196944,
        "Annisa Putri Restu"        :694228,
        "Riska Nurlita"             :849543,
        "Syarla Putri Guna"         :1095931,
        "Yandi Nugraha"             :981046,
        "Yolanda Oktaviani"         :3030997,
        "Erick Ervan Dewanggga"     :1575050,
        "Azizah Rahmawati"          :296411,
        "Aldi Taufik"               :3098808,
        "Ika Juliasari"             :2094764,
        "Debora Retima Sihombing"   :4317521,
        "Romli"                     :149098,
        "Ridhoi Berkat Zebua"       :6169604,
        "Fadilah Damayanti"         :6704840,
        "Erlangga Hutama"           :3638361,
        "Nur Halim"                 :3000531, 
        "Adistira Winditya P"       :0, 
        "Axl Wicaksono"             :2142137
        }

Tim = {"Hansyah_s2l" : {f"Daily paid": 39583010, "Paid amount": 858030646, "Total_amount": 8908510820 }}

Monthly = {
        "Edi Supriyanto"            :9.19,
        "Annisa Putri Restu"        :11.44,
        "Riska Nurlita"             :14.94,
        "Syarla Putri Guna"         :10.01,
        "Yandi Nugraha"             :9.84,
        "Yolanda Oktaviani"         :8.85,
        "Erick Ervan Dewanggga"     :10.86,
        "Azizah Rahmawati"          :10.00,
        "Aldi Taufik"               :6.90,
        "Ika Juliasari"             :9.60,
        "Debora Retima Sihombing"   :10.64,
        "Romli"                     :9.88,
        "Ridhoi Berkat Zebua"       :8.35,
        "Fadilah Damayanti"         :7.33,
        "Erlangga Hutama"           :6.68,
        "Nur Halim"                 :7.40, 
        "Adistira Winditya P"       :7.60, 
        "Axl Wicaksono"             :5.22
        }

Target = 7237417 
total_payment = 0

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

print("\n--------------------------------------------------------------------")
print(f"Total pembayaran hari ini : Rp {total_payment}")
print()
print(f"Pembayaran tertinggi: {highest_name} : Rp {highest_Payment}")
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

print("--------------------------------------------------------------------")

    

