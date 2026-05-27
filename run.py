"""
run.py
------
Entry point untuk menjalankan aplikasi Pojok Religi secara lokal.

Cara menjalankan:
    python run.py

Untuk production, gunakan WSGI server seperti Gunicorn:
    gunicorn -w 4 "app:create_app()"
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
