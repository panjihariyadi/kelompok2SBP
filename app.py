import streamlit as st
import json
import os

st.set_page_config(
    page_title="Sistem Pakar Diagnosa Laptop",
    page_icon="💻",
    layout="centered"
)

GEJALA_FILE = "gejala.json"
RULES_FILE = "rules.json"


# ===================== UTIL =====================
def load_json(file):
    if not os.path.exists(file):
        return {} if "gejala" in file else []
    with open(file, "r") as f:
        return json.load(f)


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)


gejala = load_json(GEJALA_FILE)
rules = load_json(RULES_FILE)


# ===================== SESSION STATE =====================
if "page" not in st.session_state:
    st.session_state.page = "diagnosa"

if "flash_success" not in st.session_state:
    st.session_state.flash_success = None


# ===================== SIDEBAR MENU (NO SELECTBOX) =====================
st.sidebar.title("📂 Menu Sistem")

if st.sidebar.button("🔍 Diagnosa Kerusakan", use_container_width=True):
    st.session_state.page = "diagnosa"

if st.sidebar.button("🧠 Manajemen Gejala", use_container_width=True):
    st.session_state.page = "gejala"

if st.sidebar.button("📐 Manajemen Rule", use_container_width=True):
    st.session_state.page = "rule"


# ===================== FLASH MESSAGE =====================
if st.session_state.flash_success:
    st.success(st.session_state.flash_success)
    st.session_state.flash_success = None


# =================================================
# 🔍 DIAGNOSA
# =================================================
if st.session_state.page == "diagnosa":
    st.title("🔍 Diagnosa Kerusakan Laptop")
    st.caption("Mode teknisi – analisis awal berdasarkan gejala")

    kategori = {}
    for kode, g in gejala.items():
        kategori.setdefault(g["kategori"], []).append((kode, g["nama"]))

    selected = []

    for kat, items in kategori.items():
        with st.expander(f"Kategori: {kat}"):
            for kode, nama in items:
                if st.checkbox(nama, key=f"chk_{kode}"):
                    selected.append(kode)

    if st.button("🔎 Analisa Kerusakan", use_container_width=True):
        hasil = []

        for rule in rules:
            cocok = [g for g in rule["gejala"] if g in selected]
            if cocok:
                hasil.append((rule, cocok))

        if not hasil:
            st.warning("Tidak ditemukan kecocokan rule.")
        else:
            for rule, cocok in hasil:
                st.error(f"🔧 Kerusakan: {rule['kerusakan']}")

                st.markdown("**Gejala terdeteksi:**")
                for g in cocok:
                    st.markdown(f"- {gejala[g]['nama']}")

                st.markdown(f"**Tingkat Kerusakan:** {rule['tingkat']}")

                st.markdown("**Langkah Cek Awal:**")
                for c in rule["cek"]:
                    st.markdown(f"- {c}")

                st.success(f"**Rekomendasi:** {rule['solusi']}")
                st.divider()


# =================================================
# 🧠 CRUD GEJALA
# =================================================
elif st.session_state.page == "gejala":
    st.title("🧠 Manajemen Basis Pengetahuan – Gejala")

    # ---------- CREATE ----------
    st.subheader("➕ Tambah Gejala")
    with st.form("add_gejala", clear_on_submit=True):
        kode = st.text_input("Kode Gejala (contoh: g30)")
        nama = st.text_input("Nama Gejala")
        kategori_baru = st.text_input("Kategori")
        submit = st.form_submit_button("Simpan")

        if submit:
            if not kode or not nama or not kategori_baru:
                st.warning("Semua field wajib diisi")
            elif kode in gejala:
                st.error("Kode gejala sudah ada")
            else:
                gejala[kode] = {
                    "nama": nama,
                    "kategori": kategori_baru
                }
                save_json(GEJALA_FILE, gejala)
                st.session_state.flash_success = "✅ Gejala berhasil ditambahkan"
                st.rerun()

    st.divider()

    # ---------- UPDATE & DELETE ----------
    st.subheader("✏️ Edit / 🗑️ Hapus Gejala")

    pilih = st.selectbox("Pilih Gejala", list(gejala.keys()))

    nama_edit = st.text_input("Nama Gejala", gejala[pilih]["nama"])
    kategori_edit = st.text_input("Kategori", gejala[pilih]["kategori"])

    col1, col2 = st.columns(2)

    # UPDATE
    with col1:
        if st.button("💾 Update Gejala", use_container_width=True):
            gejala[pilih] = {
                "nama": nama_edit,
                "kategori": kategori_edit
            }
            save_json(GEJALA_FILE, gejala)
            st.session_state.flash_success = "✏️ Gejala berhasil diperbarui"
            st.rerun()

    # DELETE
    with col2:
        if st.button("🗑️ Hapus Gejala", use_container_width=True):
            st.session_state.confirm_delete = pilih

    # ---------- CONFIRM DIALOG ----------
    if "confirm_delete" in st.session_state:

        @st.dialog("Konfirmasi Penghapusan")
        def confirm_delete_dialog():
            kode = st.session_state.confirm_delete
            st.error(f"⚠️ Yakin ingin menghapus gejala:\n\n**{gejala[kode]['nama']}** ?")

            col_yes, col_no = st.columns(2)

            with col_yes:
                if st.button("✅ Yes, Hapus"):
                    del gejala[kode]
                    save_json(GEJALA_FILE, gejala)
                    del st.session_state.confirm_delete
                    st.session_state.flash_success = "🗑️ Gejala berhasil dihapus"
                    st.rerun()

            with col_no:
                if st.button("❌ Cancel"):
                    del st.session_state.confirm_delete
                    st.info("Penghapusan dibatalkan")

        confirm_delete_dialog()


# =================================================
# 📐 CRUD RULE
# =================================================
elif st.session_state.page == "rule":
    st.title("📐 Manajemen Rule Diagnosa")

    st.subheader("➕ Tambah Rule")
    with st.form("add_rule"):
        kerusakan = st.text_input("Nama Kerusakan")
        tingkat = st.selectbox("Tingkat Kerusakan", ["Ringan", "Sedang", "Berat"])
        gejala_rule = st.multiselect("Gejala Terkait", list(gejala.keys()))
        cek = st.text_area("Langkah Cek Awal (1 baris = 1 langkah)")
        solusi = st.text_area("Rekomendasi")
        submit_rule = st.form_submit_button("Simpan Rule")

        if submit_rule:
            if not kerusakan or not gejala_rule:
                st.warning("Nama kerusakan dan gejala wajib diisi")
            else:
                rules.append({
                    "kerusakan": kerusakan,
                    "gejala": gejala_rule,
                    "tingkat": tingkat,
                    "cek": cek.split("\n"),
                    "solusi": solusi
                })
                save_json(RULES_FILE, rules)
                st.session_state.flash_success = "📐 Rule berhasil ditambahkan"
                st.rerun()

    st.divider()

    st.subheader("📋 Daftar Rule")
    for r in rules:
        with st.expander(r["kerusakan"]):
            st.write("Gejala:", r["gejala"])
            st.write("Tingkat:", r["tingkat"])
            st.write("Cek Awal:", r["cek"])
            st.write("Solusi:", r["solusi"])
