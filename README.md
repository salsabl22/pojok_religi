# Pojok Religi

<img width="400" alt="image (1)" src="https://github.com/user-attachments/assets/3102284c-2e0e-43ef-a985-af2929c0519d" />
<img width="400" alt="image (2)" src="https://github.com/user-attachments/assets/af6cdb1a-9976-49ee-b7df-81e5d7b58f8e" />

Asisten AI berbasis web untuk menjawab pertanyaan seputar agama, spiritualitas, dan kehidupan sehari-hari dari sudut pandang moral dan keagamaan.

Dibangun menggunakan **Flask** + **Groq AI API** (LLaMA 3.3), dengan antarmuka yang responsif dan mendukung upload dokumen.

---

## Fitur

-  **Chat AI** — Jawaban terstruktur dengan efek typewriter
-  **Autentikasi** — Login & Register berbasis localStorage (tanpa database)
-  **Multi-user** — Setiap user memiliki riwayat percakapan masing-masing
-  **Upload Dokumen** — Mendukung PDF, DOCX, JPG, PNG (maks. 5–10 MB)
-  **Dark / Light Mode** — Tema yang dapat diganti dan disimpan
-  **Responsif** — Sidebar collapsible, tampilan mobile-friendly

---

##  Tech Stack

| Layer    | Teknologi                          |
|----------|------------------------------------|
| Backend  | Python 3.11+, Flask 3              |
| AI       | Groq API — LLaMA 3.3 70B & LLaMA 4 Scout (vision) |
| Frontend | HTML5, CSS3, Vanilla JavaScript    |
| Storage  | localStorage (browser-side)        |

---

##  Cara Menjalankan

### 1. Clone & Setup

```bash
git clone https://github.com/username/pojok-religi.git
cd pojok-religi

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configuration

Buat file `.env` di root proyek:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxx
SECRET_KEY=your-secret-key-here
```

Dapatkan API key gratis di [console.groq.com](https://console.groq.com).

### 3. Run

```bash
python run.py
```

Browser: `http://localhost:5000`

---
