import streamlit as st

st.set_page_config(page_title="Sistem Pakar Laptop Pro", page_icon="💻", layout="centered")

# Header
st.markdown("<h1 style='text-align: center;'>💻 Sistem Pakar Laptop (Pro)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Transparansi Diagnosa Berbasis Gejala</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Oleh: Kelompok 2 Cihuy</p>", unsafe_allow_html=True)
st.markdown("---")

# Dictionary Label
labels = {
    "g01": "Sering Blue Screen (BSOD)", "g02": "Bunyi beep berulang saat nyala", "g03": "Aplikasi sering Force Close",
    "g04": "Booting sangat lama (>3 menit)", "g05": "Pesan 'No Bootable Device'", "g18": "Laptop freeze saat buka file",
    "g19": "Gagal install ulang Windows", "g20": "Sering muncul 'Disk Error'", "g21": "Folder mendadak hilang/corrupt",
    "g22": "Bunyi klik/detak di dalam laptop", "g16": "Laptop mati total (No Power)", "g17": "Ada bau hangus/percikan api",
    "g23": "Lampu indikator power kedip", "g24": "Port USB tidak berfungsi", "g25": "Webcam tidak terdeteksi",
    "g26": "Wi-Fi/Bluetooth hilang", "g27": "Waktu BIOS selalu berubah", "g06": "Mati mendadak saat tugas berat",
    "g07": "Body bawah sangat panas", "g08": "Fan berisik (seperti mesin)", "g28": "Fan tidak terasa ada hembusan",
    "g29": "Performa melambat saat panas", "g30": "Muncul peringatan 'Fan Error'", "g31": "Keyboard terasa panas",
    "g32": "Laptop tiba-tiba restart", "g09": "Baterai 'Not Charging'", "g10": "Mati saat kabel dicabut",
    "g33": "Baterai cepat habis (Drop)", "g34": "Body baterai terlihat kembung", "g35": "Charger terasa sangat panas",
    "g36": "Konektor charger longgar", "g37": "Lampu indikator charge mati", "g11": "Layar bergaris vertikal/horisontal",
    "g12": "Layar flicker/berkedip", "g13": "Layar sangat redup (backlight mati)", "g38": "Layar putih polos (White Screen)",
    "g39": "Ada bercak hitam (Dead Pixel)", "g40": "Warna layar berubah/pudar", "g41": "Layar goyang saat disentuh",
    "g42": "Muncul bayangan (Ghosting)", "g14": "Beberapa tombol mati", "g15": "Ghost Typing (Ketik sendiri)",
    "g43": "Tombol terasa lengket/keras", "g44": "Touchpad tidak bisa klik kiri/kanan", "g45": "Kursor lari-lari sendiri",
    "g47": "Touchpad mati total", "g48": "Bunyi bip saat tekan tombol",
    "g49": "Angka muncul saat tekan huruf", "g50": "Input delay (lambat ngetik)"
}

st.subheader("Centang Gejala yang Muncul:")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**RAM & Storage**")
    v01 = st.checkbox(labels["g01"]); v02 = st.checkbox(labels["g02"]); v03 = st.checkbox(labels["g03"])
    v04 = st.checkbox(labels["g04"]); v05 = st.checkbox(labels["g05"]); v18 = st.checkbox(labels["g18"])
    v19 = st.checkbox(labels["g19"]); v20 = st.checkbox(labels["g20"]); v21 = st.checkbox(labels["g21"]); v22 = st.checkbox(labels["g22"])
    st.markdown("**Motherboard**")
    v16 = st.checkbox(labels["g16"]); v17 = st.checkbox(labels["g17"]); v23 = st.checkbox(labels["g23"])
    v24 = st.checkbox(labels["g24"]); v25 = st.checkbox(labels["g25"]); v26 = st.checkbox(labels["g26"]); v27 = st.checkbox(labels["g27"])

