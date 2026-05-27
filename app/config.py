"""
app/config.py
-------------
Konfigurasi aplikasi yang dibaca dari environment variables.
Gunakan file .env untuk mengatur nilai-nilainya di lingkungan lokal.
"""

import os


class Config:
    """Konfigurasi utama aplikasi."""

    # Flask
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # Groq AI API
    GROQ_API_KEY: str      = os.environ.get("GROQ_API_KEY", "")
    GROQ_MODEL: str        = "llama-3.3-70b-versatile"       # Model text-only
    GROQ_VISION_MODEL: str = "meta-llama/llama-4-scout-17b-16e-instruct"  # Model vision (gambar)
    GROQ_TEMPERATURE: float = 0.5
    GROQ_MAX_TOKENS: int    = 1024

    # Upload
    UPLOAD_FOLDER: str      = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16 MB
