# anthroGizi v4.0.0

**Platform Gizi Anak Terpercaya Berbasis Sains dan Profesional**

## 🌟 Tentang anthroGizi

anthroGizi adalah platform komprehensif untuk monitoring pertumbuhan dan gizi anak yang menggabungkan teknologi terkini dengan standar internasional WHO 2006. Dirancang untuk membantu orang tua dan tenaga kesehatan dalam memantau perkembangan anak dengan akurasi tinggi.

## ✨ Fitur Unggulan

### 🔢 Kalkulator WHO Lengkap
- **WAZ** (Weight-for-Age Z-Score)
- **HAZ** (Height-for-Age Z-Score)
- **WHZ** (Weight-for-Height Z-Score)
- **BAZ** (BMI-for-Age Z-Score)
- **HCZ** (Head Circumference-for-Age Z-Score)

### 📊 Analisis & Laporan
- Grafik pertumbuhan interaktif
- Tren perkembangan anak
- Laporan PDF dan Excel
- Analisis berdasarkan kelompok usia dan gender

### 📚 Library Komprehensif
- 1000+ artikel edukatif
- Video tutorial dari ahli
- Panduan MPASI lengkap
- Tips perawatan anak

### 💬 Konsultasi Profesional
- Konsultasi WhatsApp dengan dokter spesialis
- Ahli gizi klinis
- Respon cepat (2-4 jam)

### 🎨 Personalisasi
- 3 tema warna pastel
- Mode Parent/Healthcare
- Multi-bahasa (ID/EN)
- Notifikasi motivasional

## 🚀 Teknologi yang Digunakan

### Backend
- **Flask 2.3.3** - Web framework Python
- **SQLAlchemy 2.0** - ORM database
- **pygrowup 0.9.5** - WHO calculator library
- **Chart.js** - Visualisasi data
- **Bootstrap 5.3** - UI framework

### Frontend
- **Jinja2** - Template engine
- **Font Awesome 6** - Icons
- **Google Fonts** - Typography
- **Responsive Design** - Mobile-first

### Database
- **SQLite** (development)
- **PostgreSQL** (production ready)
- **Redis** (caching & sessions)

## 📦 Instalasi

### Prasyarat
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Langkah Instalasi

1. **Clone repository**
```bash
git clone https://github.com/yourusername/anthroGizi.git
cd anthroGizi_v4
```

2. **Buat virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Konfigurasi environment**
```bash
cp .env.example .env
# Edit .env dengan konfigurasi Anda
```

5. **Inisialisasi database**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Jalankan aplikasi**
```bash
python run.py
```

## ⚙️ Konfigurasi

### Environment Variables
```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379/0
```

### Premium Packages
- **Free**: Fitur dasar, 5 kalkulasi/hari
- **Silver** (Rp49.999/bulan): Unlimited kalkulasi, 2 konsultasi
- **Gold** (Rp99.999/bulan): Semua fitur, konsultasi unlimited

## 📱 Cara Penggunaan

### Kalkulator WHO
1. Pilih mode input (usia/bulan/tanggal)
2. Masukkan data anak (berat, tinggi, lingkar kepala)
3. Pilih jenis kelamin
4. Klik "Hitung Z-Score"
5. Lihat hasil dan interpretasi

### Konsultasi Ahli
1. Upgrade ke paket Silver/Gold
2. Pilih dokter/ahli gizi
3. Klik "Konsultasi via WhatsApp"
4. Ajukan pertanyaan Anda

### Export Laporan
1. Pergi ke menu Reports
2. Pilih format (PDF/Excel)
3. Pilih periode data
4. Klik "Export"

## 🎯 Standar yang Digunakan

### Internasional
- **WHO Child Growth Standards 2006**
- **CDC Growth Charts**
- **IAP Guidelines**

### Nasional
- **Permenkes RI No. 2 Tahun 2020**
- **Standar Indonesia**

### Keamanan
- **GDPR Compliance**
- **HIPAA Privacy Protection**
- **ISO 27001 Security**

## 📊 Struktur Proyek

```
anthroGizi_v4/
├── app.py              # Main application
├── config.py           # Configuration settings
├── run.py              # Application runner
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Homepage
│   ├── calculator.html # WHO calculator
│   ├── easy_mode.html # Simplified mode
│   ├── library.html   # Article library
│   ├── videos.html    # Video library
│   ├── reports.html   # Analytics
│   ├── premium.html   # Subscription
│   ├── kpsp.html      # Development screening
│   └── about.html     # About & support
├── static/            # Static files (CSS/JS/images)
├── data/              # WHO reference data
└── uploads/           # File uploads
```

## 🔒 Keamanan & Privasi

- Enkripsi data end-to-end
- Tidak menyimpan data pribadi tanpa izin
- Compliance dengan GDPR dan HIPAA
- Session management yang aman
- Input validation dan sanitization

## 🤝 Kontribusi

Kami menyambut kontribusi dari komunitas!

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Dukungan

- **Email**: support@anthrogizi.com
- **WhatsApp**: +62 812-3456-7890
- **Telepon**: 0800-1234-5678
- **Website**: https://anthrogizi.com

## 📄 Lisensi

Proyek ini dilisensikan under MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 🙏 Acknowledgments

- **WHO** untuk standar pertumbuhan anak
- **Indonesian Pediatric Society** untuk panduan klinis
- **Komunitas Open Source** untuk tools dan library
- **Tim Developer** atas dedikasi dan kerja keras

## 📈 Statistik

- **50.000+** Pengguna aktif
- **1.000+** Artikel edukatif
- **500+** Video tutorial
- **4.8/5** Rating pengguna

---

**anthroGizi v4.0.0** - *Menciptakan Generasi Sehat dan Cerdas* 🌟

*Build: 2024.11.20.001 | Last Updated: 20 November 2024*