"""
app/groq_client.py
------------------
Klien untuk Groq AI API.

Bertanggung jawab untuk:
  - Membangun pesan (system, history, user prompt).
  - Memilih model yang tepat (text vs vision).
  - Mengirim request ke Groq dan mengembalikan respons mentah (string JSON).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from groq import Groq

if TYPE_CHECKING:
    from flask import Flask


# ── Prompt ────────────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """
Kamu adalah seorang pemuka agama yang dihormati, dikenal karena kebijaksanaan
dan selera humor yang tinggi.

== ATURAN TOPIK ==
Kamu HANYA boleh menjawab pertanyaan yang berkaitan dengan:
- Agama (Islam, dan topik keagamaan umum)
- Spiritualitas
- Kehidupan sehari-hari dari sudut pandang agama/moral

Jika pertanyaan user berada di luar topik tersebut (misalnya: coding, matematika,
politik praktis, hiburan, teknologi, resep masakan, dan sejenisnya), kamu WAJIB
menolak dengan ramah menggunakan format JSON berikut TANPA menjawab pertanyaannya:
{
  "answers": [
    {
      "heading": "Di Luar Topik",
      "points": [
        "Maaf, pertanyaan tersebut berada di luar bidang yang bisa saya bantu. Saya hanya dapat menjawab pertanyaan seputar agama, spiritualitas, dan kehidupan dari sudut pandang moral dan keagamaan.",
        "Yuk, tanyakan sesuatu yang lebih bermakna untuk perjalanan spiritualmu! Ada yang ingin kamu renungkan hari ini?"
      ]
    }
  ]
}

== ATURAN FORMAT JAWABAN (hanya untuk topik yang diizinkan) ==
Balas HANYA dalam JSON dengan format berikut, tanpa kata "json" dan tanpa spasi di awal:
{
  "answers": [
    {
      "heading": "Judul Bagian",
      "points": [
        "Poin pertama yang menjelaskan sesuatu.",
        "Poin kedua yang menjelaskan sesuatu lainnya."
      ]
    }
  ]
}

Panduan pengisian:
- Bagi jawaban menjadi 2-4 bagian (heading) yang logis, misalnya: Dalil, Penjelasan, Hikmah, Penutup.
- Setiap heading berisi 1-4 poin kalimat lengkap.
- Jelaskan dalil agama secara detail dengan unsur humor yang cerdas, tanpa menyinggung agama lain.
- Gunakan bahasa yang ringan, menghibur, namun tetap mencerminkan wawasan keagamaan yang mendalam.
- Poin terakhir di bagian terakhir boleh berisi kalimat interaktif atau pertanyaan balik ke user.
- Jangan gabungkan semua isi dalam satu poin panjang.
""".strip()

_USER_PROMPT_SUFFIX = (
    ' Jawab dalam format JSON yang sudah ditentukan: {"answers": [{"heading": "...", "points": ["..."]}]}'
)


# ── Type alias ────────────────────────────────────────────────────────────────

HistoryEntry = dict[str, str]


# ── Public interface ──────────────────────────────────────────────────────────

def query(
    user_input: str,
    history: list[HistoryEntry] | None = None,
    file_context: str | None = None,
    *,
    app: "Flask",
) -> str:
    """
    Kirim prompt ke Groq API dan kembalikan respons mentah (string JSON).

    Parameters
    ----------
    user_input : str
        Pertanyaan terbaru dari user.
    history : list, optional
        Riwayat percakapan sebelumnya dalam format [{ user, assistant }].
    file_context : str, optional
        Teks hasil ekstraksi file, atau sentinel base64 untuk gambar.
    app : Flask
        Instance Flask untuk akses konfigurasi API key dan model.

    Returns
    -------
    str
        String JSON mentah dari model AI.
    """
    client   = Groq(api_key=app.config["GROQ_API_KEY"])
    is_image = file_context and file_context.startswith("__IMAGE_BASE64__")
    model    = app.config["GROQ_VISION_MODEL"] if is_image else app.config["GROQ_MODEL"]
    messages = _build_messages(user_input, history or [], file_context)

    completion = client.chat.completions.create(
        model                 = model,
        messages              = messages,
        temperature           = app.config["GROQ_TEMPERATURE"],
        max_completion_tokens = app.config["GROQ_MAX_TOKENS"],
        top_p                 = 1,
    )

    return completion.choices[0].message.content


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_messages(
    user_input: str,
    history: list[HistoryEntry],
    file_context: str | None,
) -> list:
    """
    Susun daftar pesan lengkap: system → history → prompt user.

    Mendukung tiga mode input:
      1. Gambar  → multimodal (image_url + text).
      2. Dokumen → teks file digabung dengan pertanyaan user.
      3. Teks    → pertanyaan user saja.
    """
    messages: list = [{"role": "system", "content": _SYSTEM_PROMPT}]

    # Masukkan riwayat percakapan sebelumnya
    for turn in history:
        messages.append({"role": "user",      "content": turn["user"]})
        messages.append({"role": "assistant", "content": turn["assistant"]})

    # Mode gambar: kirim sebagai multimodal content
    if file_context and file_context.startswith("__IMAGE_BASE64__"):
        _, rest    = file_context.split("__IMAGE_BASE64__", 1)
        mime, data = rest.split("::", 1)
        messages.append({
            "role": "user",
            "content": [
                {
                    "type"      : "image_url",
                    "image_url" : {"url": f"data:{mime};base64,{data}"},
                },
                {"type": "text", "text": user_input + _USER_PROMPT_SUFFIX},
            ],
        })

    # Mode dokumen: gabungkan teks file dengan pertanyaan
    elif file_context:
        combined = (
            f"Berikut isi dokumen yang diupload user:\n\n{file_context}\n\n"
            f"Pertanyaan user: {user_input}"
        )
        messages.append({"role": "user", "content": combined + _USER_PROMPT_SUFFIX})

    # Mode teks biasa
    else:
        messages.append({"role": "user", "content": user_input + _USER_PROMPT_SUFFIX})

    return messages
