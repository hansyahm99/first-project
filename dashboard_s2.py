import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# ------------------- SETUP -------------------
st.set_page_config(page_title="Dashboard S2", layout="wide")

# ================= LOGIN DATA =================
USER_CREDENTIALS = {
    "hansyah": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "Azizah": {"password": "irfan", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "nurlita": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
    "risnur": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
}

# ================= LOGIN PAGE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

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

else:
    # ================= DASHBOARD =================
    st.title("📊 Dashboard Report S2")
    today = datetime.today().strftime('%d %B %Y')

    # Buat folder khusus untuk tiap user
    user_dir = f"data/{st.session_state.username}"
    os.makedirs(user_dir, exist_ok=True)

    # File per user
    user_files = {
        "daily": f"{user_dir}/daily.xlsx",
        "cycle": f"{user_dir}/cycle.xlsx",
        "monthly": f"{user_dir}/monthly.xlsx",
        "rank": f"{user_dir}/rank.xlsx",
        "summary": f"{user_dir}/summary.xlsx"
    }

    # ===================== NAVIGATION =====================
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.markdown("**Menu Report:**")

    # Jika hansyah, tampilkan menu Update Data
    if st.session_state.username == "hansyah":
        menu_list = [
            '📅 Report Daily',
            '🔁 Report Cycle S2',
            '📆 Report Cycle Monthly',
            '🏅 Rank Agent S2',
            '📌 Summary report',
            '💾 Update Data',
            '📒 Data Pribadi',
            '📝 Noted',
            '💬 Group Chat'
        ]
    else:
        menu_list = [
            '📅 Report Daily',
            '🔁 Report Cycle S2',
            '📆 Report Cycle Monthly',
            '🏅 Rank Agent S2',
            '📌 Summary report',
            '📒 Data Pribadi',
            '📝 Noted',
            '💬 Group Chat'
        ]

    report_option = st.sidebar.radio("Pilih menu:", menu_list)

    # ===================== REPORT DAILY =====================
    if report_option == '📅 Report Daily':
        st.header(f"📅 Report Daily - {today}")
        if os.path.exists(user_files["daily"]):
            df_daily = pd.read_excel(user_files["daily"])
            st.dataframe(df_daily)
        else:
            st.warning("Belum ada data Daily Report.")

    # ===================== REPORT CYCLE =====================
    elif report_option == '🔁 Report Cycle S2':
        st.header("🔁 Report Cycle S2")
        if os.path.exists(user_files["cycle"]):
            df_cycle = pd.read_excel(user_files["cycle"])
            st.dataframe(df_cycle)
        else:
            st.warning("Belum ada data Cycle Report.")

    # ===================== REPORT MONTHLY =====================
    elif report_option == '📆 Report Cycle Monthly':
        st.header("📆 Report Cycle Monthly")
        if os.path.exists(user_files["monthly"]):
            df_monthly = pd.read_excel(user_files["monthly"])
            st.dataframe(df_monthly)
        else:
            st.warning("Belum ada data Monthly Report.")

    # ===================== RANK AGENT =====================
    elif report_option == '🏅 Rank Agent S2':
        st.header("🏅 Rank Agent S2")
        if os.path.exists(user_files["rank"]):
            df_rank = pd.read_excel(user_files["rank"])
            st.dataframe(df_rank)
        else:
            st.warning("Belum ada data Rank Agent.")

    # ===================== SUMMARY REPORT =====================
    elif report_option == '📌 Summary report':
        st.header("📌 Summary Report")
        if os.path.exists(user_files["summary"]):
            df_summary = pd.read_excel(user_files["summary"])
            st.dataframe(df_summary)
        else:
            st.warning("Belum ada data Summary Report.")

    # ===================== UPDATE DATA (khusus hansyah) =====================
    elif report_option == '💾 Update Data' and st.session_state.username == "hansyah":
        st.header("💾 Update / Tambah Data")

        # --- FITUR UPDATE FILE REPORT ---
        file_choice = st.selectbox("Pilih file report yang mau diupdate:", list(user_files.keys()))
        target_file = user_files[file_choice]

        uploaded_file = st.file_uploader("Upload file Excel baru untuk update report", type=["xlsx"])
        if uploaded_file is not None:
            with open(target_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Data {file_choice} berhasil diperbarui ✅")

        # Opsi tambah manual untuk Daily Report
        st.subheader("➕ Tambah data manual (Daily Report)")
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

    # ===================== DATA PRIBADI USER =====================
    elif report_option == '📒 Data Pribadi':
        st.header("📒 Data Pribadi User")
        user_data_file = f"user_data/{st.session_state.username}.xlsx"
        os.makedirs("user_data", exist_ok=True)

        if not os.path.exists(user_data_file):
            pd.DataFrame(columns=["Kolom1", "Kolom2", "Kolom3"]).to_excel(user_data_file, index=False)

        df_user = pd.read_excel(user_data_file)
        st.write("Data pribadi kamu (seperti Excel):")
        edited_df = st.data_editor(df_user, num_rows="dynamic", use_container_width=True)

        if st.button("💾 Simpan Data Pribadi"):
            edited_df.to_excel(user_data_file, index=False)
            st.success("Data pribadi berhasil disimpan ✅")

    # ===================== FITUR NOTED =====================
    elif report_option == '📝 Noted':
        st.header("📝 Catatan Pribadi (Noted)")
        os.makedirs("notes", exist_ok=True)
        notes_file = f"notes/{st.session_state.username}_notes.txt"

        if os.path.exists(notes_file):
            with open(notes_file, "r", encoding="utf-8") as f:
                current_notes = f.read()
        else:
            current_notes = ""

        notes_text = st.text_area("Tulis catatanmu di sini:", current_notes, height=250)

        if st.button("💾 Simpan Catatan"):
            with open(notes_file, "w", encoding="utf-8") as f:
                f.write(notes_text)
            st.success("Catatan berhasil disimpan ✅")

    # ===================== FITUR GROUP CHAT =====================
    elif report_option == '💬 Group Chat':
        st.header("💬 Group Chat (Semua User)")

        os.makedirs("chat", exist_ok=True)
        chat_file = "chat/group_chat.csv"

        if not os.path.exists(chat_file):
            pd.DataFrame(columns=["waktu", "user", "pesan"]).to_csv(chat_file, index=False)

        chat_df = pd.read_csv(chat_file)

        if not chat_df.empty:
            for _, row in chat_df.iterrows():
                st.markdown(f"**[{row['waktu']}] {row['user']}**: {row['pesan']}")
        else:
            st.info("Belum ada pesan di group chat.")

        st.subheader("✉️ Kirim Pesan")
        new_message = st.text_input("Tulis pesanmu:")
        if st.button("Kirim"):
            waktu = datetime.now().strftime("%H:%M:%S")
            new_row = pd.DataFrame([[waktu, st.session_state.username, new_message]],
                                   columns=["waktu", "user", "pesan"])
            chat_df = pd.concat([chat_df, new_row], ignore_index=True)
            chat_df.to_csv(chat_file, index=False)
            st.rerun()

    # ===================== LOGOUT =====================
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
