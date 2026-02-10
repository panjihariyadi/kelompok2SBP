import streamlit as st

# Setup dasar
st.set_page_config(page_title="Diagnosa Laptop Kelompok 2", page_icon="💻", layout="centered")

# Header yang gak kaku
st.markdown("<h1 style='text-align: center;'>💻 Cek Gejala Laptop</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>By: Kelompok 2 Cihuy</p>", unsafe_allow_html=True)
st.markdown("---")

# 1. KATEGORI LAYAR
with st.expander("🖥️ Masalah Layar", expanded=True):
    l1 = st.checkbox("Layar bergaris atau kedip-kedip")
    l2 = st.checkbox("Layar redup banget (tapi mesin nyala)")
    if l1 or l2:
        st.info("📌 **Info Teknis:** Coba colok ke monitor luar/TV. Kalau di TV gambarnya bagus, berarti panel LCD kamu yang kena. Kalau di TV juga rusak, berarti mesin (VGA) yang bermasalah.")

# 2. KATEGORI POWER & MATI TOTAL
with st.expander("🔌 Masalah Power & Mesin"):
    p1 = st.checkbox("Laptop mati total (gak ada lampu sama sekali)")
    p2 = st.checkbox("Ada bau hangus atau percikan api")
    p3 = st.checkbox("Lampu indikator casan mati pas dicolok")
    if p1 and p2:
        st.error("⚠️ **Peringatan:** Ini indikasi konslet di Motherboard. Jangan dicolok casan lagi, bahaya!")
    elif p1 and p3:
        st.warning("🧐 **Analisis:** Listrik gak masuk. Cek kabel charger kamu atau lubang colokannya mungkin rusak.")

# 3. KATEGORI SUHU
with st.expander("❄️ Masalah Panas"):
    s1 = st.checkbox("Laptop tiba-tiba mati pas lagi dipake berat")
    s2 = st.checkbox("Suara kipas kenceng banget kayak mesin jet")
    if s1 and s2:
        st.error("🔥 **Diagnosa:** Overheat! Kipas kotor atau pasta prosesor udah kering. Perlu dibongkar buat dibersihin.")

st.markdown("---")

# RINGKASAN DIAGNOSA (Untuk Laporan)
if st.button("TAMPILKAN RINGKASAN UNTUK LAPORAN", use_container_width=True):
    st.subheader("📋 Hasil Diagnosa Akhir:")
    dapet = False
    
    if l1 or l2:
        st.error("**K01 - Kerusakan Panel LCD** (Berdasarkan gejala visual)")
        dapet = True
    if (p1 and p2) or (p1 and p3):
        st.error("**K02 - Kerusakan Motherboard / Jalur Power**")
        dapet = True
    if s1 and s2:
        st.error("**K03 - Kerusakan Sistem Pendingin (Overheat)**")
        dapet = True
        
    if not dapet:
        st.write("Silakan pilih gejala dulu buat liat hasilnya.")