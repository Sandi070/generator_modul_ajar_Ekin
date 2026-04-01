import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Konfigurasi Halaman (Harus diletakkan paling atas)
st.set_page_config(
    page_title="AI Generator Modul Ajar",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- FUNGSI MENGHITUNG TAHUN PELAJARAN OTOMATIS ---
def get_tahun_pelajaran():
    now = datetime.now()
    # Jika bulan sebelum Juli (Jan-Jun), berarti masih tahun ajaran tahun lalu/sekarang
    if now.month < 7:
        return f"{now.year - 1}/{now.year}"
    # Jika bulan Juli ke atas, berarti masuk tahun ajaran sekarang/tahun depan
    else:
        return f"{now.year}/{now.year + 1}"

# --- DESAIN HEADER ---
st.title("📚 AI Generator Modul Ajar")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 18px; margin-bottom: 20px;">
    <i>Pendekatan Deep Learning & Kurikulum Berbasis Cinta</i> 💖
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR UNTUK API KEY ---
with st.sidebar:
    st.header("⚙️ Pengaturan Sistem")
    st.markdown("Untuk menggunakan aplikasi ini, setiap guru harus memasukkan API Key masing-masing.")
    
    # Input API Key disembunyikan (tipe password)
    user_api_key = st.text_input("Masukkan Gemini API Key Anda:", type="password")
    
    st.markdown("---")
    st.markdown("**Belum punya API Key?**")
    st.markdown("[👉 Dapatkan gratis di sini](https://aistudio.google.com/)")
    st.markdown("*(Login dengan akun Google, lalu klik 'Get API key')*")

# --- FORMULIR UTAMA ---
st.markdown("### Lengkapi Data Pembelajaran")

col1, col2 = st.columns(2)

with col1:
    mapel = st.text_input("Mata Pelajaran", value="Kimia")
    fase = st.text_input("Fase / Kelas", value="F / XI")
    # Menu Tahun Pelajaran yang terisi otomatis berdasarkan tahun saat ini
    tahun = st.text_input("Tahun Pelajaran", value=get_tahun_pelajaran())

with col2:
    materi = st.text_input("Materi / Topik Pembelajaran", value="Pereaksi Pembatas")
    pendekatan = st.selectbox("Pendekatan Tambahan", [
        "Pendidikan Karakter",
        "Moderasi Beragama (Nilai-nilai Kemenag)",
        "Bilingual (Indonesia - Inggris)",
        "Berbasis TIK (PhET, Media Interaktif)",
        "Pembelajaran Inovatif (PBL / Gamifikasi)"
    ])

st.markdown("---")

# --- TOMBOL GENERATE ---
if st.button("✨ Buat Modul Ajar AI", use_container_width=True, type="primary"):
    
    # Validasi input
    if not user_api_key.strip():
        st.warning("⚠️ Silakan masukkan API Key di menu samping (sidebar) terlebih dahulu.")
    elif not mapel.strip() or not fase.strip() or not materi.strip() or not tahun.strip():
        st.warning("⚠️ Harap lengkapi semua kolom: Mata Pelajaran, Fase, Materi, dan Tahun Pelajaran!")
    else:
        try:
            with st.spinner("⏳ Sedang merakit modul pembelajaran dengan cinta..."):
                
                # Konfigurasi API
                genai.configure(api_key=user_api_key)
                
                # Menggunakan model Gemini sesuai preferensi Anda
                model = genai.GenerativeModel('gemini-flash-latest')
                
                # Menyusun Prompt (Menambahkan variabel {tahun} ke dalam instruksi)
                prompt_system = f"""
                Kamu adalah seorang ahli pendidikan dan penyusun kurikulum tingkat lanjut. Buatkan Modul Ajar (RPP) yang komprehensif untuk mata pelajaran {mapel}, Fase/Kelas {fase}, Tahun Pelajaran {tahun}, dengan topik "{materi}".

                WAJIB GUNAKAN FORMAT BERIKUT (Format tebal/Heading untuk judul):
                A. Informasi Umum (Identitas, Kompetensi Awal, Dimensi Profil, Capaian Pembelajaran, Tujuan Pembelajaran, Model/Pendekatan)
                B. Komponen Inti (Langkah-langkah Pembelajaran terbagi menjadi Pendahuluan, Inti, Penutup. Serta Asesmen Diagnostik, Formatif, dan Sumatif lengkap dengan rubrik)
                C. Kegiatan Pengayaan dan Remidial
                D. Lampiran (Bahan Ajar singkat dan rancangan Lembar Kerja Peserta Didik / LKPD)

                SYARAT KHUSUS DAN FILOSOFI:
                1. Pembelajaran Mendalam (Deep Learning): Pastikan langkah pembelajaran mengeksplorasi konsep tingkat tinggi (HOTS), tidak hanya menghafal.
                2. Kurikulum Berbasis Cinta (Kemenag): Integrasikan narasi kasih sayang, empati, pendekatan humanis berpusat pada siswa, dan penghargaan terhadap proses belajar anak di bagian apersepsi dan penutup.
                3. Pendekatan Terpilih: Fokuskan metode dan aktivitas pada "{pendekatan}". Jika TIK, sebutkan penggunaan media interaktif. Jika Moderasi Beragama, sisipkan nilai toleransi dan keseimbangan dalam materi. Jika Bilingual, gunakan istilah dwibahasa di materi inti.

                Buatkan secara lengkap, profesional, dan siap cetak. Gunakan pemformatan Markdown yang rapi.
                """
                
                response = model.generate_content(prompt_system)
                st.success("✅ Modul Ajar berhasil dibuat!")
                
                # SIMPAN HASIL KE SESSION STATE agar tidak hilang saat tombol download diklik
                st.session_state['hasil_modul'] = response.text
                
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: Periksa kembali API Key Anda atau coba beberapa saat lagi. Detail error: {e}")

# --- MENAMPILKAN HASIL & TOMBOL DOWNLOAD ---
# Bagian ini ditempatkan di luar blok if st.button agar tetap muncul setelah render ulang
if 'hasil_modul' in st.session_state:
    with st.expander("📄 LIHAT HASIL MODUL AJAR", expanded=True):
        st.markdown(st.session_state['hasil_modul'])
        
        # Format nama file agar rapi (misal: Modul_Ajar_Kimia_Pereaksi_Pembatas.md)
        nama_file = f"Modul_Ajar_{mapel}_{materi.replace(' ', '_')}.md"
        
        # Tombol Download Bawaan Streamlit
        st.download_button(
            label="📥 Download Modul Ajar",
            data=st.session_state['hasil_modul'],
            file_name=nama_file,
            mime="text/markdown",
            use_container_width=True
        )
