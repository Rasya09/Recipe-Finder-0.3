import json
import os

# File JSON tempat menyimpan data pengguna
DATA_FILE = 'users.json'

# File JSON tempat menyimpan data resep
RECIPES_FILE = 'recipes.json'

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

# Fungsi memuat data resep dari file JSON
def load_recipes():
    if not os.path.exists(RECIPES_FILE):
        with open(RECIPES_FILE, 'w') as file:
            json.dump([], file)
    with open(RECIPES_FILE, 'r') as file:
        return json.load(file)

# Fungsi menyimpan data resep ke file JSON
def save_recipes(data):
    with open(RECIPES_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Fungsi untuk membuat ID otomatis
def generate_id(users):
    if not users:
        return 1
    return max(user['id'] for user in users) + 1

# Fungsi untuk membuat ID resep otomatis
def generate_recipe_id(recipes):
    if not recipes:
        return 1
    return max(recipe['id'] for recipe in recipes) + 1

# Fungsi registrasi pengguna
def register():
    print("\n=== Registrasi Pengguna ===")
    users = load_data()

    # Input data pengguna
    username = input("Masukkan username: ")
    email = input("Masukkan email: ")

    # Cek apakah email sudah digunakan
    for user in users:
        if user['email'] == email:
            print("Email sudah terdaftar! Silakan gunakan email lain.")
            return

    password = input("Masukkan password: ")

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
        "password": password,
        "role": role
    })

    # Simpan data ke file JSON
    save_data(users)
    print("Registrasi berhasil! Anda dapat login sekarang.")

# Fungsi login pengguna
def login():
    print("\n=== Login Pengguna ===")
    email = input("Masukkan email: ")
    password = input("Masukkan password: ")

    # Load data pengguna
    users = load_data()

    # Cek apakah email dan password cocok
    for user in users:
        if user['email'] == email and user['password'] == password:
            print(f"Login berhasil! Selamat datang, {user['username']} ({user['role']}).")
            return user  # Mengembalikan data pengguna
    print("Login gagal! Email atau password salah.")
    return None

# Fungsi untuk menambahkan resep
def add_recipe(chef):
    print("\n=== Tambahkan Resep Baru ===")
    recipes = load_recipes()

    # Input data resep
    title = input("Masukkan judul resep: ")
    description = input("Masukkan deskripsi resep: ")
    ingredients = input("Masukkan bahan-bahan (pisahkan dengan koma): ").split(",")
    steps = input("Masukkan langkah-langkah (pisahkan dengan titik koma): ").split(";")

    # Buat ID resep otomatis
    recipe_id = generate_recipe_id(recipes)

    # Tambahkan resep ke dalam list
    recipes.append({
        "id": recipe_id,
        "title": title.strip(),
        "description": description.strip(),
        "ingredients": [i.strip() for i in ingredients],
        "steps": [s.strip() for s in steps],
        "author": chef['username']  # Menyimpan nama Chef sebagai pembuat resep
    })

    # Simpan data ke file JSON
    save_recipes(recipes)
    print("Resep berhasil ditambahkan!")

# Fungsi untuk mengedit resep
def edit_recipe(chef):
    print("\n=== Edit Resep ===")
    recipes = load_recipes()
    chef_recipes = [recipe for recipe in recipes if recipe['author'] == chef['username']]

    if not chef_recipes:
        print("Anda belum memiliki resep untuk diedit.")
        return

    print("Resep Anda:")
    for recipe in chef_recipes:
        print(f"{recipe['id']}. {recipe['title']}")

    try:
        recipe_id = int(input("Masukkan ID resep yang ingin diedit: "))
    except ValueError:
        print("ID tidak valid!")
        return

    recipe_to_edit = next((recipe for recipe in chef_recipes if recipe['id'] == recipe_id), None)
    if not recipe_to_edit:
        print("Resep tidak ditemukan.")
        return

    print("Kosongkan input jika tidak ingin mengubah bagian tersebut.")
    new_title = input(f"Judul baru ({recipe_to_edit['title']}): ") or recipe_to_edit['title']
    new_description = input(f"Deskripsi baru ({recipe_to_edit['description']}): ") or recipe_to_edit['description']
    new_ingredients = input("Bahan-bahan baru (pisahkan dengan koma, atau tekan Enter untuk tidak mengubah): ")
    new_steps = input("Langkah-langkah baru (pisahkan dengan titik koma, atau tekan Enter untuk tidak mengubah): ")

    recipe_to_edit['title'] = new_title
    recipe_to_edit['description'] = new_description
    if new_ingredients:
        recipe_to_edit['ingredients'] = [i.strip() for i in new_ingredients.split(",")]
    if new_steps:
        recipe_to_edit['steps'] = [s.strip() for s in new_steps.split(";")]

    save_recipes(recipes)
    print("Resep berhasil diperbarui!")

# Fungsi untuk menghapus resep
def delete_recipe(chef):
    print("\n=== Hapus Resep ===")
    recipes = load_recipes()
    chef_recipes = [recipe for recipe in recipes if recipe['author'] == chef['username']]

    if not chef_recipes:
        print("Anda belum memiliki resep untuk dihapus.")
        return

    print("Resep Anda:")
    for recipe in chef_recipes:
        print(f"{recipe['id']}. {recipe['title']}")

    try:
        recipe_id = int(input("Masukkan ID resep yang ingin dihapus: "))
    except ValueError:
        print("ID tidak valid!")
        return

    recipe_to_delete = next((recipe for recipe in chef_recipes if recipe['id'] == recipe_id), None)
    if not recipe_to_delete:
        print("Resep tidak ditemukan.")
        return

    confirm = input(f"Apakah Anda yakin ingin menghapus resep '{recipe_to_delete['title']}'? (y/n): ").lower()
    if confirm == 'y':
        recipes.remove(recipe_to_delete)
        save_recipes(recipes)
        print("Resep berhasil dihapus!")
    else:
        print("Penghapusan dibatalkan.")
