"""
app/routes/__init__.py
----------------------
Mendaftarkan semua blueprint ke aplikasi Flask.
Tambahkan blueprint baru di sini jika aplikasi berkembang.
"""

from flask import Flask

from app.routes.index_routes import index_bp


def register_routes(app: Flask) -> None:
    """Daftarkan semua blueprint ke instance Flask."""
    app.register_blueprint(index_bp)
