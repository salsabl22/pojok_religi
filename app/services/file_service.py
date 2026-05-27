"""
app/services/file_service.py
----------------------------
Layanan untuk menangani file yang diupload user.

Alur kerja:
  1. Simpan file sementara ke UPLOAD_FOLDER.
  2. Ekstrak konten (teks atau gambar base64).
  3. Hapus file dari server setelah diekstrak.

Format kembalian:
  - PDF / DOCX : string teks biasa.
  - Gambar     : sentinel "__IMAGE_BASE64__<mime>::<base64>" (dikonsumsi groq_client).
"""

from __future__ import annotations

import base64
import os

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS: set[str] = {"pdf", "png", "jpg", "jpeg", "docx"}


def allowed_file(filename: str) -> bool:
    """Return True jika ekstensi file ada dalam daftar yang diizinkan."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text(file: FileStorage, upload_folder: str) -> str:
    """
    Simpan file sementara, ekstrak kontennya, lalu hapus.

    Parameters
    ----------
    file : FileStorage
        Objek file dari request Flask.
    upload_folder : str
        Path folder penyimpanan sementara.

    Returns
    -------
    str
        Teks hasil ekstraksi, atau sentinel base64 untuk gambar.
    """
    filename = secure_filename(file.filename)
    ext      = filename.rsplit(".", 1)[1].lower()
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    try:
        if ext == "pdf":
            return _extract_pdf(filepath)
        elif ext in {"png", "jpg", "jpeg"}:
            return _extract_image(filepath, ext)
        elif ext == "docx":
            return _extract_docx(filepath)
        return ""
    finally:
        # Selalu hapus file sementara, bahkan jika ekstraksi gagal
        if os.path.exists(filepath):
            os.remove(filepath)


# ── Private extractors ────────────────────────────────────────────────────────

def _extract_pdf(filepath: str) -> str:
    """Ekstrak teks dari file PDF menggunakan pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader  # type: ignore[no-redef]  # fallback lama

    pages: list[str] = []
    with open(filepath, "rb") as f:
        for page in PdfReader(f).pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n".join(pages)


def _extract_image(filepath: str, ext: str) -> str:
    """Encode gambar ke base64 dengan format sentinel untuk groq_client."""
    mime = "image/jpeg" if ext in {"jpg", "jpeg"} else "image/png"
    with open(filepath, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"__IMAGE_BASE64__{mime}::{encoded}"


def _extract_docx(filepath: str) -> str:
    """Ekstrak teks dari file DOCX menggunakan python-docx."""
    from docx import Document
    doc = Document(filepath)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
