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

def get_valid_username(text_form="Masukkan nama pengguna: "):
    while True:
        username = input(text_form).strip()
        if username:
            return username
        print("Username tidak boleh kosong!")

def validate_email(email):
    if not email.endswith("@gmail.com"):
        return False
    name_part = email.split("@")[0]
    return len(name_part) > 0

def get_valid_email(text_form="Masukkan email: ", users=None, current_user_id=None):
    while True:
        email = input(text_form).strip()
        if not email:
            print("Email tidak boleh kosong!")
            continue
            
        if not validate_email(email):
            print("Email harus berformat @gmail.com dan memiliki nama!")
            continue
            
        # Cek duplikasi email jika users list disediakan
        if users is not None:
            email_exists = any(u['email'] == email and u['id'] != current_user_id for u in users)
            if email_exists:
                print("Email sudah terdaftar! Silakan gunakan email lain.")
                continue
                
        return email

def get_valid_password(text_form="Masukkan password (minimal 8 karakter): "):
    while True:
        password = input(text_form).strip()
        if not password:
            print("Password tidak boleh kosong!")
            continue
            
        if len(password) < 8:
            print("Password harus minimal 8 karakter!")
            continue
            
        return password
    
# Fungsi registrasi pengguna
def register():
    print("\n=== Registrasi Pengguna ===")
    users = load_data()

    username = get_valid_username()
    email = get_valid_email(users=users)
    password = get_valid_password()

    # Hash password dengan bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Pilih role
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

    user_id = generate_id(users)
    users.append({
        "id": user_id,
        "username": username,
        "email": email,
        "password": hashed_password.decode('utf-8'),
        "role": role
    })

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
