import subprocess
import os

# Path ke file .bat
bat_file_path = r"D:\Raihan Parfum\run.bat"

# Cek apakah file .bat ada
if not os.path.isfile(bat_file_path):
    raise FileNotFoundError(f"File {bat_file_path} tidak ditemukan.")

# Jalankan file .bat
subprocess.run([bat_file_path], shell=True)