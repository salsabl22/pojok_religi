"""
app/__init__.py
---------------
Application factory untuk Flask.
Menggunakan pola Factory Pattern agar mudah diuji dan dikonfigurasi.
"""

import os

from flask import Flask

from app.config import Config
from app.routes import register_routes


def create_app(config_class: type = Config) -> Flask:
    """
    Buat dan konfigurasikan instance Flask.

    Parameters
    ----------
    config_class : type
        Kelas konfigurasi yang akan digunakan (default: Config).

    Returns
    -------
    Flask
        Instance aplikasi yang sudah dikonfigurasi.
    """
    app = Flask(__name__, static_folder="../static")
    app.config.from_object(config_class)

    # Buat folder upload jika belum ada
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    register_routes(app)

    return app
