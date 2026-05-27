"""
app/routes/index_routes.py
--------------------------
Blueprint utama yang menangani:
  - GET  /      → Render halaman utama (index.html)
  - POST /chat  → Endpoint AI: terima pertanyaan, kembalikan jawaban JSON
"""

from __future__ import annotations

import json
import re

from flask import Blueprint, current_app, jsonify, render_template, request
from flask.wrappers import Response

from app import groq_client
from app.services.file_service import allowed_file, extract_text

index_bp = Blueprint("index", __name__)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _strip_markdown_fences(text: str) -> str:
    """Hapus ```json ... ``` yang kadang dihasilkan model secara otomatis."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _parse_history(raw: str) -> list[dict[str, str]]:
    """Deserialise history percakapan dari frontend secara aman."""
    try:
        history = json.loads(raw)
        if isinstance(history, list):
            return history
    except (json.JSONDecodeError, TypeError):
        pass
    return []


def _error_response(message: str) -> dict:
    """Format respons error yang konsisten untuk dikirim ke frontend."""
    return {"answers": [{"heading": "Terjadi Kesalahan", "points": [message]}]}


def _is_rate_limit_error(error_message: str) -> bool:
    """
    Deteksi apakah error berasal dari rate limit atau token limit Groq API.
    Cek dilakukan secara case-insensitive.
    """
    keywords = [
        "rate_limit_exceeded", "tokens per minute", "request too large",
        "tpm", "too many tokens", "context_length_exceeded",
        "maximum context length", "token limit", "ratelimiterror",
        "rate limit", "exceeded",
    ]
    error_lower = error_message.lower()
    return any(kw in error_lower for kw in keywords)


# ── Routes ────────────────────────────────────────────────────────────────────

@index_bp.route("/", methods=["GET"])
def index() -> str:
    """Render halaman utama."""
    return render_template("index.html")


@index_bp.route("/chat", methods=["POST"])
def chat() -> Response:
    """
    Endpoint utama untuk percakapan dengan AI.

    Menerima:
        - input   (str)       : Pertanyaan dari user.
        - history (JSON str)  : Riwayat percakapan sebelumnya.
        - file    (FileStorage): File opsional (PDF, gambar, DOCX).

    Mengembalikan:
        JSON dengan key `answers` berisi daftar { heading, points }.
        Jika rate limit: tambahan key `__error_type: "rate_limit"`.
    """
    user_input: str = (request.form.get("input") or "").strip()

    if not user_input:
        return jsonify({
            "answers": [{"heading": "Ups!", "points": ["Tolong masukkan pertanyaan terlebih dahulu."]}]
        })

    history = _parse_history(request.form.get("history", "[]"))

    # Proses file yang diupload (opsional)
    file_context: str | None = None
    uploaded_file = request.files.get("file")

    if uploaded_file and uploaded_file.filename:
        if not allowed_file(uploaded_file.filename):
            return jsonify(_error_response(
                "Format file tidak didukung. Gunakan PDF, gambar (JPG/PNG), atau DOCX."
            ))
        file_context = extract_text(uploaded_file, current_app.config["UPLOAD_FOLDER"])

    # Kirim ke Groq AI
    try:
        raw_response   = groq_client.query(
            user_input,
            history,
            file_context,
            app=current_app._get_current_object(),
        )
        clean_response = _strip_markdown_fences(raw_response)
        parsed         = json.loads(clean_response)
        parsed["_raw"] = clean_response
        return jsonify(parsed)

    except json.JSONDecodeError as exc:
        current_app.logger.error("Gagal parse JSON dari model: %s", exc)
        return jsonify(_error_response("Model mengembalikan format yang tidak valid."))

    except Exception as exc:
        error_str = str(exc)
        current_app.logger.exception("Error tidak terduga: %s", exc)

        if _is_rate_limit_error(error_str):
            return jsonify({
                "__error_type" : "rate_limit",
                "answers"      : [{"heading": "Terjadi Kesalahan", "points": [error_str]}],
            })

        return jsonify(_error_response(error_str))
