import json
import os
import bcrypt

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

# Fungsi untuk membuat ID otomatis
def generate_id(users):
    if not users:
        return 1
    return max(user['id'] for user in users) + 1

def validate_email(email):
    if not email.endswith("@gmail.com"):
        return False
    name_part = email.split("@")[0]
    return len(name_part) > 0

# Fungsi registrasi pengguna
def register():
    print("\n=== Registrasi Pengguna ===")
    users = load_data()

    # Input data pengguna
    while True:
        username = input("Masukkan username: ").strip()
        if username:
            break
        print("Username tidak boleh kosong!")

    while True:
        email = input("Masukkan email: ").strip()
        if email:
            if validate_email(email):
                break
            else:
                print("Email harus berformat @gmail.com dan memiliki nama!")
        else:
            print("Email tidak boleh kosong!")

    # Cek apakah email sudah digunakan
    for user in users:
        if user['email'] == email:
            print("Email sudah terdaftar! Silakan gunakan email lain.")
            return

    while True:
        password = input("Masukkan password (minimal 8 karakter): ").strip()
        if password:
            if len(password) >= 8:
                break
            else:
                print("Password harus minimal 8 karakter!")
        else:
            print("Password tidak boleh kosong!")

    # Hash password dengan bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Pilih role antara user dan chef
    while True:
        print("\nPilih Role:")
        print("1. User")
        print("2. Chef")
        role_input = input("Pilih (1/2): ")
        if role_input == '1':
            role = 'User'
            break
        elif role_input == '2':
            role = 'Chef'
            break
        else:
            print("Pilihan tidak valid! Pilih 1 atau 2.")

    # Buat ID otomatis
    user_id = generate_id(users)

    # Tambahkan pengguna ke dalam list
    users.append({
        "id": user_id,
        "username": username,
        "email": email,
        "password": hashed_password.decode('utf-8'),  # Simpan dalam bentuk string
        "role": role
    })

    # Simpan data ke file JSON
    save_data(users)
    print("Registrasi berhasil! Anda dapat login sekarang.")

# Fungsi login pengguna
def login():
    print("\n=== Login Pengguna ===")
    
    while True:
        email = input("Masukkan email: ").strip()
        if not validate_email(email):
            print("❌ Email harus menggunakan @gmail.com dan memiliki nama sebelum '@'!")
            continue
        break

    password = input("Masukkan password: ").strip()

    users = load_data()

    for user in users:
        if user['email'] == email and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            print(f"✅ Login berhasil! Selamat datang, {user['username']} ({user['role']}).")
            return user

    print("\n")
    print("❌ Login gagal!")
    print("Email atau password salah.")
    return None
