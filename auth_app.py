import json
import os

# File JSON tempat menyimpan data pengguna
DATA_FILE = 'users.json'

# Fungsi memuat data dari file JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as file:
            json.dump([], file)
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# Fungsi menyimpan data ke file JSON
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Fungsi registrasi pengguna
def register():
    print("\n=== Registrasi Pengguna ===")
    username = input("Masukkan username: ").strip()
    email = input("Masukkan email: ").strip()
    password = input("Masukkan password: ").strip()

    # Validasi input
    if not username or not email or not password:
        print("Semua field harus diisi!")
        return False

    # Load data pengguna
    users = load_data()

    # Cek apakah email sudah digunakan
    for user in users:
        if user['email'] == email:
            print("Email sudah digunakan! Silakan gunakan email lain.")
            return False

    # Tambahkan pengguna baru ke data
    users.append({"username": username, "email": email, "password": password})
    save_data(users)
    print("Registrasi berhasil! Anda dapat login sekarang.")
    return True

# Fungsi login pengguna
def login():
    print("\n=== Login Pengguna ===")
    email = input("Masukkan email: ").strip()
    password = input("Masukkan password: ").strip()

    # Load data pengguna
    users = load_data()

    # Cek apakah email dan password cocok
    for user in users:
        if user['email'] == email and user['password'] == password:
            print(f"Login berhasil! Selamat datang, {user['username']}.")
            return True

    print("Login gagal! Email atau password salah.")
    return False
