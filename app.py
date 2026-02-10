import streamlit as st

# Setup tab browser biar gak cuma tulisan 'streamlit'
st.set_page_config(page_title="Diagnosa Laptop Kelompok 2", page_icon="💻", layout="centered")

# --- BAGIAN ATAS (JUDUL) ---
st.markdown("<h1 style='text-align: center;'>💻 Cek Kerusakan Laptop</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Aplikasi ini bantu nebak laptop kamu kenapa-napa berdasarkan gejalanya.</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>By: Kelompok 2 Cihuy</p>", unsafe_allow_html=True)
st.markdown("---")

st.subheader("Pilih gejala yang muncul:")

# Isinya sama kayak tadi, cuma variabelnya dipendekin biar gak pusing bacanya
labels = {
    "g01": "Sering Blue Screen (BSOD)", "g02": "Bunyi beep berulang saat nyala", "g03": "Aplikasi sering Force Close",
    "g04": "Booting lama banget (>3 menit)", "g05": "Muncul 'No Bootable Device'", "g18": "Laptop freeze pas buka file",
    "g19": "Gagal pas install ulang Windows", "g20": "Muncul pesan 'Disk Error'", "g21": "Folder mendadak ilang/corrupt",
    "g22": "Ada bunyi klik/detak di dalem", "g16": "Mati total (Gak ada lampu nyala)", "g17": "Bau hangus atau ada percikan",
    "g23": "Lampu power cuma kedip-kedip", "g24": "Lubang USB gak fungsi", "g25": "Webcam gak kebaca",
    "g26": "Wi-Fi atau Bluetooth ilang", "g27": "Jam/Waktu BIOS ngaco terus", "g06": "Mati sendiri pas lagi kerja berat",
    "g07": "Body bawah panas banget", "g08": "Kipas berisik kyk mesin jet", "g28": "Kipas gak ada anginnya",
    "g29": "Laptop lemot pas udah panas", "g30": "Muncul tulisan 'Fan Error'", "g31": "Keyboard berasa panas",
    "g32": "Suka restart sendiri", "g09": "Dicas tapi gak nambah (Not Charging)", "g10": "Mati pas kabel casan dicabut",
    "g33": "Batre boros banget (Drop)", "g34": "Batre kelihatannya kembung", "g35": "Batok charger panas bgt",
    "g36": "Lobang charger goyang", "g37": "Lampu casan mati", "g11": "Layar bergaris",
    "g12": "Layar kedip-kedip (flicker)", "g13": "Layar redup bgt kyk mati", "g38": "Layar putih polos doang",
    "g39": "Ada titik item (Dead Pixel)", "g40": "Warna layar aneh/pudar", "g41": "Layar goyang pas disentuh",
    "g42": "Ada bayangan di layar", "g14": "Ada tombol yang gak fungsi", "g15": "Ngetik sendiri (Ghost Typing)",
    "g43": "Tombol keras atau lengket", "g44": "Klik kiri/kanan touchpad gak bisa", "g45": "Kursor lari-lari sendiri",
    "g47": "Touchpad mati total", "g48": "Bunyi 'tit' pas ngetik",
    "g49": "Ngetik huruf keluar angka", "g50": "Ngetik berasa delay"
}

# Bikin menu dropdown biar gak menuh-menuhin layar
kiri, kanan = st.columns(2)

with kiri:
    with st.expander("📁 Masalah RAM & Storage"):
        v01 = st.checkbox(labels["g01"]); v02 = st.checkbox(labels["g02"]); v03 = st.checkbox(labels["g03"])
        v04 = st.checkbox(labels["g04"]); v05 = st.checkbox(labels["g05"]); v18 = st.checkbox(labels["g18"])
        v19 = st.checkbox(labels["g19"]); v20 = st.checkbox(labels["g20"]); v21 = st.checkbox(labels["g21"]); v22 = st.checkbox(labels["g22"])

    with st.expander("🔌 Masalah Motherboard"):
        v16 = st.checkbox(labels["g16"]); v17 = st.checkbox(labels["g17"]); v23 = st.checkbox(labels["g23"])
        v24 = st.checkbox(labels["g24"]); v25 = st.checkbox(labels["g25"]); v26 = st.checkbox(labels["g26"]); v27 = st.checkbox(labels["g27"])

    with st.expander("❄️ Suhu & Kipas"):
        v06 = st.checkbox(labels["g06"]); v07 = st.checkbox(labels["g07"]); v08 = st.checkbox(labels["g08"])
        v28 = st.checkbox(labels["g28"]); v29 = st.checkbox(labels["g29"]); v30 = st.checkbox(labels["g30"])
        v31 = st.checkbox(labels["g31"]); v32 = st.checkbox(labels["g32"])

