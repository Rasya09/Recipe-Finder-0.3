import bcrypt
from auth_app import get_valid_email, get_valid_password, get_valid_username, register, login, json
from resep import add_recipe, load_recipes

import json

# Fungsi umum untuk memuat dan menyimpan data JSON
def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(file_name, data):
    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    try:
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")

# Fungsi khusus untuk favorit
def load_favorites():
    return load_data("favorites.json")

def save_favorites(favorites):
    save_data("favorites.json", favorites)

# Menu Utama
def user_menu(user):
    recipes = load_data("recipes.json")
    favorites = load_favorites()
    user_favorites = favorites.get(user['username'], [])

    while True:
        print(f"\n=== Main Menu, Halo selamat datang {user['username']} ===")
        print("1. Lihat Resep Berdasarkan Kategori")
        print("2. Lihat Resep Yang DiFavoritkan")
        print("3. Rekomendasi Resep")
        print("4. Cari Resep")
        print("5. Profile")
        print("6. Logout")

        pilihan = input("Pilih menu (1/2/3/4/5): ")

        if pilihan == '1':
            lihat_resep_berdasarkan_kategori(recipes, user)
        elif pilihan == '2':
            lihat_resep_favorit(user_favorites, favorites, user['username'])
        elif pilihan == '3':
            rekomendasi_resep(recipes)
        elif pilihan == '4':
            cari_resep(recipes)
        elif pilihan == '5':
            user_profile_menu(user)
        elif pilihan == '6':
            print("Logout berhasil. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# 1. Lihat Resep Berdasarkan Kategori
def lihat_resep_berdasarkan_kategori(recipes, user):
    categories = ["Makanan Ringan", "Makanan Berat", "Makanan Penutup", "Makanan Pembuka", "Minuman"]
    print("\nPilih kategori resep yang ingin dilihat:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")

    try:
        selected_index = int(input("Masukkan nomor kategori: ")) - 1
        if selected_index < 0 or selected_index >= len(categories):
            print("Pilihan kategori tidak valid!")
            return
        
        selected_category = categories[selected_index]
        filtered_recipes = [recipe for recipe in recipes if recipe.get("category") == selected_category]

        if not filtered_recipes:
            print(f"Tidak ada resep tersedia untuk kategori '{selected_category}'.")
            return

        for i, recipe in enumerate(filtered_recipes, 1):
            print(f"{i}. {recipe['title']}")

        selected_recipe_index = int(input("Pilih resep untuk melihat detail (masukkan nomor): ")) - 1
        if 0 <= selected_recipe_index < len(filtered_recipes):
            tampilkan_detail_resep(filtered_recipes[selected_recipe_index], user)
        else:
            print("Pilihan tidak valid!")

    except ValueError:
        print("Masukkan nomor yang valid!")

# 2. Lihat Resep Favorit
def lihat_resep_favorit(user_favorites, favorites, username):
    if not user_favorites:
        print("Anda belum memiliki resep yang difavoritkan.")
        return

    for i, recipe in enumerate(user_favorites, 1):
        print(f"{i}. {recipe['title']} oleh {recipe['author']}")

    try:
        selected_input = input("Pilih resep untuk melihat detail (masukkan nomor atau ketik 'keluar'): ").strip()
        if selected_input.lower() == 'keluar':
            return

        selected_recipe_index = int(selected_input) - 1
        if 0 <= selected_recipe_index < len(user_favorites):
            recipe = user_favorites[selected_recipe_index]
            print(f"\nJudul: {recipe['title']}")
            print(f"Deskripsi: {recipe['description']}")
            print(f"Bahan: {recipe['ingredients']}")
            print(f"Langkah: {recipe['steps']}")

            opsi = input("Hapus resep dari favorit? (y/n): ").strip().lower()
            if opsi == 'y':
                user_favorites.pop(selected_recipe_index)
                favorites[username] = user_favorites
                save_favorites(favorites)
                print("Resep dihapus dari favorit.")
        else:
            print("Pilihan tidak valid!")

    except ValueError:
        print("Masukkan nomor yang valid!")

# 3. Rekomendasi Resep Berdasarkan Penilaian
def rekomendasi_resep(recipes):
    ranked_recipes = sorted(
        recipes,
        key=lambda x: sum(x.get("nilai", [])) / len(x.get("nilai", [])) if x.get("nilai") else 0,
        reverse=True
    )

    print("\nRekomendasi Resep Teratas:")
    for i, recipe in enumerate(ranked_recipes[:5], 1):
        rata_rata = sum(recipe.get("nilai", [])) / len(recipe.get("nilai", [])) if recipe.get("nilai") else 0
        print(f"{i}. {recipe['title']} - Rata-rata Nilai: {rata_rata:.2f}")

# 4. Cari Resep
def cari_resep(recipes):
    keyword = input("Masukkan kata kunci untuk mencari resep: ").strip().lower()
    found_recipes = [recipe for recipe in recipes if keyword in recipe['title'].lower()]

    if found_recipes:
        for i, recipe in enumerate(found_recipes, 1):
            print(f"{i}. {recipe['title']}")
    else:
        print("Tidak ada resep yang cocok dengan kata kunci.")

# Tampilkan Detail Resep
def tampilkan_detail_resep(recipe, user):
    while True:
        # Muat ulang data setiap kali loop untuk memastikan data terbaru
        recipes = load_data("recipes.json")
        current_recipe = None
        
        # Cari resep dalam data
        for i, r in enumerate(recipes):
            if r['id'] == recipe['id']:
                current_recipe = recipes[i]
                recipe_index = i
                break
                
        if not current_recipe:
            print("Resep tidak ditemukan")
            return
            
        # Pastikan properti 'nilai' dan 'user_nilai' ada
        if 'nilai' not in current_recipe:
            current_recipe['nilai'] = []
        if 'user_nilai' not in current_recipe:
            current_recipe['user_nilai'] = []

        # Cek apakah user sudah menilai resep
        user_already_rated = any(u['id'] == user['id'] for u in current_recipe['user_nilai'])

        print(f"\nJudul: {current_recipe['title']}")
        print(f"Deskripsi: {current_recipe['description']}")
        print(f"Bahan: {', '.join(current_recipe['ingredients'])}")
        print(f"Langkah: {', '.join(current_recipe['steps'])}")

        if current_recipe['nilai']:
            rata_rata = sum(current_recipe['nilai']) / len(current_recipe['nilai'])
            print(f"Rata-rata Penilaian: {rata_rata:.2f}")

        print("\nPilih Opsi:")
        if user_already_rated:
            print("1. Ubah nilai untuk resep ini")
        else:
            print("1. Memberikan nilai untuk resep ini")
        print("2. Memberikan ulasan/komentar untuk resep ini")
        print("3. Menambahkan resep ini ke daftar favorit")
        print("4. Keluar ke menu utama")

        opsi = input("Pilih opsi (1/2/3/4): ").strip()

        if opsi == '1':
            try:
                nilai = int(input("Beri nilai (1-5): "))
                if 1 <= nilai <= 5:
                    if user_already_rated:
                        # Ubah nilai pengguna yang sudah ada
                        for u in current_recipe['user_nilai']:
                            if u['id'] == user['id']:
                                # Hapus nilai lama dari array nilai
                                old_rating_index = current_recipe['user_nilai'].index(u)
                                if old_rating_index < len(current_recipe['nilai']):
                                    current_recipe['nilai'].pop(old_rating_index)
                                # Update nilai user
                                u['nilai'] = nilai
                                # Tambahkan nilai baru ke array nilai
                                current_recipe['nilai'].append(nilai)
                                print("Nilai berhasil diperbarui!")
                                break
                    else:
                        # Tambahkan nilai baru
                        current_recipe['user_nilai'].append({
                            'id': user['id'], 
                            'username': user['username'], 
                            'nilai': nilai
                        })
                        current_recipe['nilai'].append(nilai)
                        print("Nilai berhasil ditambahkan!")
                    
                    # Update recipe dalam array recipes
                    recipes[recipe_index] = current_recipe
                    save_data("recipes.json", recipes)
                else:
                    print("Nilai harus antara 1 dan 5.")
            except ValueError:
                print("Masukkan angka yang valid!")

        elif opsi == '2':
            ulasan = input("Tulis ulasan Anda: ")
            current_recipe.setdefault('ulasan', []).append(ulasan)
            recipes[recipe_index] = current_recipe
            save_data("recipes.json", recipes)
            print("Ulasan berhasil ditambahkan!")

        elif opsi == '3':
            favorites = load_favorites()
            user_favorites = favorites.get(user['username'], [])
            
            # Cek apakah resep sudah ada di favorit berdasarkan ID
            recipe_exists = any(fav.get('id') == current_recipe['id'] for fav in user_favorites)
            
            if not recipe_exists:
                # Tambahkan seluruh data resep ke favorit
                favorite_recipe = {
                    'id': current_recipe['id'],
                    'title': current_recipe['title'],
                    'description': current_recipe['description'],
                    'ingredients': current_recipe['ingredients'],
                    'steps': current_recipe['steps'],
                    'category': current_recipe['category'],
                    'author': current_recipe['author']
                }
                
                # Tambahkan ulasan jika ada
                if 'ulasan' in current_recipe:
                    favorite_recipe['ulasan'] = current_recipe['ulasan']
                
                # Tambahkan nilai jika ada
                if 'nilai' in current_recipe:
                    favorite_recipe['nilai'] = current_recipe['nilai']
                
                user_favorites.append(favorite_recipe)
                favorites[user['username']] = user_favorites
                save_favorites(favorites)
                print("Resep ditambahkan ke favorit.")
            else:
                print("Resep sudah ada di daftar favorit.")

        elif opsi == '4':
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

#5. Fungsi untuk profil user
def view_profile(user):
    print(f"\n=== Profil ===")
    print(f"Nama Pengguna: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Role: {user['role']}")

def user_profile_menu(user):
    favorites = load_favorites()
    user_favorites = favorites.get(user['username'], [])
    while True:
        print(f"\n=== Profil Pengguna ===")
        view_profile(user)
        print("\nMenu:")
        print("1. Edit Profil")
        print("2. Lihat Resep Favorit")
        print("3. Kembali ke Menu Utama")
        pilihan = input("Pilih menu (1/2/3): ")
        if pilihan == '1':
            edit_profile(user)
        elif pilihan == '2':
            lihat_resep_favorit(user_favorites, favorites, user['username'])
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak valid.")

def get_valid_role(prompt="Pilih Role:\n1. User\n2. Chef\nPilih (1/2): "):
    while True:
        role_input = input(prompt)
        if role_input == '1':
            return 'User'
        elif role_input == '2':
            return 'Chef'
        else:
            print("Pilihan tidak valid! Pilih 1 atau 2.")

def edit_profile(user):
    while True:
        print("\nMenu Edit Profil:")
        print("1. Edit Nama")
        print("2. Edit Email")
        print("3. Edit Password")
        print("4. Edit Role")
        print("5. Kembali ke Menu Sebelumnya")
        pilihan = input("Pilih menu (1/2/3/4/5): ")

        users = load_users()
        user_index = next((i for i, u in enumerate(users) if u['id'] == user['id']), None)

        if user_index is None:
            print("Error: User tidak ditemukan")
            return

        if pilihan == '1':
            new_name = get_valid_username()
            user['username'] = new_name
            users[user_index]['username'] = new_name
            save_users(users)
            print("Nama berhasil diperbarui.")
                
        elif pilihan == '2':
            new_email = get_valid_email()
            user['email'] = new_email
            users[user_index]['email'] = new_email
            save_users(users)
            print("Email berhasil diperbarui.")
                
        elif pilihan == '3':
            new_password = get_valid_password()
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user['password'] = hashed_password.decode('utf-8')
            users[user_index]['password'] = hashed_password.decode('utf-8')
            save_users(users)
            print("Password berhasil diperbarui.")

        elif pilihan == '4':
            print(f"\nRole saat ini: {user['role']}")
            new_role = get_valid_role()
            user['role'] = new_role
            users[user_index]['role'] = new_role
            save_users(users)
            print("Role berhasil diperbarui.")
                
        elif pilihan == '5':
            break
        else:
            print("Pilihan tidak valid.")

# Fungsi menu untuk pengguna dengan role Chef
def chef_menu(user):
    while True:
        print(f"\n=== Main Menu, Halo selamat datang Chef {user['username']} ===")
        print("1. Tambahkan Resep Baru")
        print("2. Lihat Resep Keseluruhan")
        print("3. Lihat Resep Saya")
        # print("4. Edit Resep")
        # print("5. Hapus Resep")
        print("4. Cari Resep")
        print("5. Logout")

        pilihan = input("Pilih menu (1/2/3/4/5): ")

        if pilihan == '1':
            add_recipe(user)  # Panggil fungsi untuk menambahkan resep
        elif pilihan == '2':
            recipes = load_recipes()
            if not recipes:
                print("Belum ada resep yang tersedia.")
            else:
                print("Resep yang tersedia:")
                for i, recipe in enumerate(recipes, 1):
                    print(f"{i}. {recipe['title']} oleh {recipe['author']}")  # Menampilkan judul resep dan pembuat

                try:
                    selected_recipe_index = int(input("Pilih resep untuk melihat detail (masukkan nomor): ")) - 1
                    if selected_recipe_index < 0 or selected_recipe_index >= len(recipes):
                        print("Pilihan tidak valid!")
                        continue

                    selected_recipe = recipes[selected_recipe_index]
                    print("\nDetail Resep:")
                    print(f"Judul: {selected_recipe['title']}")
                    print(f"Deskripsi: {selected_recipe['description']}")
                    print(f"Bahan-bahan: {', '.join(selected_recipe['ingredients'])}")
                    print(f"Langkah-langkah: {', '.join(selected_recipe['steps'])}")
                    print(f"Dibuat oleh: {selected_recipe['author']}")
                except ValueError:
                    print("Pilihan tidak valid!")
        elif pilihan == '3':
            my_recipes = [recipe for recipe in load_recipes() if recipe['author'] == user['username']]
            if not my_recipes:
                print("Anda belum memiliki resep.")
            else:
                print("Resep Anda:")
                for i, recipe in enumerate(my_recipes, 1):
                    print(f"{i}. {recipe['title']}")  # Menampilkan hanya judul resep

                try:
                    selected_recipe_index = int(input("Pilih resep untuk melihat detail (masukkan nomor): ")) - 1
                    if selected_recipe_index < 0 or selected_recipe_index >= len(my_recipes):
                        print("Pilihan tidak valid!")
                        continue

                    selected_recipe = my_recipes[selected_recipe_index]
                    print("\nDetail Resep:")
                    print(f"Judul: {selected_recipe['title']}")
                    print(f"Deskripsi: {selected_recipe['description']}")
                    print(f"Bahan-bahan: {', '.join(selected_recipe['ingredients'])}")
                    print(f"Langkah-langkah: {', '.join(selected_recipe['steps'])}")
                    print(f"Kategori: {selected_recipe['category']}")  # Menampilkan kategori resep
                except ValueError:
                    print("Pilihan tidak valid!")
        # elif pilihan == '4':
        #     edit_recipe(user)
        # elif pilihan == '5':
        #     delete_recipe(user)
        elif pilihan == '4':  # Fitur pencarian resep
            keyword = input("Masukkan kata kunci pencarian: ").strip()
            if not keyword:
                print("Kata kunci tidak boleh kosong!")
            else:
                # Mencari resep berdasarkan kata kunci
                recipes = load_recipes()
                search_results = [recipe for recipe in recipes if keyword.lower() in recipe['title'].lower() or keyword.lower() in recipe['description'].lower()]

                if not search_results:
                    print("Tidak ada resep yang ditemukan.")
                else:
                    print("\nHasil Pencarian:")
                    for i, recipe in enumerate(search_results, 1):
                        print(f"{i}. {recipe['title']} oleh {recipe['author']}")

                    while True:
                        selected_input = input("Pilih resep untuk melihat detail (masukkan nomor atau ketik 'keluar' untuk kembali): ").strip()
                        
                        if selected_input.lower() == 'keluar':
                            print("Kembali ke menu awal...")
                            break
                        
                        try:
                            selected_recipe_index = int(selected_input) - 1
                            if selected_recipe_index < 0 or selected_recipe_index >= len(search_results):
                                print("Pilihan tidak valid! Silakan coba lagi.")
                                continue

                            selected_recipe = search_results[selected_recipe_index]
                            print("\nDetail Resep:")
                            print(f"Judul: {selected_recipe['title']}")
                            print(f"Deskripsi: {selected_recipe['description']}")
                            print(f"Bahan-bahan: {', '.join(selected_recipe['ingredients'])}")
                            print(f"Langkah-langkah: {', '.join(selected_recipe['steps'])}")
                            print(f"Dibuat oleh: {selected_recipe['author']}")
                            break
                        except ValueError:
                            print("Pilihan tidak valid! Masukkan nomor yang benar atau ketik 'keluar' untuk kembali.")
        elif pilihan == '5':
            print("Logout berhasil. Kembali ke menu utama.")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih menu yang benar.")


# Fungsi menu utama
def main_menu():
    while True:
        print("\n=== Aplikasi Resep ===")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")

        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == '1':
            user = login()
            if user:
                if user['role'] == 'User':
                    user_menu(user)  # Masuk ke menu User
                elif user['role'] == 'Chef':
                    chef_menu(user)  # Masuk ke menu Chef
        elif pilihan == '2':
            register()  # Registrasi pengguna baru
        elif pilihan == '3':
            print("Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih menu yang benar.")