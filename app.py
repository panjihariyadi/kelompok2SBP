import streamlit as st
import json
import os

# ===================== CONFIG =====================
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

# ===================== SESSION =====================
if "page" not in st.session_state:
    st.session_state.page = "diagnosa"
if "flash" not in st.session_state:
    st.session_state.flash = None

# ===================== SIDEBAR =====================
st.sidebar.title("📂 Menu Sistem")

if st.sidebar.button("🔍 Diagnosa Kerusakan", use_container_width=True):
    st.session_state.page = "diagnosa"

if st.sidebar.button("🧠 Manajemen Gejala", use_container_width=True):
    st.session_state.page = "gejala"

if st.sidebar.button("📐 Manajemen Rule", use_container_width=True):
    st.session_state.page = "rule"

st.sidebar.markdown("---")
st.sidebar.caption("👥 Kelompok 2 Y7C")
st.sidebar.caption("📘 Sistem Berbasis Pengetahuan")
st.sidebar.caption("© 2026")

# ===================== FLASH =====================
if st.session_state.flash:
    st.success(st.session_state.flash)
    st.session_state.flash = None

# =================================================
# 🔍 DIAGNOSA
# =================================================
if st.session_state.page == "diagnosa":
    st.title("🔍 Diagnosa Kerusakan Laptop")
    st.caption("Sistem ini memberikan indikasi awal kemungkinan kerusakan software atau hardware")

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
# 🧠 CRUD GEJALA (CREATE + UPDATE + DELETE)
# =================================================
elif st.session_state.page == "gejala":
    st.title("🧠 Manajemen Basis Pengetahuan – Gejala")

    # ---------- CREATE ----------
    st.subheader("➕ Tambah Gejala")
    with st.form("add_gejala", clear_on_submit=True):
        kode = st.text_input("Kode Gejala (contoh: g40)")
        nama = st.text_input("Nama Gejala")
        kategori_baru = st.text_input("Kategori")
        submit = st.form_submit_button("Simpan")

        if submit:
            if not kode or not nama or not kategori_baru:
                st.warning("Semua field wajib diisi")
            elif kode in gejala:
                st.error("Kode gejala sudah ada")
            else:
                gejala[kode] = {"nama": nama, "kategori": kategori_baru}
                save_json(GEJALA_FILE, gejala)
                st.session_state.flash = "✅ Gejala berhasil ditambahkan"
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
            st.session_state.flash = "✏️ Gejala berhasil diperbarui"
            st.rerun()

    # DELETE
    with col2:
        if st.button("🗑️ Hapus Gejala", use_container_width=True):
            st.session_state.confirm_delete_gejala = pilih

    if "confirm_delete_gejala" in st.session_state:

        @st.dialog("Konfirmasi Penghapusan Gejala")
        def confirm_delete_gejala():
            kode = st.session_state.confirm_delete_delete_gejala if False else st.session_state.confirm_delete_gejala
            st.error(f"Yakin ingin menghapus gejala:\n\n**{gejala[kode]['nama']}** ?")

            col_y, col_n = st.columns(2)
            with col_y:
                if st.button("✅ Yes, Hapus"):
                    del gejala[kode]
                    save_json(GEJALA_FILE, gejala)
                    del st.session_state.confirm_delete_gejala
                    st.session_state.flash = "🗑️ Gejala berhasil dihapus"
                    st.rerun()

            with col_n:
                if st.button("❌ Cancel"):
                    del st.session_state.confirm_delete_gejala
                    st.info("Penghapusan dibatalkan")

        confirm_delete_gejala()

# =================================================
# 📐 CRUD RULE (LENGKAP)
# =================================================
elif st.session_state.page == "rule":
    st.title("📐 Manajemen Rule Diagnosa")

    # ---------- CREATE RULE ----------
    st.subheader("➕ Tambah Rule")
    with st.form("add_rule", clear_on_submit=True):
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
                st.session_state.flash = "📐 Rule berhasil ditambahkan"
                st.rerun()

    st.divider()

    # ---------- EDIT & DELETE RULE ----------
    st.subheader("✏️ Edit / 🗑️ Hapus Rule")

    rule_names = [r["kerusakan"] for r in rules]
    idx = st.selectbox("Pilih Rule", range(len(rule_names)), format_func=lambda i: rule_names[i])
    rule = rules[idx]

    with st.form("edit_rule"):
        nama = st.text_input("Nama Kerusakan", rule["kerusakan"])
        tingkat = st.selectbox(
            "Tingkat Kerusakan",
            ["Ringan", "Sedang", "Berat"],
            index=["Ringan", "Sedang", "Berat"].index(rule["tingkat"])
        )
        gejala_edit = st.multiselect("Gejala Terkait", list(gejala.keys()), default=rule["gejala"])
        cek = st.text_area("Langkah Cek Awal", "\n".join(rule["cek"]))
        solusi = st.text_area("Rekomendasi", rule["solusi"])
        update_btn = st.form_submit_button("Update Rule")

        if update_btn:
            rules[idx] = {
                "kerusakan": nama,
                "gejala": gejala_edit,
                "tingkat": tingkat,
                "cek": cek.split("\n"),
                "solusi": solusi
            }
            save_json(RULES_FILE, rules)
            st.session_state.flash = "✏️ Rule berhasil diperbarui"
            st.rerun()

    if st.button("🗑️ Hapus Rule", use_container_width=True):
        st.session_state.confirm_delete_rule = idx

    if "confirm_delete_rule" in st.session_state:

        @st.dialog("Konfirmasi Penghapusan Rule")
        def confirm_delete_rule():
            r = rules[st.session_state.confirm_delete_rule]
            st.error(f"Yakin ingin menghapus rule:\n\n**{r['kerusakan']}** ?")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, Hapus"):
                    rules.pop(st.session_state.confirm_delete_rule)
                    save_json(RULES_FILE, rules)
                    del st.session_state.confirm_delete_rule
                    st.session_state.flash = "🗑️ Rule berhasil dihapus"
                    st.rerun()

            with col2:
                if st.button("❌ Cancel"):
                    del st.session_state.confirm_delete_rule
                    st.info("Penghapusan dibatalkan")

        confirm_delete_rule()
