import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from streamlit_autorefresh import st_autorefresh
import base64
import pytz
from datetime import datetime

    # ------------------- FUNGSI NOTIFIKASI -------------------
def play_sound():
    sound_file = "notif.mp3"  # file mp3 harus ada di folder project
    if os.path.exists(sound_file):
        with open(sound_file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            md = f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
            st.markdown(md, unsafe_allow_html=True)

def show_notification(msg):
    st.toast(f"🔔 {msg}")
    play_sound()

    # ------------------- SETUP -------------------
st.set_page_config(page_title="Dashboard S2", layout="wide")

    #pastikan folder utama ada
os.makedirs("user_data", exist_ok=True)
os.makedirs("user_data/chat_images", exist_ok=True)
        # ================= LOGIN DATA =================
USER_CREDENTIALS = {
    "hansyah": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "riska": {"password": "riskacantik", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "azizah": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "annisa": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "sucika": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "taufik": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "halim": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "dika": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "tita": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "debora": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "ervan": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "romli": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "adistira": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "fadilah": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "sabrina": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "feronika": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "afrian": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "ayat": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "nurani": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
}
    # ================= SESSION LOGIN =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

    # ================= LOGIN PAGE =================
if not st.session_state.logged_in:
    st.title("🔑 Login Dashboard S2")

    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Login berhasil! Selamat datang, {username}.")
            st.rerun()
        else:
            st.error("ID atau Password salah ❌")

    # ================= DASHBOARD =================
else:
    st.title("📊 Dashboard Report S2")
    today = datetime.today().strftime('%d %B %Y')

    # Ambil file sesuai user yang login
    user_files = USER_CREDENTIALS[st.session_state.username]["files"]

    # ===================== NAVIGATION =====================
    profile_pic_path = f"user_data/profile_pics/{st.session_state.username}.png"
    if os.path.exists(profile_pic_path):
        st.sidebar.image(profile_pic_path, width=100)
    else:
        st.sidebar.image("https://img.icons8.com/color/96/user-male-circle--v1.png", width=80)

    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.markdown("**Menu Report:**")
    report_option = st.sidebar.radio(
        "Pilih report:",
        ('📅 Report Daily',
         '🔁 Report Cycle S2',
         '📆 Report Cycle Monthly',
         '🏅 Rank Agent S2',
         '📌 Summary report',
         '💾 Update Data',
         '💬 Group Chat',
         '📩 Private Chat',
         '⚙️ Settings',
         "📂 File Manager")
    )

    # ===================== DAILY REPORT =====================
    if report_option == '📅 Report Daily':
        st.header(f"📅 Report Daily - {today}")
        if os.path.exists(user_files["daily"]):
            df_daily = pd.read_excel(user_files["daily"])[['Collector', 'Repayment_amount']].fillna(0)
            df_daily = df_daily[df_daily['Collector'] != 'Hansyah Martha Kusuma D']
            df_daily["Repayment_amount"] = (
                df_daily['Repayment_amount'].astype(str)
                .str.replace(',', '')
                .str.replace('.00', '')
                .astype(int)
            )
            Data = dict(zip(df_daily['Collector'], df_daily['Repayment_amount']))
            nama = list(Data.keys())
            values = list(Data.values())

            fig1, ax1 = plt.subplots(figsize=(10, 4))
            ax1.barh(nama, values, color='orange')
            ax1.set_title(f"Report Daily {today} (Target Rp 7.000.000)", fontweight='bold')
            ax1.set_xlim(0, max(values) * 1.1)
            ax1.set_ylabel("Collector")
            ax1.get_xaxis().set_visible(False)
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['bottom'].set_visible(False)
            ax1.spines['left'].set_visible(False)

            max_val = max(values)
            for i, val in enumerate(values):
                if val > 0:
                    threshold = max_val * 0.08
                    if val >= threshold:
                        ax1.text(val - (max_val * 0.01), i, f"Rp {val:,}", va='center', fontsize=6, ha='right', color='black')
                    else:
                        ax1.text(val + (max_val * 0.1), i, f"Rp {val:,}", va='center', fontsize=8, ha='right', color='black')

            ax1.invert_yaxis()
            st.pyplot(fig1)
            st.dataframe(df_daily.rename(columns={"Repayment_amount": "Repayment Amount"}))
        else:
            st.warning("Belum ada data Daily untuk user ini.")

    # ===================== CYCLE REPORT =====================
    elif report_option == '🔁 Report Cycle S2':
        st.header(f"🔁 Report Cycle S2 - {today}")
        if os.path.exists(user_files["cycle"]):
            df_cycle = pd.read_excel(user_files["cycle"])[['Team', 'Recovery rate']].fillna(0)
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

            fig2, ax2 = plt.subplots(figsize=(2.5, 2.5), dpi=200)
            patches, texts, autotexts = ax2.pie(rate, autopct='%1.2f%%', startangle=140, colors=plt.cm.tab20.colors, textprops={'fontsize': 6})
            ax2.set_title(f"Cycle S2 Recovery Rate (Target: 0.12)", fontsize=7, fontweight='bold')
            ax2.axis('equal')
            ax2.legend(patches, team, loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=6, ncol=3)

            df_cycle.index = df_cycle.index + 1
            st.pyplot(fig2)
            st.dataframe(df_cycle[['Team', 'Recovery rate']])
        else:
            st.warning("Belum ada data Cycle untuk user ini.")

    # ===================== MONTHLY REPORT =====================
    elif report_option == '📆 Report Cycle Monthly':
        st.header("📆 Report Monthly - September 2025")
        if os.path.exists(user_files["monthly"]):
            df_monthly = pd.read_excel(user_files["monthly"])[['Collector', 'Pending Amount Recovery']].fillna(0)
            df_monthly = df_monthly[df_monthly['Collector'] != 'Hansyah Martha Kusuma D']
            df_monthly["Pending Amount Recovery"] = df_monthly['Pending Amount Recovery'].astype(float)
            Monthly = dict(zip(df_monthly['Collector'], df_monthly['Pending Amount Recovery']))
            bulan = list(Monthly.keys())
            hasil = list(Monthly.values())

            fig3, ax3 = plt.subplots(figsize=(12, 6))
            ax3.barh(bulan, hasil, color='purple')
            ax3.set_title("Monthly Pending Recovery (Target: 12.52%)", fontweight='bold')
            ax3.set_xlabel("Pending Amount Recovery")
            ax3.get_xaxis().set_visible(False)
            ax3.set_ylabel("Collector")
            ax3.set_xlim(0, max(hasil) * 1.2)

            for spine in ax3.spines.values():
                spine.set_visible(False)

            def format_number(val):
                return f"{val:.2f}%" if isinstance(val, float) else str(val)

            for i, val in enumerate(hasil):
                if val > 0:
                    label = format_number(val)
                    if val > 1:
                        ax3.text(val - 0.3, i, label, va='center', ha='right', fontsize=10, color='white')
                    else:
                        ax3.text(val + 0.3, i, label, va='center', ha='right', fontsize=10, color='black')

            ax3.invert_yaxis()
            st.pyplot(fig3)
            st.dataframe(df_monthly)
        else:
            st.warning("Belum ada data Monthly untuk user ini.")

    # ===================== RANK AGENT =====================
    elif report_option == '🏅 Rank Agent S2':
        st.header(f"🏅 Rank Agent S2 - {today}")
        if os.path.exists(user_files["rank"]):
            df_rank = pd.read_excel(user_files["rank"])[['Team', 'Collector', 'Monthly Pending Total(Rp)', 'Repayment', 'Recovery rate']].fillna(0)
            df_rank['_sort_rate'] = (
                df_rank['Recovery rate']
                .astype(str)
                .str.replace(',', '.')
                .str.replace('%', '')
                .astype(float)
            )
            df_rank_sorted = df_rank.sort_values(by="_sort_rate", ascending=False).drop(columns="_sort_rate")
            df_rank_sorted.index = df_rank_sorted.index + 1
            st.subheader("📈 Rank Agent Table (sorted by Recovery Rate)")
            st.dataframe(df_rank_sorted)
        else:
            st.warning("Belum ada data Rank untuk user ini.")

    # ===================== SUMMARY =====================
    elif report_option == '📌 Summary report':
        st.header("📌 Summary Report")
        if all(os.path.exists(user_files[f]) for f in ["daily", "monthly", "rank"]):
            df_daily = pd.read_excel(user_files["daily"])[['Collector', 'Repayment_amount']].fillna(0)
            df_daily = df_daily[df_daily['Collector'] != 'Hansyah Martha Kusuma D']
            df_daily["Repayment_amount"] = (
                df_daily['Repayment_amount'].astype(str)
                .str.replace(',', '')
                .str.replace('.00', '')
                .astype(int)
            )
            Data = dict(zip(df_daily['Collector'], df_daily['Repayment_amount']))

            df_monthly = pd.read_excel(user_files["monthly"])[['Collector', 'Pending Amount Recovery']].fillna(0)
            df_monthly = df_monthly[df_monthly['Collector'] != 'Hansyah Martha Kusuma D']
            df_monthly["Pending Amount Recovery"] = df_monthly['Pending Amount Recovery'].astype(float)
            hasil = df_monthly['Pending Amount Recovery'].tolist()

            df_rank = pd.read_excel(user_files["rank"])[['Team', 'Collector', 'Monthly Pending Total(Rp)', 'Repayment', 'Recovery rate']].fillna(0)

            Target = 7000000
            total_payment = sum(Data.values())
            highest_name = max(Data, key=Data.get)
            highest_payment = Data[highest_name]

            st.subheader("🎯 Daily Payment Summary")
            st.write(f"**Target Harian :** Rp {Target:,}")
            st.write(f"**Total Pembayaran Hari Ini :** Rp {total_payment:,}")
            st.write(f"**Pembayaran Tertinggi :** {highest_name} - Rp {highest_payment:,}")

            st.write("### Status Collector and Target:")
            status_data = []
            for name, val in Data.items():
                status = "✅ Target" if val > Target else "❌ Belum Target"
                status_data.append({"Collector": name, "Pembayaran": val, "Status": status})

            df_status = pd.DataFrame(status_data)
            df_status.index = df_status.index + 1
            st.dataframe(df_status)

            st.subheader("📊 Monthly Recovery Summary")
            st.write("**Target Recovery :** 12.52%")
            average_result = sum(hasil) / len(hasil)
            st.write(f"**Rata-rata Recovery Tim :** {average_result:.2f} %")

            hansyah_data = df_rank[df_rank['Team'] == 'Hansyah_S2l'].copy()
            hansyah_data['Repayment'] = hansyah_data['Repayment'].astype(str).str.replace(',', '').astype(float)
            hansyah_data['Monthly Pending Total(Rp)'] = hansyah_data['Monthly Pending Total(Rp)'].astype(str).str.replace(',', '').astype(float)
            total_repayment_hansyah = hansyah_data['Repayment'].sum()
            total_unpaid_hansyah = hansyah_data['Monthly Pending Total(Rp)'].sum()

            st.write(f"**Total Repayment :** Rp {total_repayment_hansyah:,.0f}")
            st.write(f"**Total Unpaid :** Rp {total_unpaid_hansyah:,.0f}")
        else:
            st.warning("Belum ada data Summary untuk user ini.")

    # ===================== UPDATE DATA =====================
    elif report_option == '💾 Update Data':
        st.header("💾 Update / Tambah Data")

    # --- FITUR UPDATE FILE REPORT ---
        file_choice = st.selectbox("Pilih file report yang mau diupdate:", list(user_files.keys()))
        target_file = user_files[file_choice]

        uploaded_file = st.file_uploader("Upload file Excel baru untuk update report", type=["xlsx"])
        if uploaded_file is not None:
            with open(target_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Data {file_choice} berhasil diperbarui ✅")

        st.subheader("➕ Tambah data manual (hanya untuk Daily Report)")
        if file_choice == "daily":
            collector = st.text_input("Collector")
            amount = st.number_input("Repayment_amount", min_value=0, step=1000)
            if st.button("Simpan data baru"):
                if os.path.exists(target_file):
                    df_existing = pd.read_excel(target_file)
                else:
                    df_existing = pd.DataFrame(columns=["Collector", "Repayment_amount"])

                new_row = {"Collector": collector, "Repayment_amount": amount}
                df_existing = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)
                df_existing.to_excel(target_file, index=False)
                st.success("Data berhasil ditambahkan ✅")
                st.dataframe(df_existing)

    # --- FITUR DATA PRIBADI USER ---
        st.subheader("📒 Data Pribadi User")
        os.makedirs("user_data", exist_ok=True)
        user_data_file = f"user_data/{st.session_state.username}.xlsx"

    # Kalau file belum ada, buat dengan tipe kolom sesuai permintaan
        if not os.path.exists(user_data_file):
            df_user = pd.DataFrame({
                "Kolom1": pd.Series(dtype="str"),   # string
                "Kolom2": pd.Series(dtype="str"),   # string
                "Kolom3": pd.Series(dtype="float"), # angka
                "Kolom4": pd.Series(dtype="float")  # angka
            })
            df_user.to_excel(user_data_file, index=False)
        else:
    # Baca excel: Kolom1 & Kolom2 jadi string, Kolom3 angka
            df_user = pd.read_excel(
                user_data_file,
                dtype={"Kolom1": str, "Kolom2": str, "Kolom3": float, "Kolom4": float}
            )

        st.write("Data pribadi kamu (seperti Excel):")
        edited_df = st.data_editor(df_user, num_rows="dynamic", use_container_width=True)

        if st.button("💾 Simpan Data Pribadi"):
            edited_df.to_excel(user_data_file, index=False)
            st.success("Data pribadi berhasil disimpan ✅")

    # --- FITUR NOTED PRIBADI ---
        st.subheader("📝 Noted Pribadi")
        notes_file = f"user_data/{st.session_state.username}_notes.txt"

        if not os.path.exists(notes_file):
            with open(notes_file, "w", encoding="utf-8") as f:
                f.write("")

    # Baca isi notes
        with open(notes_file, "r", encoding="utf-8") as f:
            current_notes = f.read()

    # Text area untuk edit notes
        new_notes = st.text_area("Tulis catatan pribadimu di sini:", current_notes, height=200)

        if st.button("💾 Simpan Noted"):
            with open(notes_file, "w", encoding="utf-8") as f:
                f.write(new_notes)
            st.success("Catatan berhasil disimpan ✅")

    # ===================== GROUP CHAT =====================
    elif report_option == '💬 Group Chat':
        st.header("💬 Group Chat Dashboard S2")

        chat_file = "user_data/group_chat.csv"
        os.makedirs("user_data", exist_ok=True)
        os.makedirs("user_data/chat_images", exist_ok=True)

        if not os.path.exists(chat_file):
            df_chat = pd.DataFrame(columns=["id", "username", "time", "message"])
            df_chat.to_csv(chat_file, index=False)

        df_chat = pd.read_csv(chat_file)

    # ==== CEK PESAN BARU UNTUK NOTIFIKASI ====
        last_seen_file = f"user_data/last_seen_{st.session_state.username}_group.txt"
        if os.path.exists(last_seen_file):
            with open(last_seen_file, "r") as f:
                last_seen = f.read().strip()
        else:
            last_seen = "00:00:00"

        new_msgs = df_chat[df_chat["time"] > last_seen]
        if not new_msgs.empty and new_msgs.iloc[-1]["username"] != st.session_state.username:
            show_notification(f"{len(new_msgs)} pesan baru di Group Chat!")

    # update last_seen
        if not df_chat.empty:
            with open(last_seen_file, "w") as f:
                f.write(df_chat.iloc[-1]["time"])

    # 🔄 AUTO REFRESH KHUSUS GRUP CHAT
        st_autorefresh(interval=1500, limit=None, key="chat_refresh")

        if not df_chat.empty:
            for idx, row in df_chat.iterrows():
                with st.chat_message("user"):
                    if row['message'] == "__deleted__": 
                        st.markdown(f"**{row['username']} ({row['time']})**: 🗑 Pesan ini telah dihapus")
                    else:
    # 🔥 CEK APAKAH PESAN GAMBAR ATAU TEKS
                        if str(row['message']).startswith("__img__"):
                            img_path = row['message'].replace("__img__:", "")
                            if os.path.exists(img_path):
                                st.markdown(f"**{row['username']} ({row['time']})** mengirim gambar:")
                                st.image(img_path, width=200)
                                with open(img_path, "rb") as file:
                                    st.download_button(
                                        label="⬇️ Download Gambar",
                                        data=file,
                                        file_name=os.path.basename(img_path),
                                        mime="image/png",
                                        key=f"dl_{idx}"  # unik per pesan
                                    )
                            else:
                                st.warning("❌ Gambar tidak ditemukan")
                        else:
                            st.markdown(f"**{row['username']} ({row['time']})**: {row['message']}")

    # tombol hapus hanya muncul untuk pengirim pesan
                    if row['username'] == st.session_state.username:
                        if st.button("Hapus", key=f"del_{idx}"):
                            df_chat.loc[idx, "message"] = "__deleted__"
                            df_chat.to_csv(chat_file, index=False)
                            st.rerun()
        else:
            st.info("Belum ada chat, ayo mulai ngobrol 🚀")

        col1, col2 = st.columns([3, 1])
        with col1:
            new_msg = st.chat_input("Ketik pesanmu di sini...")
        with col2:
            uploaded_img = st.file_uploader("📷", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

        if new_msg:
            from zoneinfo import ZoneInfo
            now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([{
                "id": len(df_chat) + 1,
                "username": st.session_state.username,
                "time": now,
                "message": new_msg
            }])
            df_chat = pd.concat([df_chat, new_row], ignore_index=True)
            df_chat.to_csv(chat_file, index=False)
            st.rerun()
        
        if uploaded_img and "last_uploaded" not in st.session_state:
            from zoneinfo import ZoneInfo
            now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
            img_path = f"user_data/chat_images/{st.session_state.username}_{now.replace(':','-')}_{uploaded_img.name}"
            with open(img_path, "wb") as f:
                f.write(uploaded_img.read())

            new_row = pd.DataFrame([{
                "id": len(df_chat) + 1,
                "username": st.session_state.username,
                "time": now,
                "message": f"__img__:{img_path}"
            }])
            df_chat = pd.concat([df_chat, new_row], ignore_index=True)
            df_chat.to_csv(chat_file, index=False)

            st.session_state["last_uploaded"] = uploaded_img.name
            st.rerun()
            
        if uploaded_img is None and "last_uploaded" in st.session_state:
            del st.session_state["last_uploaded"]

    # ===================== PRIVATE CHAT =====================
    elif report_option == '📩 Private Chat':
        st.header("📩 Private Chat")

        chat_dir = "user_data/private_chats"
        os.makedirs(chat_dir, exist_ok=True)

        all_users = list(USER_CREDENTIALS.keys())
        all_users.remove(st.session_state.username)
        target_user = st.selectbox("Pilih user untuk private chat:", all_users)

        users_pair = "_".join(sorted([st.session_state.username, target_user]))
        chat_file = os.path.join(chat_dir, f"{users_pair}.csv")

        if not os.path.exists(chat_file):
            df_chat = pd.DataFrame(columns=["id", "username", "time", "message"])
            df_chat.to_csv(chat_file, index=False)

        df_chat = pd.read_csv(chat_file)

    # ==== CEK PESAN BARU UNTUK NOTIFIKASI ====
        last_seen_file = f"user_data/last_seen_{st.session_state.username}_{target_user}.txt"
        if os.path.exists(last_seen_file):
            with open(last_seen_file, "r") as f:
                last_seen = f.read().strip()
        else:
            last_seen = "00:00:00"

        new_msgs = df_chat[(df_chat["time"] > last_seen) & (df_chat["username"] != st.session_state.username)]
        if not new_msgs.empty:
            show_notification(f"{len(new_msgs)} pesan baru dari {target_user}")

    # update last_seen
        if not df_chat.empty:
            os.makedirs("user_data", exist_ok=True)
            with open(last_seen_file, "w") as f:
                f.write(df_chat.iloc[-1]["time"])

    # 🔄 AUTO REFRESH KHUSUS PRIVATE CHAT
        st_autorefresh(interval=1500, limit=None, key="private_refresh")

        if not df_chat.empty:
            for idx, row in df_chat.iterrows():
                role = "assistant" if row['username'] == st.session_state.username else "user"
                with st.chat_message(role):
                    if row['message'] == "__deleted__":
                        st.markdown(f"**{row['username']} ({row['time']})**: 🗑 Pesan ini telah dihapus")
                    else:
    # 🔥 CEK PESAN GAMBAR ATAU TEKS
                        if str(row['message']).startswith("__img__"):
                            img_path = row['message'].replace("__img__:", "")
                            if os.path.exists(img_path):
                                st.markdown(f"**{row['username']} ({row['time']})** mengirim gambar:")
                                st.image(img_path, width=200)  # tampil lebih proporsional
                                with open(img_path, "rb") as file:
                                    st.download_button(
                                        label="⬇️ Download Gambar",
                                        data=file,
                                        file_name=os.path.basename(img_path),
                                        mime="image/png",
                                        key=f"dl_priv_{idx}"
                                    )
                            else:
                                st.warning("❌ Gambar tidak ditemukan")
                        else:
                            st.markdown(f"**{row['username']} ({row['time']})**: {row['message']}")

    # tombol hapus hanya muncul untuk pengirim pesan
                    if row['username'] == st.session_state.username:
                        if st.button("Hapus", key=f"del_priv_{idx}"):
                            df_chat.loc[idx, "message"] = "__deleted__"
                            df_chat.to_csv(chat_file, index=False)
                            st.rerun()
        else:
            st.info(f"Belum ada chat dengan {target_user}")

    # === INPUT PESAN & GAMBAR ===
        col1, col2 = st.columns([3, 1])
        with col1:
            new_msg = st.chat_input(f"Ketik pesan ke {target_user}...")
        with col2:
            uploaded_img = st.file_uploader("📷", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

    # === SIMPAN PESAN TEKS ===
        if new_msg:
            from zoneinfo import ZoneInfo
            now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([{
                "id": len(df_chat) + 1,
                "username": st.session_state.username,
                "time": now,
                "message": new_msg
            }])
            df_chat = pd.concat([df_chat, new_row], ignore_index=True)
            df_chat.to_csv(chat_file, index=False)
            st.rerun()

         # === SIMPAN PESAN GAMBAR ===
        if uploaded_img and "last_uploaded" not in st.session_state:
            from zoneinfo import ZoneInfo
            now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
            img_path = f"user_data/chat_images/{st.session_state.username}_{now.replace(':','-')}_{uploaded_img.name}"
            with open(img_path, "wb") as f:
                f.write(uploaded_img.read())

            new_row = pd.DataFrame([{
                "id": len(df_chat) + 1,
                "username": st.session_state.username,
                "time": now,
                "message": f"__img__:{img_path}"
            }])
            df_chat = pd.concat([df_chat, new_row], ignore_index=True)
            df_chat.to_csv(chat_file, index=False)

            st.session_state["last_uploaded"] = uploaded_img.name
            st.rerun()

        if uploaded_img is None and "last_uploaded" in st.session_state:
            del st.session_state["last_uploaded"]

#----------------halaman Setting-----------
    elif report_option == '⚙️ Settings':
        st.header("⚙️ Pengaturan Akun")

    # ---------- FOTO PROFIL ----------
        st.subheader("🖼 Ganti Foto Profil")
        os.makedirs("user_data/profile_pics", exist_ok=True)
        profile_pic_path = f"user_data/profile_pics/{st.session_state.username}.png"

    # Tampilkan foto jika ada
        if os.path.exists(profile_pic_path):
            st.image(profile_pic_path, width=100, caption="Foto Profil Saat Ini")

        uploaded_image = st.file_uploader("Upload foto baru (.png, .jpg, .jpeg)", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            with open(profile_pic_path, "wb") as f:
                f.write(uploaded_image.read())
            st.success("Foto profil berhasil diperbarui ✅")
            st.rerun()

    # ---------- GANTI PASSWORD ----------
        st.subheader("🔑 Ganti Password")
        old_password = st.text_input("Password Lama", type="password")
        new_password = st.text_input("Password Baru", type="password")
        confirm_password = st.text_input("Konfirmasi Password Baru", type="password")

        if st.button("Ubah Password"):
            current_password = USER_CREDENTIALS[st.session_state.username]["password"]
            if old_password != current_password:
                st.error("Password lama salah ❌")
            elif new_password != confirm_password:
                st.error("Konfirmasi password tidak cocok ❌")
            elif new_password == "":
                st.warning("Password baru tidak boleh kosong")
            else:
                USER_CREDENTIALS[st.session_state.username]["password"] = new_password
                st.success("Password berhasil diubah ✅ (Perubahan hanya berlaku selama runtime jika tidak disimpan permanen)")
    
        st.markdown("⚠️ *Catatan: Password akan hilang jika aplikasi dimuat ulang kecuali kamu menyimpan ke file JSON / DB.*")

    # ---------- HAPUS CHAT GRUP ----------
        st.subheader("🧹 Hapus Riwayat Chat Grup")
        if st.button("🗑 Hapus Semua Chat Grup"):
            chat_file = "user_data/group_chat.csv"
            if os.path.exists(chat_file):
                df_empty = pd.DataFrame(columns=["id", "username", "time", "message"])
                df_empty.to_csv(chat_file, index=False)
                st.success("Riwayat chat grup berhasil dihapus ✅")
            else:
                st.info("Belum ada chat grup untuk dihapus.")

    # ---------- HAPUS CHAT PRIVAT ----------
        st.subheader("🧹 Hapus Riwayat Chat Privat")
        chat_dir = "user_data/private_chats"
        if os.path.exists(chat_dir):
            user_files = [f for f in os.listdir(chat_dir) if st.session_state.username in f]
            if user_files:
                for file in user_files:
                    if st.button(f"🗑 Hapus Chat dengan {file.replace('.csv','').replace(st.session_state.username, '').replace('_','')}"):
                        os.remove(os.path.join(chat_dir, file))
                        st.success(f"Riwayat chat privat dengan {file} berhasil dihapus ✅")
            else:
                st.info("Tidak ada riwayat chat privat.")
        else:
            st.info("Folder chat privat belum dibuat.")
    
    # ===================== FILE MANAGER =====================
    elif report_option == '📂 File Manager':
        st.header("📂 File Manager")

        UPLOAD_DIR = "user_uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    # --- Upload file ---
        uploaded_file = st.file_uploader(
            "Upload file (xlsx, csv, txt, pdf, png, jpg, jpeg)",
            type=["xlsx", "csv", "txt", "pdf", "png", "jpg", "jpeg"]
        )
        if uploaded_file:
            save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ File berhasil disimpan: {uploaded_file.name}")

        # --- Preview isi file ---
            ext = uploaded_file.name.split(".")[-1].lower()
            if ext == "xlsx":
                df = pd.read_excel(save_path)
                st.dataframe(df)
            elif ext == "csv":
                df = pd.read_csv(save_path)
                st.dataframe(df)
            elif ext == "txt":
                with open(save_path, "r", encoding="utf-8") as f:
                    st.text_area("Isi TXT:", f.read(), height=200)
            elif ext in ["png", "jpg", "jpeg"]:
                st.image(save_path, width=300)
            elif ext == "pdf":
                st.info("📄 PDF berhasil diupload (preview tidak didukung).")

    # --- Daftar file tersimpan ---
        st.subheader("📑 File Tersimpan")
        files = os.listdir(UPLOAD_DIR)
        if files:
            for file in files:
                file_path = os.path.join(UPLOAD_DIR, file)

            # download button
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Download {file}",
                        data=f,
                        file_name=file
                    )
            # delete button
                if st.button(f"🗑️ Hapus {file}", key=f"del_{file}"):
                    os.remove(file_path)
                    st.warning(f"{file} dihapus!")
                    st.experimental_rerun()
        else:
            st.info("Belum ada file yang diupload.")

    # ===================== LOGOUT =====================
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
