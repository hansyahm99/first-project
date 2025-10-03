# dashboard_s2_full.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import base64
import json
from zoneinfo import ZoneInfo
from streamlit_autorefresh import st_autorefresh

# ------------------- UTILITIES -------------------
def ensure_dirs():
    os.makedirs("user_data", exist_ok=True)
    os.makedirs("user_data/chat_images", exist_ok=True)
    os.makedirs("user_data/chat_files/group", exist_ok=True)
    os.makedirs("user_data/chat_files/private", exist_ok=True)
    os.makedirs("user_data/profile_pics", exist_ok=True)
    os.makedirs("user_data/uploads", exist_ok=True)
    os.makedirs("user_data/private_chats", exist_ok=True)

def sanitize_filename(fname: str) -> str:
    fname = fname.replace("..", "")
    fname = fname.replace("/", "_").replace("\\", "_")
    fname = fname.strip().replace(" ", "_")
    return fname

def play_sound():
    # Jika file notif.mp3 ada, embed sebagai base64 audio (autoplay)
    sound_file = "notif.mp3"
    if os.path.exists(sound_file):
        try:
            with open(sound_file, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            md = f"""
            <audio autoplay>
              <source src="data:audio/mp3;base64,{b64}" type="audio/mp3" />
            </audio>
            """
            st.markdown(md, unsafe_allow_html=True)
        except Exception:
            pass

def show_notification(msg):
    # Streamlit versi lama mungkin tidak punya st.toast; fallback ke st.info
    try:
        st.toast(f"🔔 {msg}")
    except Exception:
        st.info(f"🔔 {msg}")
    play_sound()

def load_excel_safe(path, usecols=None, dtype=None):
    try:
        return pd.read_excel(path, usecols=usecols, dtype=dtype)
    except Exception:
        try:
            # coba read tanpa usecols jika gagal
            return pd.read_excel(path)
        except Exception:
            return pd.DataFrame()

def save_json_safe(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_json_safe(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

# ------------------- DEFAULT CREDENTIALS -------------------
DEFAULT_CREDENTIALS = {
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
    "suwandi": {"password": "12345", "files": {"daily": "riska.xlsx", "cycle": "riskuy.xlsx", "monthly": "nurlita.xlsx", "rank": "risnur.xlsx"}},
}

CREDENTIALS_FILE = "user_credentials.json"

def ensure_credentials():
    creds = load_json_safe(CREDENTIALS_FILE)
    if not creds:
        # simpan default jika belum ada
        save_json_safe(CREDENTIALS_FILE, DEFAULT_CREDENTIALS)
        creds = DEFAULT_CREDENTIALS.copy()
    # Pastikan setiap user punya struktur "files" minimal
    for k, v in creds.items():
        if "files" not in v:
            v["files"] = {"daily": "", "cycle": "", "monthly": "", "rank": ""}
    return creds

# ------------------- START -------------------
ensure_dirs()
USER_CREDENTIALS = ensure_credentials()

# ------------------- SESSION STATE -------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="Dashboard S2", layout="wide")

# ------------------- LOGIN PAGE -------------------
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
    # ------------------- DASHBOARD -------------------
    st.title("📊 Dashboard Report S2")
    today = datetime.now(ZoneInfo("Asia/Jakarta")).strftime('%d %B %Y')
    # Ambil file sesuai user yang login (fallback aman)
    user_files = USER_CREDENTIALS.get(st.session_state.username, {}).get("files", {})
    # ---------------- SIDEBAR ----------------
    profile_pic_path = f"user_data/profile_pics/{st.session_state.username}.png"
    if os.path.exists(profile_pic_path):
        st.sidebar.image(profile_pic_path, width=100)
    else:
        st.sidebar.image("https://img.icons8.com/color/96/user-male-circle--v1.png", width=80)
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.markdown("**Menu Report:**")
    report_option = st.sidebar.radio(
        "Pilih report:",
        (
            '📅 Report Daily',
            '🔁 Report Cycle S2',
            '📆 Report Cycle Monthly',
            '🏅 Rank Agent S2',
            '📌 Summary report',
            '💾 Update Data',
            '💬 Group Chat',
            '📩 Private Chat',
            '📂 File Manager',
            '⚙️ Settings',
            'Musik Muktar',
        )
    )

    # ----------------- helper display message -----------------
    def display_message(row):
        # role chat_message (Streamlit chat) : if row username == current -> assistant else user
        role = "assistant" if row.get('username') == st.session_state.username else "user"
        with st.chat_message(role):
            st.markdown(f"**{row.get('username', '')}** ({row.get('time', '')}):")
            # show file preview if present
            fp = row.get("file_path", None)
            msg = row.get("message", "")
            # if explicit file_path exists
            if isinstance(fp, str) and fp and fp.lower() != "nan":
                ext = os.path.splitext(fp)[1].lower()
                if ext in [".png", ".jpg", ".jpeg"]:
                    if os.path.exists(fp):
                        st.image(fp, caption=os.path.basename(fp), width=300)
                    else:
                        st.warning("❌ File gambar tidak ditemukan")
                else:
                    if os.path.exists(fp):
                        try:
                            with open(fp, "rb") as f:
                                st.download_button("⬇️ Unduh file", f, file_name=os.path.basename(fp))
                        except Exception:
                            st.warning("❌ Gagal menyiapkan download")
                    else:
                        st.warning("❌ File tidak ditemukan")
            # if message contains __img__ path inside
            elif isinstance(msg, str) and msg.startswith("__img__:"):
                img_path = msg.replace("__img__:", "")
                if os.path.exists(img_path):
                    try:
                        st.image(img_path, caption=os.path.basename(img_path), width=300)
                    except Exception:
                        st.warning("❌ Gagal menampilkan gambar")
                else:
                    st.warning("❌ File gambar tidak ditemukan")
            # if normal text message
            if isinstance(msg, str) and msg and not msg.startswith("__img__:"):
                # render text (plain)
                st.write(msg)

    # ===================== DAILY REPORT =====================
    if report_option == '📅 Report Daily':
        st.header(f"📅 Report Daily - {today}")
        target_path = user_files.get("daily", "")
        if target_path and os.path.exists(target_path):
            df_daily = load_excel_safe(target_path)
            # safe column extraction
            if 'Collector' in df_daily.columns and 'Repayment_amount' in df_daily.columns:
                df_daily = df_daily[['Collector', 'Repayment_amount']].fillna(0)
                # filter out a specific name safely
                df_daily = df_daily[df_daily['Collector'] != 'Hansyah Martha Kusuma D']
                # normalize Repayment_amount to int
                def to_int_safe(x):
                    try:
                        s = str(x).replace(',', '').replace('.00', '')
                        return int(float(s))
                    except Exception:
                        return 0
                df_daily["Repayment_amount"] = df_daily['Repayment_amount'].apply(to_int_safe)
                Data = dict(zip(df_daily['Collector'], df_daily['Repayment_amount']))
                if Data:
                    nama = list(Data.keys())
                    values = list(Data.values())
                    fig1, ax1 = plt.subplots(figsize=(10, 4))
                    ax1.barh(nama, values, color='orange')
                    ax1.set_title(f"Report Daily {today} (Target Rp 7.000.000)", fontweight='bold')
                    ax1.set_xlim(0, max(values) * 1.1 if max(values) > 0 else 1)
                    ax1.set_ylabel("Collector")
                    ax1.get_xaxis().set_visible(False)
                    for spine in ['top', 'right', 'bottom', 'left']:
                        ax1.spines[spine].set_visible(False)
                    max_val = max(values) if values else 0
                    for i, val in enumerate(values):
                        if val > 0 and max_val > 0:
                            threshold = max_val * 0.08
                            if val >= threshold:
                                ax1.text(val - (max_val * 0.01), i, f"Rp {val:,}", va='center', fontsize=6, ha='right', color='black')
                            else:
                                ax1.text(val + (max_val * 0.1), i, f"Rp {val:,}", va='center', fontsize=8, ha='right', color='black')
                    ax1.invert_yaxis()
                    st.pyplot(fig1)
                    st.dataframe(df_daily.rename(columns={"Repayment_amount": "Repayment Amount"}))
                else:
                    st.info("Tidak ada data pembayaran di file Daily.")
            else:
                st.warning("Kolom 'Collector' atau 'Repayment_amount' tidak ditemukan pada file Daily.")
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
        st.header("📆 Report Monthly")
        target_path = user_files.get("monthly", "")
        if target_path and os.path.exists(target_path):
            df_monthly = load_excel_safe(target_path)
            if 'Collector' in df_monthly.columns and 'Pending Amount Recovery' in df_monthly.columns:
                df_monthly = df_monthly[['Collector', 'Pending Amount Recovery']].fillna(0)
                df_monthly = df_monthly[df_monthly['Collector'] != 'Hansyah Martha Kusuma D']
                # ensure float
                def to_float_safe(x):
                    try:
                        return float(x)
                    except Exception:
                        return 0.0
                df_monthly["Pending Amount Recovery"] = df_monthly['Pending Amount Recovery'].apply(to_float_safe)
                Monthly = dict(zip(df_monthly['Collector'], df_monthly['Pending Amount Recovery']))
                if Monthly:
                    bulan = list(Monthly.keys())
                    hasil = list(Monthly.values())
                    fig3, ax3 = plt.subplots(figsize=(12, 6))
                    ax3.barh(bulan, hasil, color='purple')
                    ax3.set_title("Monthly Pending Recovery (Target: 12.52%)", fontweight='bold')
                    ax3.set_xlabel("Pending Amount Recovery")
                    ax3.get_xaxis().set_visible(False)
                    ax3.set_ylabel("Collector")
                    ax3.set_xlim(0, max(hasil) * 1.2 if hasil and max(hasil) > 0 else 1)
                    for spine in ax3.spines.values():
                        spine.set_visible(False)
                    for i, val in enumerate(hasil):
                        if val > 0:
                            label = f"{val:.2f}" if isinstance(val, float) else str(val)
                            if val > 1:
                                ax3.text(val - 0.3, i, label, va='center', ha='right', fontsize=10, color='white')
                            else:
                                ax3.text(val + 0.3, i, label, va='center', ha='right', fontsize=10, color='black')
                    ax3.invert_yaxis()
                    st.pyplot(fig3)
                    st.dataframe(df_monthly)
                else:
                    st.info("Tidak ada data Monthly.")
            else:
                st.warning("Kolom 'Collector' atau 'Pending Amount Recovery' tidak ditemukan pada file Monthly.")
        else:
            st.warning("Belum ada data Monthly untuk user ini.")

    # ===================== RANK AGENT =====================
    elif report_option == '🏅 Rank Agent S2':
        st.header(f"🏅 Rank Agent S2 - {today}")
        target_path = user_files.get("rank", "")
        if target_path and os.path.exists(target_path):
            df_rank = load_excel_safe(target_path)
            needed = ['Team', 'Collector', 'Monthly Pending Total(Rp)', 'Repayment', 'Recovery rate']
            if all(col in df_rank.columns for col in needed):
                df_rank = df_rank[needed].fillna(0)
                def to_float_rate(x):
                    try:
                        return float(str(x).replace(',', '.').replace('%', ''))
                    except Exception:
                        return 0.0
                df_rank['_sort_rate'] = df_rank['Recovery rate'].apply(to_float_rate)
                df_rank_sorted = df_rank.sort_values(by="_sort_rate", ascending=False).drop(columns="_sort_rate")
                df_rank_sorted.index = df_rank_sorted.index + 1
                st.subheader("📈 Rank Agent Table (sorted by Recovery Rate)")
                st.dataframe(df_rank_sorted)
            else:
                st.warning("File Rank tidak memiliki semua kolom yang dibutuhkan.")
        else:
            st.warning("Belum ada data Rank untuk user ini.")

    # ===================== SUMMARY =====================
    elif report_option == '📌 Summary report':
        st.header("📌 Summary Report")
        files_exist = all(user_files.get(k) and os.path.exists(user_files.get(k)) for k in ["daily", "monthly", "rank"])
        if files_exist:
            # DAILY
            df_daily = load_excel_safe(user_files["daily"])
            if 'Collector' in df_daily.columns and 'Repayment_amount' in df_daily.columns:
                df_daily = df_daily[['Collector', 'Repayment_amount']].fillna(0)
                df_daily = df_daily[df_daily['Collector'] != 'Hansyah Martha Kusuma D']
                def to_int_safe(x):
                    try:
                        s = str(x).replace(',', '').replace('.00', '')
                        return int(float(s))
                    except Exception:
                        return 0
                df_daily["Repayment_amount"] = df_daily['Repayment_amount'].apply(to_int_safe)
                Data = dict(zip(df_daily['Collector'], df_daily['Repayment_amount']))
            else:
                Data = {}

            # MONTHLY
            df_monthly = load_excel_safe(user_files["monthly"])
            if 'Collector' in df_monthly.columns and 'Pending Amount Recovery' in df_monthly.columns:
                df_monthly = df_monthly[['Collector', 'Pending Amount Recovery']].fillna(0)
                df_monthly = df_monthly[df_monthly['Collector'] != 'Hansyah Martha Kusuma D']
                df_monthly["Pending Amount Recovery"] = df_monthly['Pending Amount Recovery'].apply(lambda x: float(x) if str(x).replace('.', '', 1).replace('-', '').isdigit() else 0.0)
                hasil = df_monthly['Pending Amount Recovery'].tolist()
            else:
                hasil = []

            # RANK
            df_rank = load_excel_safe(user_files["rank"])
            if 'Team' in df_rank.columns:
                hansyah_data = df_rank[df_rank['Team'] == 'Hansyah_S2l'].copy()
                # attempt to coerce numeric columns
                for col in ['Repayment', 'Monthly Pending Total(Rp)']:
                    if col in hansyah_data.columns:
                        hansyah_data[col] = hansyah_data[col].astype(str).str.replace(',', '').apply(lambda x: float(x) if x.replace('.', '', 1).replace('-', '').isdigit() else 0.0)
                total_repayment_hansyah = hansyah_data['Repayment'].sum() if 'Repayment' in hansyah_data.columns else 0.0
                total_unpaid_hansyah = hansyah_data['Monthly Pending Total(Rp)'].sum() if 'Monthly Pending Total(Rp)' in hansyah_data.columns else 0.0
            else:
                total_repayment_hansyah = 0.0
                total_unpaid_hansyah = 0.0

            # summary display
            Target = 7000000
            total_payment = sum(Data.values()) if Data else 0
            if Data:
                highest_name = max(Data, key=Data.get)
                highest_payment = Data[highest_name]
            else:
                highest_name = "-"
                highest_payment = 0

            st.subheader("🎯 Daily Payment Summary")
            st.write(f"**Target Harian :** Rp {Target:,}")
            st.write(f"**Total Pembayaran Hari Ini :** Rp {total_payment:,}")
            st.write(f"**Pembayaran Tertinggi :** {highest_name} - Rp {highest_payment:,}")
            st.write("### Status Collector and Target:")
            status_data = []
            for name, val in (Data.items() if Data else []):
                status = "✅ Target" if val > Target else "❌ Belum Target"
                status_data.append({"Collector": name, "Pembayaran": val, "Status": status})
            df_status = pd.DataFrame(status_data)
            if not df_status.empty:
                df_status.index = df_status.index + 1
                st.dataframe(df_status)
            else:
                st.info("Tidak ada data status collector.")

            st.subheader("📊 Monthly Recovery Summary")
            st.write("**Target Recovery :** 12.52%")
            if hasil:
                average_result = sum(hasil) / len(hasil)
                st.write(f"**Rata-rata Recovery Tim :** {average_result:.2f} %")
            else:
                st.info("Tidak ada data monthly untuk dihitung rata-rata.")
            st.write(f"**Total Repayment Hansyah :** Rp {total_repayment_hansyah:,.0f}")
            st.write(f"**Total Unpaid Hansyah :** Rp {total_unpaid_hansyah:,.0f}")
        else:
            st.warning("Belum ada data Summary untuk user ini (daily/monthly/rank harus tersedia).")

    # ===================== UPDATE DATA =====================
    elif report_option == '💾 Update Data':
        st.header("💾 Update / Tambah Data")
        # pilih file yang boleh diupdate (lihat user_files)
        file_choice = st.selectbox("Pilih file report yang mau diupdate:", list(user_files.keys()) if user_files else [])
        target_file = user_files.get(file_choice, "")
        uploaded_file = st.file_uploader("Upload file Excel baru untuk update report", type=["xlsx"])
        if uploaded_file is not None and target_file:
            try:
                with open(target_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Data {file_choice} berhasil diperbarui ✅")
            except Exception as e:
                st.error(f"Gagal menyimpan file: {e}")

        st.subheader("➕ Tambah data manual (hanya untuk Daily Report)")
        if file_choice == "daily":
            collector = st.text_input("Collector")
            amount = st.number_input("Repayment_amount", min_value=0, step=1000)
            if st.button("Simpan data baru"):
                if target_file and os.path.exists(target_file):
                    df_existing = load_excel_safe(target_file)
                else:
                    df_existing = pd.DataFrame(columns=["Collector", "Repayment_amount"])
                new_row = {"Collector": collector, "Repayment_amount": amount}
                df_existing = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)
                try:
                    df_existing.to_excel(target_file, index=False)
                    st.success("Data berhasil ditambahkan ✅")
                    st.dataframe(df_existing)
                except Exception as e:
                    st.error(f"Gagal menyimpan data baru: {e}")

        # --- DATA PRIBADI USER (Excel kecil) ---
        st.subheader("📒 Data Pribadi User")
        user_data_file = f"user_data/{st.session_state.username}.xlsx"
        if not os.path.exists(user_data_file):
            df_user = pd.DataFrame({
                "Kolom1": pd.Series(dtype="str"),
                "Kolom2": pd.Series(dtype="str"),
                "Kolom3": pd.Series(dtype="float"),
                "Kolom4": pd.Series(dtype="float")
            })
            df_user.to_excel(user_data_file, index=False)
        else:
            df_user = pd.read_excel(user_data_file, dtype={"Kolom1": str, "Kolom2": str, "Kolom3": float, "Kolom4": float})
        st.write("Data pribadi kamu (seperti Excel):")
        edited_df = st.data_editor(df_user, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Simpan Data Pribadi"):
            try:
                edited_df.to_excel(user_data_file, index=False)
                st.success("Data pribadi berhasil disimpan ✅")
            except Exception as e:
                st.error(f"Gagal menyimpan data pribadi: {e}")

        # --- NOTED PRIBADI ---
        st.subheader("📝 Noted Pribadi")
        notes_file = f"user_data/{st.session_state.username}_notes.txt"
        if not os.path.exists(notes_file):
            with open(notes_file, "w", encoding="utf-8") as f:
                f.write("")
        with open(notes_file, "r", encoding="utf-8") as f:
            current_notes = f.read()
        new_notes = st.text_area("Tulis catatan pribadimu di sini:", current_notes, height=200)
        if st.button("💾 Simpan Noted"):
            with open(notes_file, "w", encoding="utf-8") as f:
                f.write(new_notes)
            st.success("Catatan berhasil disimpan ✅")

    # ===================== GROUP CHAT =====================
    elif report_option == '💬 Group Chat':
        st.header("💬 Group Chat Dashboard S2")
        chat_file = "user_data/group_chat.csv"
        if not os.path.exists(chat_file):
            df_chat = pd.DataFrame(columns=["id", "username", "time", "message", "file_path"])
            df_chat.to_csv(chat_file, index=False)
        df_chat = pd.read_csv(chat_file)

        # cek pesan baru untuk notif berdasarkan last_seen
        last_seen_file = f"user_data/last_seen_{st.session_state.username}_group.txt"
        if os.path.exists(last_seen_file):
            with open(last_seen_file, "r") as f:
                last_seen = f.read().strip()
        else:
            last_seen = "0000-00-00 00:00:00"
        new_msgs = df_chat[df_chat["time"] > last_seen] if not df_chat.empty else pd.DataFrame()
        if not new_msgs.empty and new_msgs.iloc[-1]["username"] != st.session_state.username:
            show_notification(f"{len(new_msgs)} pesan baru di Group Chat!")
        # update last_seen
        if not df_chat.empty:
            with open(last_seen_file, "w") as f:
                f.write(df_chat.iloc[-1]["time"])

        # auto refresh grup chat
        st_autorefresh(interval=1500, limit=None, key="chat_refresh")

        # tampilkan pesan
        if not df_chat.empty:
            for idx, row in df_chat.iterrows():
                # handle deleted marker
                if str(row.get('message', '')) == "__deleted__":
                    with st.chat_message("user"):
                        st.markdown(f"**{row.get('username')} ({row.get('time')})**: 🗑 Pesan ini telah dihapus")
                else:
                    display_message(row)
                    # tombol hapus hanya untuk pengirim
                    if row.get('username') == st.session_state.username:
                        if st.button("Hapus", key=f"del_{idx}"):
                            df_chat.loc[idx, "message"] = "__deleted__"
                            df_chat.to_csv(chat_file, index=False)
                            st.rerun()
        else:
            st.info("Belum ada chat, ayo mulai ngobrol 🚀")

        col1, col2 = st.columns([3, 1])
        with col1:
            mention_users = st.selectbox("👥 Tag anggota (opsional)", ["-"] + list(USER_CREDENTIALS.keys()))
            new_msg = st.chat_input("Ketik pesanmu di sini...")
            if mention_users != "-" and new_msg:
                new_msg = f"@{mention_users} {new_msg}"
        with col2:
            uploaded_file = st.file_uploader("📷", type=["png", "jpg", "jpeg", "pdf", "zip", "xlsx", "xls", "csv", "txt"], label_visibility="collapsed")

        if new_msg:
            now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([{
                "id": len(df_chat) + 1,
                "username": st.session_state.username,
                "time": now,
                "message": new_msg,
                "file_path": None
            }])
            df_chat = pd.concat([df_chat, new_row], ignore_index=True)
            df_chat.to_csv(chat_file, index=False)
            st.rerun()

        if uploaded_file:
            now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
            safe_name = sanitize_filename(f"{st.session_state.username}_{now.replace(':', '-')}_{uploaded_file.name}")
            save_path = os.path.join("user_data", "chat_images", safe_name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            df_chat = pd.read_csv(chat_file)  # reload because may changed
            new_row = pd.DataFrame([{
                "id": len(df_chat) + 1,
                "username": st.session_state.username,
                "time": now,
                "message": f"__img__:{save_path}",
                "file_path": save_path
            }])
            df_chat = pd.concat([df_chat, new_row], ignore_index=True)
            df_chat.to_csv(chat_file, index=False)
            st.rerun()

    # ===================== PRIVATE CHAT =====================
    elif report_option == '📩 Private Chat':
        st.header("📩 Private Chat")
        chat_dir = "user_data/private_chats"
        os.makedirs(chat_dir, exist_ok=True)
        all_users = list(USER_CREDENTIALS.keys())
        if st.session_state.username in all_users:
            all_users.remove(st.session_state.username)
        target_user = st.selectbox("Pilih user untuk private chat:", all_users) if all_users else None
        if target_user:
            users_pair = "_".join(sorted([st.session_state.username, target_user]))
            chat_file = os.path.join(chat_dir, f"{users_pair}.csv")
            if not os.path.exists(chat_file):
                df_chat = pd.DataFrame(columns=["id", "username", "time", "message", "file_path"])
                df_chat.to_csv(chat_file, index=False)
            df_chat = pd.read_csv(chat_file)

            # new message notif
            last_seen_file = f"user_data/last_seen_{st.session_state.username}_{target_user}.txt"
            if os.path.exists(last_seen_file):
                with open(last_seen_file, "r") as f:
                    last_seen = f.read().strip()
            else:
                last_seen = "0000-00-00 00:00:00"
            new_msgs = df_chat[(df_chat["time"] > last_seen) & (df_chat["username"] != st.session_state.username)] if not df_chat.empty else pd.DataFrame()
            if not new_msgs.empty:
                show_notification(f"{len(new_msgs)} pesan baru dari {target_user}")
            if not df_chat.empty:
                with open(last_seen_file, "w") as f:
                    f.write(df_chat.iloc[-1]["time"])

            st_autorefresh(interval=1500, limit=None, key="private_refresh")

            if not df_chat.empty:
                for idx, row in df_chat.iterrows():
                    if str(row.get('message', '')) == "__deleted__":
                        role = "assistant" if row.get('username') == st.session_state.username else "user"
                        with st.chat_message(role):
                            st.markdown(f"**{row.get('username')} ({row.get('time')})**: 🗑 Pesan ini telah dihapus")
                    else:
                        display_message(row)
                        if row.get('username') == st.session_state.username:
                            if st.button("Hapus", key=f"del_priv_{idx}"):
                                df_chat.loc[idx, "message"] = "__deleted__"
                                df_chat.to_csv(chat_file, index=False)
                                st.rerun()
            else:
                st.info(f"Belum ada chat dengan {target_user}")

            col1, col2 = st.columns([3, 1])
            with col1:
                new_msg = st.chat_input(f"Ketik pesan ke {target_user}...")
            with col2:
                uploaded_file = st.file_uploader("📷", type=["png", "jpg", "jpeg", "pdf", "zip", "xlsx", "xls", "csv", "txt"], label_visibility="collapsed")

            if new_msg:
                now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame([{
                    "id": len(df_chat) + 1,
                    "username": st.session_state.username,
                    "time": now,
                    "message": new_msg,
                    "file_path": None
                }])
                df_chat = pd.concat([df_chat, new_row], ignore_index=True)
                df_chat.to_csv(chat_file, index=False)
                st.rerun()

            if uploaded_file:
                now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
                safe_name = sanitize_filename(f"{st.session_state.username}_{now.replace(':', '-')}_{uploaded_file.name}")
                save_path = os.path.join("user_data", "chat_images", safe_name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                df_chat = pd.read_csv(chat_file)
                new_row = pd.DataFrame([{
                    "id": len(df_chat) + 1,
                    "username": st.session_state.username,
                    "time": now,
                    "message": f"__img__:{save_path}",
                    "file_path": save_path
                }])
                df_chat = pd.concat([df_chat, new_row], ignore_index=True)
                df_chat.to_csv(chat_file, index=False)
                st.rerun()

    # ===================== FILE MANAGER =====================
    elif report_option == '📂 File Manager':
        st.header("📂 File Manager (File pribadi per akun)")
        UPLOAD_ROOT = os.path.join("user_data", "uploads")
        user_dir = os.path.join(UPLOAD_ROOT, st.session_state.username)
        os.makedirs(user_dir, exist_ok=True)
        uploaded_files = st.file_uploader(
            "Upload file (xlsx, csv, txt, pdf, png, jpg, jpeg) — file hanya untuk akunmu",
            type=["xlsx", "xls", "csv", "txt", "pdf", "png", "jpg", "jpeg"],
            accept_multiple_files=True
        )
        if uploaded_files:
            for uploaded_file in uploaded_files:
                safe_name = sanitize_filename(uploaded_file.name)
                timestamp = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y%m%d_%H%M%S")
                save_name = f"{timestamp}_{safe_name}"
                save_path = os.path.join(user_dir, save_name)
                try:
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"✅ File disimpan: {save_name}")
                    ext = safe_name.split(".")[-1].lower()
                    try:
                        if ext in ("xlsx", "xls"):
                            df = pd.read_excel(save_path)
                            st.dataframe(df)
                        elif ext == "csv":
                            df = pd.read_csv(save_path)
                            st.dataframe(df)
                        elif ext == "txt":
                            with open(save_path, "r", encoding="utf-8", errors="ignore") as f:
                                st.text_area("Isi TXT:", f.read(), height=200)
                        elif ext in ("png", "jpg", "jpeg"):
                            st.image(save_path, width=300)
                        elif ext == "pdf":
                            st.info("PDF berhasil diupload — preview PDF tidak tersedia.")
                    except Exception as e:
                        st.warning(f"Preview gagal: {e}")
                except Exception as e:
                    st.error(f"Gagal menyimpan file: {e}")

        st.markdown("---")
        st.subheader("📑 File kamu")
        files = sorted(os.listdir(user_dir), reverse=True)
        if files:
            for fname in files:
                file_path = os.path.join(user_dir, fname)
                col1, col2, col3 = st.columns([6, 1, 1])
                with col1:
                    st.write(fname)
                with col2:
                    try:
                        with open(file_path, "rb") as f:
                            st.download_button("⬇️", f, file_name=fname, key=f"dl_{fname}")
                    except Exception:
                        st.error("Download gagal")
                with col3:
                    if st.button("🗑️", key=f"del_{fname}"):
                        os.remove(file_path)
                        st.warning(f"{fname} dihapus")
                        st.rerun()
        else:
            st.info("Belum ada file.")

    # ===================== SETTINGS =====================
    elif report_option == '⚙️ Settings':
        st.info(f"👤 Username aktif: {st.session_state.get('username', 'Tidak ditemukan')}")
        st.header("⚙️ Pengaturan Akun")

        # --- FOTO PROFIL ---
        st.subheader("🖼 Ganti Foto Profil")
        profile_pic_path = f"user_data/profile_pics/{st.session_state.username}.png"
        if os.path.exists(profile_pic_path):
            st.image(profile_pic_path, width=100, caption="Foto Profil Saat Ini")
        if st.button("🗑 Hapus Foto Profil"):
            if os.path.exists(profile_pic_path):
                os.remove(profile_pic_path)
                st.success("Foto profil berhasil dihapus ❌")
                st.rerun()
            else:
                st.info("Foto profil tidak ditemukan.")
        uploaded_image = st.file_uploader("Upload foto baru (.png, .jpg, .jpeg)", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            with open(profile_pic_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
            st.success("Foto profil berhasil diperbarui ✅")
            st.rerun()

        # --- GANTI PASSWORD ---
        st.subheader("🔑 Ganti Password")
        creds = load_json_safe(CREDENTIALS_FILE)
        old_password = st.text_input("Password Lama", type="password")
        new_password = st.text_input("Password Baru", type="password")
        confirm_password = st.text_input("Konfirmasi Password Baru", type="password")
        if st.button("Ubah Password"):
            if st.session_state.username not in creds:
                st.error("Akun tidak ditemukan di database ❌")
            else:
                current_password = creds[st.session_state.username]["password"]
                if old_password != current_password:
                    st.error("Password lama salah ❌")
                elif new_password != confirm_password:
                    st.error("Konfirmasi password tidak cocok ❌")
                elif new_password == "":
                    st.warning("Password baru tidak boleh kosong")
                else:
                    creds[st.session_state.username]["password"] = new_password
                    save_json_safe(CREDENTIALS_FILE, creds)
                    st.success("Password berhasil diubah dan disimpan permanen ✅")

        # --- HAPUS CHAT GRUP ---
        st.subheader("🧹 Hapus Riwayat Chat Grup")
        if st.button("🗑 Hapus Semua Chat Grup"):
            chat_file = "user_data/group_chat.csv"
            if os.path.exists(chat_file):
                df_empty = pd.DataFrame(columns=["id", "username", "time", "message", "file_path"])
                df_empty.to_csv(chat_file, index=False)
                st.success("Riwayat chat grup berhasil dihapus ✅")
            else:
                st.info("Belum ada chat grup untuk dihapus.")

        # --- HAPUS CHAT PRIVAT ---
        st.subheader("🧹 Hapus Riwayat Chat Privat")
        chat_dir = "user_data/private_chats"
        if os.path.exists(chat_dir):
            user_files = [f for f in os.listdir(chat_dir) if st.session_state.username in f]
            if user_files:
                for file in user_files:
                    display_name = file.replace('.csv', '').replace(st.session_state.username, '').replace('_', '')
                    if st.button(f"🗑 Hapus Chat dengan {display_name}", key=f"del_hist_{file}"):
                        os.remove(os.path.join(chat_dir, file))
                        st.success(f"Riwayat chat privat dengan {display_name} berhasil dihapus ✅")
            else:
                st.info("Tidak ada riwayat chat privat.")
        else:
            st.info("Folder chat privat belum dibuat.")

    # ===================== LOGOUT =====================
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
