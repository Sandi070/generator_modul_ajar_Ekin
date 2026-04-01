import streamlit as st
import google.generativeai as genai
from datetime import datetime
import markdown

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
    
    if not user_api_key.strip():
        st.warning("⚠️ Silakan masukkan API Key di menu samping (sidebar) terlebih dahulu.")
    elif not mapel.strip() or not fase.strip() or not materi.strip() or not tahun.strip():
        st.warning("⚠️ Harap lengkapi semua kolom: Mata Pelajaran, Fase, Materi, dan Tahun Pelajaran!")
    else:
        try:
            with st.spinner("⏳ Sedang merakit modul pembelajaran dengan cinta..."):
                
                genai.configure(api_key=user_api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                
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
                st.session_state['hasil_modul'] = response.text
                
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: Periksa kembali API Key Anda atau coba beberapa saat lagi. Detail error: {e}")

# --- MENAMPILKAN HASIL & TOMBOL DOWNLOAD WORD ---
if 'hasil_modul' in st.session_state:
    with st.expander("📄 LIHAT HASIL MODUL AJAR", expanded=True):
        # Tampilkan di layar aplikasi
        st.markdown(st.session_state['hasil_modul'])
        
        # PROSES KONVERSI KE FORMAT WORD (.doc) YANG LEBIH RAPI
        # Tambahan ekstensi 'sane_lists' dan 'nl2br' agar paragraf dan poin-poin terstruktur baik
        html_content = markdown.markdown(
            st.session_state['hasil_modul'], 
            extensions=['tables', 'sane_lists', 'nl2br']
        )
        
        # Kerangka HTML dengan injeksi CSS khusus Microsoft Word
        word_html_template = f"""
        <html xmlns:v="urn:schemas-microsoft-com:vml"
              xmlns:o="urn:schemas-microsoft-com:office:office"
              xmlns:w="urn:schemas-microsoft-com:office:word"
              xmlns:m="http://schemas.microsoft.com/office/2004/12/omml"
              xmlns="http://www.w3.org/TR/REC-html40">
        <head>
            <meta charset='utf-8'>
            <title>Modul Ajar</title>
            <style>
                @page WordSection1 {{
                    size: 21.0cm 29.7cm; /* Setelan Kertas A4 */
                    margin: 2.54cm 2.54cm 2.54cm 2.54cm; /* Margin Normal (Atas, Bawah, Kiri, Kanan) */
                    mso-header-margin: 35.4pt;
                    mso-footer-margin: 35.4pt;
                    mso-paper-source: 0;
                }}
                div.WordSection1 {{
                    page: WordSection1;
                }}
                body {{
                    font-family: 'Times New Roman', serif;
                    font-size: 12pt;
                    line-height: 1.5;
                    color: black;
                }}
                h1, h2, h3, h4 {{
                    font-family: 'Arial', sans-serif;
                    color: black;
                    margin-top: 18pt;
                    margin-bottom: 6pt;
                }}
                p {{
                    margin-top: 0;
                    margin-bottom: 10pt;
                    text-align: justify; /* Membuat teks Rata Kiri-Kanan */
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 10pt;
                    margin-bottom: 12pt;
                }}
                th, td {{
                    border: 1pt solid black;
                    padding: 6pt 8pt;
                    vertical-align: top;
                    text-align: left;
                }}
                ul, ol {{
                    margin-top: 0;
                    margin-bottom: 10pt;
                }}
                li {{
                    margin-bottom: 5pt;
                    text-align: justify;
                }}
            </style>
        </head>
        <body>
            <div class="WordSection1">
                {html_content}
            </div>
        </body>
        </html>
        """
        
        # Format nama file
        nama_file = f"Modul_Ajar_{mapel}_{materi.replace(' ', '_')}.doc"
        
        # Tombol Download dengan tipe MIME Microsoft Word
        st.download_button(
            label="📥 Download Format MS Word (.doc)",
            data=word_html_template,
            file_name=nama_file,
            mime="application/msword",
            use_container_width=True
        )crosoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
        <head>
            <meta charset='utf-8'>
            <title>Modul Ajar</title>
            <style>
                body {{
                    font-family: 'Times New Roman', serif;
                    font-size: 12pt;
                    line-height: 1.5;
                }}
                h1, h2, h3, h4 {{
                    font-family: 'Arial', sans-serif;
                    color: #000000;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Format nama file
        nama_file = f"Modul_Ajar_{mapel}_{materi.replace(' ', '_')}.doc"
        
        # Tombol Download dengan tipe MIME Microsoft Word
        st.download_button(
            label="📥 Download Format MS Word (.doc)",
            data=word_html_template,
            file_name=nama_file,
            mime="application/msword",
            use_container_width=True
        )