with col2:
    st.markdown("**Suhu & Cooling**")
    v06 = st.checkbox(labels["g06"]); v07 = st.checkbox(labels["g07"]); v08 = st.checkbox(labels["g08"])
    v28 = st.checkbox(labels["g28"]); v29 = st.checkbox(labels["g29"]); v30 = st.checkbox(labels["g30"])
    v31 = st.checkbox(labels["g31"]); v32 = st.checkbox(labels["g32"])
    st.markdown("**Baterai & Charger**")
    v09 = st.checkbox(labels["g09"]); v10 = st.checkbox(labels["g10"]); v33 = st.checkbox(labels["g33"])
    v34 = st.checkbox(labels["g34"]); v35 = st.checkbox(labels["g35"]); v36 = st.checkbox(labels["g36"]); v37 = st.checkbox(labels["g37"])

with col3:
    st.markdown("**LCD & Visual**")
    v11 = st.checkbox(labels["g11"]); v12 = st.checkbox(labels["g12"]); v13 = st.checkbox(labels["g13"])
    v38 = st.checkbox(labels["g38"]); v39 = st.checkbox(labels["g39"]); v40 = st.checkbox(labels["g40"])
    v41 = st.checkbox(labels["g41"]); v42 = st.checkbox(labels["g42"])
    st.markdown("**Keyboard & Touchpad**")
    v14 = st.checkbox(labels["g14"]); v15 = st.checkbox(labels["g15"]); v43 = st.checkbox(labels["g43"])
    v44 = st.checkbox(labels["g44"]); v45 = st.checkbox(labels["g45"]); v47 = st.checkbox(labels["g47"])
    v48 = st.checkbox(labels["g48"]); v49 = st.checkbox(labels["g49"]); v50 = st.checkbox(labels["g50"])

st.markdown("---")

if st.button("MULAI ANALISIS HARDWARE", use_container_width=True):
    diagnosa = []
    
    def get_selected(ids):
        # Mengambil list gejala yang dicentang
        return [labels[i] for i in ids if globals().get(f"v{i[1:]}")]

    # LOGIKA RULES
    if (v01 and v02) or (v03 and v18 and v48):
        diagnosa.append({"n": "RAM (Memory)", "g": get_selected(["g01", "g02", "g03", "g18", "g48"]), "s": "Bersihkan pin RAM atau ganti modul."})
    
    if v04 or v05 or v19 or v20 or v21 or v22:
        diagnosa.append({"n": "Storage (HDD/SSD)", "g": get_selected(["g04", "g05", "g18", "g19", "g20", "g21", "g22"]), "s": "Cek kesehatan disk. Ganti ke SSD jika perlu."})
        
    if v06 or v07 or v08 or v28 or v29 or v30 or v31:
        diagnosa.append({"n": "Sistem Pendingin", "g": get_selected(["g06", "g07", "g08", "g28", "g29", "g30", "g31"]), "s": "Bersihkan fan & repaste thermal paste."})

    if v09 or v10 or v33 or v34 or v37:
        diagnosa.append({"n": "Baterai / Power Circuit", "g": get_selected(["g09", "g10", "g33", "g34", "g37"]), "s": "Cek cell baterai atau ganti unit baru."})

    if v11 or v12 or v13 or v38 or v39 or v40 or v41 or v42:
        diagnosa.append({"n": "Panel Layar LCD", "g": get_selected(["g11", "g12", "g13", "g38", "g39", "g40", "g41", "g42"]), "s": "Cek kabel fleksibel atau ganti panel."})

    if v14 or v15 or v43 or v44 or v45 or v47 or v49 or v50:
        diagnosa.append({"n": "Keyboard / Touchpad", "g": get_selected(["g14", "g15", "g43", "g44", "g45", "g47", "g49", "g50"]), "s": "Ganti modul keyboard atau bersihkan sirkuit."})

    if v16 or v17 or v23 or v24 or v25 or v26 or v27:
        diagnosa.append({"n": "Motherboard & IC Power", "g": get_selected(["g16", "g17", "g23", "g24", "g25", "g26", "g27"]), "s": "Butuh penanganan teknisi spesialis mesin."})

    # OUTPUT HASIL
    if diagnosa:
        st.subheader("Hasil Analisis Sistem:")
        for d in diagnosa:
            with st.container():
                st.error(f"### Kerusakan: {d['n']}")
                st.markdown("**Gejala yang terdeteksi:**")
                for g in d['g']:
                    st.markdown(f"- {g}")
                st.success(f"**Saran Perbaikan:** {d['s']}")
                st.markdown("---")
    else:
        st.warning("Gejala belum mencukupi untuk diagnosa otomatis.")