with kanan:
    with st.expander("🖥️ Masalah Layar"):
        v11 = st.checkbox(labels["g11"]); v12 = st.checkbox(labels["g12"]); v13 = st.checkbox(labels["g13"])
        v38 = st.checkbox(labels["g38"]); v39 = st.checkbox(labels["g39"]); v40 = st.checkbox(labels["g40"])
        v41 = st.checkbox(labels["g41"]); v42 = st.checkbox(labels["g42"])

    with st.expander("🔋 Batre & Casan"):
        v09 = st.checkbox(labels["g09"]); v10 = st.checkbox(labels["g10"]); v33 = st.checkbox(labels["g33"])
        v34 = st.checkbox(labels["g34"]); v35 = st.checkbox(labels["g35"]); v36 = st.checkbox(labels["g36"]); v37 = st.checkbox(labels["g37"])

    with st.expander("⌨️ Keyboard & Touchpad"):
        v14 = st.checkbox(labels["g14"]); v15 = st.checkbox(labels["g15"]); v43 = st.checkbox(labels["g43"])
        v44 = st.checkbox(labels["g44"]); v45 = st.checkbox(labels["g45"]); v47 = st.checkbox(labels["g47"])
        v48 = st.checkbox(labels["g48"]); v49 = st.checkbox(labels["g49"]); v50 = st.checkbox(labels["g50"])

st.markdown("---")

# --- BAGIAN LOGIKA (CORE NYA) ---
if st.button("CEK SEKARANG", use_container_width=True):
    hasil_akhir = [] # List buat nampung diagnosa yang cocok
    
    # Fungsi simpel buat narik teks gejala yang dicentang
    def dapet_gejala(list_id):
        return [labels[i] for i in list_id if globals().get(f"v{i[1:]}")]

    # Aturan mainnya (Rules). Pakai AND kalau butuh beberapa gejala barengan, pakai OR kalau satu aja udah cukup.
    if (v01 and v02) or (v03 and v18 and v48):
        hasil_akhir.append({"n": "RAM (Memory)", "g": dapet_gejala(["g01", "g02", "g03", "g18", "g48"]), "s": "Coba bersihin pin RAM pakai penghapus atau ganti RAM baru."})
    
    if v04 or v05 or v19 or v20 or v21 or v22:
        hasil_akhir.append({"n": "Penyimpanan (HDD/SSD)", "g": dapet_gejala(["g04", "g05", "g18", "g19", "g20", "g21", "g22"]), "s": "Buruan backup data! Disk kamu kyknya udah mau wassalam. Ganti ke SSD biar kenceng."})
        
    if v06 or v07 or v08 or v28 or v29 or v30 or v31:
        hasil_akhir.append({"n": "Laptop Kepanasan (Overheat)", "g": dapet_gejala(["g06", "g07", "g08", "g28", "g29", "g30", "g31"]), "s": "Bersihin debu di kipas terus ganti thermal paste-nya."})

    if v09 or v10 or v33 or v34 or v37:
        hasil_akhir.append({"n": "Masalah Batre", "g": dapet_gejala(["g09", "g10", "g33", "g34", "g37"]), "s": "Batre udah drop atau kembung. Ganti unit baru biar aman."})

    if v11 or v12 or v13 or v38 or v39 or v40 or v41 or v42:
        hasil_akhir.append({"n": "Masalah Layar (LCD)", "g": dapet_gejala(["g11", "g12", "g13", "g38", "g39", "g40", "g41", "g42"]), "s": "Cek kabel fleksibelnya, kalo tetep gitu ya harus ganti panel LCD."})

    if v14 or v15 or v43 or v44 or v45 or v47 or v49 or v50:
        hasil_akhir.append({"n": "Keyboard / Touchpad", "g": dapet_gejala(["g14", "g15", "g43", "g44", "g45", "g47", "g49", "g50"]), "s": "Ganti modul keyboard atau touchpadnya. Kalo kena air, langsung matiin laptopnya."})

    if v16 or v17 or v23 or v24 or v25 or v26 or v27:
        hasil_akhir.append({"n": "Motherboard (Mesin)", "g": dapet_gejala(["g16", "g17", "g23", "g24", "g25", "g26", "g27"]), "s": "Ini masalah berat. Harus dibawa ke tukang servis spesialis mesin."})

    # --- TAMPILIN HASILNYA ---
    if hasil_akhir:
        st.subheader("Hasil Cek:")
        for h in hasil_akhir:
            with st.container():
                st.error(f"### Kerusakan: {h['n']}")
                st.markdown("**Gejala yang kamu pilih:**")
                for g in h['g']:
                    st.markdown(f"- {g}")
                st.success(f"**Solusi:** {h['s']}")
                st.markdown("---")
    else:
        st.warning("Belum bisa nebak. Coba centang gejala yang lebih spesifik.")