# 🕌 Pojok Religi

Asisten AI berbasis web untuk menjawab pertanyaan seputar agama, spiritualitas, dan kehidupan sehari-hari dari sudut pandang moral dan keagamaan.

Dibangun menggunakan **Flask** + **Groq AI API** (LLaMA 3.3), dengan antarmuka yang responsif dan mendukung upload dokumen.

---

## ✨ Fitur

- 💬 **Chat AI** — Jawaban terstruktur dengan efek typewriter
- 🔐 **Autentikasi** — Login & Register berbasis localStorage (tanpa database)
- 👤 **Multi-user** — Setiap user memiliki riwayat percakapan masing-masing
- 📎 **Upload Dokumen** — Mendukung PDF, DOCX, JPG, PNG (maks. 5–10 MB)
- 🌙 **Dark / Light Mode** — Tema yang dapat diganti dan disimpan
- 📱 **Responsif** — Sidebar collapsible, tampilan mobile-friendly

> **Catatan:** Autentikasi dan riwayat disimpan di `localStorage` browser.
> Data hanya tersedia di perangkat dan browser yang sama.
> Untuk deployment production, gunakan database (MySQL, PostgreSQL, dll).

---

## 🛠 Tech Stack

| Layer    | Teknologi                          |
|----------|------------------------------------|
| Backend  | Python 3.11+, Flask 3              |
| AI       | Groq API — LLaMA 3.3 70B & LLaMA 4 Scout (vision) |
| Frontend | HTML5, CSS3, Vanilla JavaScript    |
| Storage  | localStorage (browser-side)        |

---

## 🚀 Cara Menjalankan

### 1. Clone & Setup

```bash
git clone https://github.com/username/pojok-religi.git
cd pojok-religi

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Konfigurasi

Buat file `.env` di root proyek:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxx
SECRET_KEY=your-secret-key-here
```

Dapatkan API key gratis di [console.groq.com](https://console.groq.com).

### 3. Jalankan

```bash
python run.py
```

Buka browser: `http://localhost:5000`

---

## 📁 Struktur Proyek

```
pojok-religi/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Konfigurasi (env vars)
│   ├── groq_client.py       # Integrasi Groq AI API
│   ├── routes/
│   │   ├── __init__.py      # Registrasi blueprint
│   │   └── index_routes.py  # Route utama (/, /chat)
│   ├── services/
│   │   └── file_service.py  # Ekstraksi konten file upload
│   └── templates/
│       └── index.html       # SPA — UI + logika JavaScript
├── static/
│   ├── css/
│   │   └── style.css        # Desain & tema (light/dark)
│   └── icon/
│       ├── mosque.png
│       └── button_submit.png
├── uploads/                 # Folder sementara file upload (auto-dibuat)
├── .env                     # Variabel lingkungan (tidak di-commit)
├── .gitignore
├── requirements.txt
├── run.py                   # Entry point
└── README.md
```

---

## 📝 Catatan Pengembang

- Seluruh logika JavaScript dikemas dalam satu **IIFE** untuk menghindari polusi global scope.
- History percakapan disimpan per user dengan key `pojokreligi_convs_<username>` di localStorage.
- AI hanya menjawab topik agama, spiritualitas, dan kehidupan — pertanyaan di luar topik akan ditolak dengan ramah.
- File upload dihapus otomatis dari server setelah konten diekstrak.

---

## 📄 Lisensi

MIT License — bebas digunakan untuk portofolio dan pengembangan lebih lanjut.
