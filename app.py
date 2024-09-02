from app import app

app.run(debug = True, host="0.0.0.0", port=5000)
# app.run(debug = True)

# ===== Manajemen database =====
# flask db init
# flask db stamp head 
# flask db migrate
# flask db upgrade

# ===== Menjalankan aplikasi =====
# py app.py

# ===== Membuat/Menginstall requairements.txt =====
# pip freeze > requirements.txt
# pip install -r requirements.txt

# ===== Website penyedia icon =====
# https://www.w3schools.com/icons/

# ===== Konversi Python Code ke .exe =====
# pyinstaller --onefile --icon=app\static\ico\logo-raihan-parfum-dark.ico "Raihan Parfum.py"

# ===== Membuat environment baru =====
# py -m venv env

# IP Laptop
# 192.168.251.33 (Makassar)
# 192.168.43.41 (Karossa)