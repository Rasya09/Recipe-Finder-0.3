import bcrypt
from auth_app import get_valid_email, get_valid_password, get_valid_username, register, login, json
from resep import add_recipe, delete_recipe, delete_recipe_interactive, edit_recipe, edit_recipe_interactive, load_recipes

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
        print("5. Lihat Resep Dengan Waktu Tertentu")
        print("6. Lihat resep dengan visual memasak")
        print("7. Profile")
        print("8. Logout")

        pilihan = input("Pilih menu (1/2/3/4/5/6/7/8): ")

        if pilihan == '1':
            lihat_resep_berdasarkan_kategori(recipes, user)
        elif pilihan == '2':
            lihat_resep_favorit(user_favorites, favorites, user['username'], user)
        elif pilihan == '3':
            rekomendasi_resep(recipes, user)
        elif pilihan == '4':
            cari_resep(recipes)
        elif pilihan == '5':
            lihat_resep_dengan_waktu(recipes, user)
        elif pilihan == '6':
            visual_resep(recipes,user)
        elif pilihan == "7":
            user_profile_menu(user)
        elif pilihan == '8':
            print("Logout berhasil. Sampai jumpa!")
            main_menu()
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
def lihat_resep_favorit(user_favorites, favorites, username, user):  # Tambahkan parameter user
    if not user_favorites:
        print("Anda belum memiliki resep yang difavoritkan.")
        return

    while True:
        print("\n=== Resep Favorit ===")
        for i, recipe in enumerate(user_favorites, 1):
            print(f"{i}. {recipe['title']} oleh {recipe['author']}")

        try:
            selected_input = input("\nPilih resep untuk melihat detail (masukkan nomor atau ketik 'keluar'): ").strip()
            if selected_input.lower() == 'keluar':
                return

            selected_recipe_index = int(selected_input) - 1
            if 0 <= selected_recipe_index < len(user_favorites):
                selected_recipe = user_favorites[selected_recipe_index]
                
                # Langsung menggunakan objek user yang diterima dari parameter
                tampilkan_detail_resep(selected_recipe, user)
                
            else:
                print("⚠️ Pilihan tidak valid!")

        except ValueError:
            print("⚠️ Masukkan nomor yang valid!")

# 3. Rekomendasi Resep Berdasarkan Penilaian
def rekomendasi_resep(recipes, user):  # Tambahkan user sebagai parameter
    ranked_recipes = sorted(
        recipes,
        key=lambda x: sum(x.get("nilai", [])) / len(x.get("nilai", [])) if x.get("nilai") else 0,
        reverse=True
    )

    print("\nRekomendasi Resep Teratas:")
    for i, recipe in enumerate(ranked_recipes[:5], 1):
        rata_rata = sum(recipe.get("nilai", [])) / len(recipe.get("nilai", [])) if recipe.get("nilai") else 0
        print(f"{i}. {recipe['title']} - Rata-rata Nilai: {rata_rata:.2f}")
    
    while True:
        pilihan = input("\nPilih nomor resep untuk melihat detailnya (1-5) atau tekan '0' untuk kembali ke menu utama: ")
        
        if pilihan == '0':
            break
        elif pilihan in [str(i) for i in range(1, 6)]:
            index = int(pilihan) - 1
            selected_recipe = ranked_recipes[index]
            tampilkan_detail_resep(selected_recipe, user)
        else:
            print("Pilihan tidak valid. Silakan pilih nomor antara 1-5 atau 0 untuk kembali.")

# 4. Cari Resep
def cari_resep(recipes):
    keyword = input("Masukkan kata kunci untuk mencari resep: ").strip().lower()
    found_recipes = []

    # Pencarian berdasarkan judul atau bahan
    for recipe in recipes:
        if keyword in recipe['title'].lower() or any(keyword in ingredient.lower() for ingredient in recipe.get('ingredients', [])):
            found_recipes.append(recipe)

    # Tampilkan hasil pencarian
    if found_recipes:
        print("\nResep yang ditemukan:")
        for i, recipe in enumerate(found_recipes, 1):
            print(f"{i}. {recipe['title']}")
    else:
        print("Tidak ada resep yang cocok dengan kata kunci.")

# 5. Lihat Resep Berdasarkan Waktu Tertentu
def lihat_resep_dengan_waktu(recipes, user):
    """
    Menampilkan resep berdasarkan waktu memasak yang diinginkan pengguna dan memungkinkan untuk melihat detail resep.
    """
    try:
        waktu = int(input("\nMasukkan waktu memasak yang diinginkan (dalam menit): "))
        
        if waktu <= 0:
            print("⚠️ Waktu harus lebih dari 0 menit.")
            return
        
        # Filter resep berdasarkan waktu
        resep_sesuai = [resep for resep in recipes if resep.get('time') and int(resep['time']) <= waktu]
        
        if resep_sesuai:
            print(f"\n📚 Resep dengan waktu memasak {waktu} menit atau kurang:")
            for idx, resep in enumerate(resep_sesuai, start=1):
                print(f"{idx}. {resep['title']} - Waktu Memasak: {resep['time']} menit")
            
            while True:
                try:
                    pilihan = input("\n🔍 Pilih resep untuk melihat detail (masukkan nomor, atau 'keluar' untuk keluar): ").strip()
                    if pilihan.lower() == 'keluar':
                        print("🔙 Kembali ke menu utama...")
                        return
                    
                    pilihan_idx = int(pilihan) - 1
                    if 0 <= pilihan_idx < len(resep_sesuai):
                        tampilkan_detail_resep(resep_sesuai[pilihan_idx], user)
                        break
                    else:
                        print("⚠️ Nomor tidak valid. Silakan pilih dari daftar.")
                except ValueError:
                    print("⚠️ Masukkan angka yang valid atau 'q' untuk keluar.")
        else:
            print("\n❌ Tidak ada resep yang sesuai dengan waktu yang dimasukkan.")
    
    except ValueError:
        print("⚠️ Harap masukkan angka yang valid untuk waktu memasak.")

#6. Fungsi untuk melihat resep dengan visual
def visual_resep(recipes,user):
    #filter resep berdasarkan visual
    resep_visual = [resep for resep in recipes if resep.get('link')]
    if resep_visual:
        print("\nResep dengan visual memasak")
        for idx, resep in enumerate(resep_visual, start=1):
            print(f"{idx}. {resep['title']}")

        while True:
            try:
                pilihan = input("\n🔍 Pilih resep untuk melihat detail (masukkan nomor, atau 'keluar' untuk keluar): ").strip()                    
                if pilihan.lower() == 'keluar':
                    print("🔙 Kembali ke menu utama...")
                    return
                    
                pilihan_idx = int(pilihan) - 1
                if 0 <= pilihan_idx < len(resep_visual):
                    tampilkan_detail_resep(resep_visual[pilihan_idx], user)
                    break
                else:
                    print("⚠️ Nomor tidak valid. Silakan pilih dari daftar.")
            except ValueError:
                print("⚠️ Masukkan angka yang valid atau 'q' untuk keluar.")
    else:
        print("Tidak ada resep dengan visual memasak")

# Tampilkan Detail Resep
def tampilkan_detail_resep(recipe, user):
    while True:
        # Muat ulang data setiap iterasi
        recipes = load_data("recipes.json")
        current_recipe = next((r for r in recipes if r['id'] == recipe['id']), None)
        
        if not current_recipe:
            print("Resep tidak ditemukan.")
            return False
        
        # Pastikan properti yang dibutuhkan ada
        current_recipe.setdefault('nilai', [])
        current_recipe.setdefault('user_nilai', [])
        current_recipe.setdefault('ulasan', [])

        # Cek apakah user sudah menilai resep
        user_already_rated = any(u['id'] == user['id'] for u in current_recipe['user_nilai'])

        print(f"\n=== Detail Resep ===")
        print(f"📌 Judul: {current_recipe['title']}")
        print(f"📖 Deskripsi: {current_recipe['description']}")
        print(f"\n🥗 Bahan:")
        for i, bahan in enumerate(current_recipe['ingredients'], start=1):
            print(f"   {i}. {bahan}")
        print(f"\n👨‍🍳 Langkah:")
        for i, langkah in enumerate(current_recipe['steps'], start=1):
            print(f"   {i}. {langkah}")

        print(f"\nWaktu Memasak : {current_recipe['time']} menit\n")

        for i, ulasan in enumerate(current_recipe['ulasan'], start=1):
            print(f"{i}, {ulasan}")
        
        if current_recipe['nilai']:
            rata_rata = sum(current_recipe['nilai']) / len(current_recipe['nilai'])
            print(f"\n⭐ Rata-rata Penilaian: {rata_rata:.2f}")

        print(f"\nCara memasak bisa lihat di : {current_recipe['link']}")

        # Opsi untuk pengguna
        print("\n🔑 Pilih Opsi:")
        print("1. Ubah/Masukkan nilai untuk resep ini" if user_already_rated else "1. Berikan nilai untuk resep ini")
        print("2. Tambahkan ulasan untuk resep ini")
        print("3. Tambahkan ke daftar favorit")
        print("4. Kembali ke menu utama")
        
        opsi = input("Pilih opsi (1/2/3/4): ").strip()

        if opsi == '1':  
            # Memberi atau memperbarui nilai
            try:
                nilai = int(input("🎯 Masukkan nilai (1-5): "))
                if 1 <= nilai <= 5:
                    if user_already_rated:
                        for u in current_recipe['user_nilai']:
                            if u['id'] == user['id']:
                                current_recipe['nilai'].remove(u['nilai'])
                                u['nilai'] = nilai
                                current_recipe['nilai'].append(nilai)
                                print("✅ Nilai berhasil diperbarui!")
                                break
                    else:
                        current_recipe['user_nilai'].append({
                            'id': user['id'],
                            'username': user['username'],
                            'nilai': nilai
                        })
                        current_recipe['nilai'].append(nilai)
                        print("✅ Nilai berhasil ditambahkan!")

                    save_data("recipes.json", recipes)
                else:
                    print("⚠️ Nilai harus antara 1 dan 5.")
            except ValueError:
                print("⚠️ Harap masukkan angka yang valid.")

        elif opsi == '2':  
            # Memberikan ulasan
            ulasan = input("💬 Tulis ulasan Anda: ").strip()
            if ulasan:
                current_recipe['ulasan'].append({
                    'id': user['id'],
                    'username': user['username'],
                    'ulasan': ulasan
                })
                save_data("recipes.json", recipes)
                print("✅ Ulasan berhasil ditambahkan!")
            else:
                print("⚠️ Ulasan tidak boleh kosong.")

        elif opsi == '3':  
            # Tambahkan ke favorit
            favorites = load_favorites()
            user_favorites = favorites.get(user['username'], [])
            
            if not any(fav['id'] == current_recipe['id'] for fav in user_favorites):
                favorite_recipe = {
                    'id': current_recipe['id'],
                    'title': current_recipe['title'],
                    'description': current_recipe['description'],
                    'ingredients': current_recipe['ingredients'],
                    'steps': current_recipe['steps'],
                    'category': current_recipe['category'],
                    'author': current_recipe['author']
                }
                
                if 'ulasan' in current_recipe:
                    favorite_recipe['ulasan'] = current_recipe['ulasan']
                if 'nilai' in current_recipe:
                    favorite_recipe['nilai'] = current_recipe['nilai']
                
                user_favorites.append(favorite_recipe)
                favorites[user['username']] = user_favorites
                save_favorites(favorites)
                print("✅ Resep berhasil ditambahkan ke favorit!")
            else:
                print("⚠️ Resep sudah ada di daftar favorit.")

        elif opsi == '4':  
            # Kembali ke menu utama
            print("🔙 Kembali ke menu utama...")
            user_menu(user)
            # break
            # return True

        else:
            print("⚠️ Pilihan tidak valid. Silakan coba lagi.")



#7. Fungsi untuk profil user
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
            result = edit_profile(user)
            if result == "role_changed":
                if user['role'] == 'Chef':
                    print("\nAnda telah berganti role menjadi Chef. Mengalihkan ke menu Chef...")
                    chef_menu(user)
                    return  # Keluar dari profile_menu dan kembali ke main_menu
                elif user['role'] == 'User':
                    print("\nAnda telah berganti role menjadi User. Mengalihkan ke menu User...")
                    user_menu(user)
                    return  # Keluar dari profile_menu dan kembali ke main_menu
        elif pilihan == '2':
            lihat_resep_favorit(user_favorites, favorites, user['username'])
        elif pilihan == '3':
            return  # Kembali ke menu sebelumnya
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
            new_email = get_valid_email(users=users, current_user_id=user['id'])
            if new_email != user['email']:  # Periksa jika email benar-benar berubah
                user['email'] = new_email
                users[user_index]['email'] = new_email
                save_users(users)
                print("Email berhasil diperbarui.")
            else:
                print("Email sama dengan yang sudah ada, tidak ada perubahan.")
                
        elif pilihan == '3':
            new_password = get_valid_password()
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user['password'] = hashed_password.decode('utf-8')
            users[user_index]['password'] = hashed_password.decode('utf-8')
            save_users(users)
            print("Password berhasil diperbarui.")

        elif pilihan == '4':
            print(f"\nRole saat ini: {user['role']}")
            old_role = user['role']
            new_role = get_valid_role()
            if new_role != old_role:
                user['role'] = new_role
                users[user_index]['role'] = new_role
                save_users(users)
                print(f"Role berhasil diubah dari {old_role} menjadi {new_role}")
                return "role_changed"
                
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
        print("4. Cari Resep")
        print("5. Profile")
        # print("5. Hapus Resep")
        print("6. Logout")

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
                    print(f"Waktu Memasak: {selected_recipe['time']}")
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
                    print(f"{i}. {recipe['title']}")

                try:
                    selected_recipe_index = int(input("Pilih resep untuk melihat detail (masukkan nomor): ")) - 1
                    if 0 <= selected_recipe_index < len(my_recipes):
                        selected_recipe = my_recipes[selected_recipe_index]
                        print("\nDetail Resep:")
                        print(f"Judul: {selected_recipe['title']}")
                        print(f"Deskripsi: {selected_recipe['description']}")
                        print(f"Bahan-bahan: {', '.join(selected_recipe['ingredients'])}")
                        print(f"Langkah-langkah: {', '.join(selected_recipe['steps'])}")
                        print(f"Kategori: {selected_recipe['category']}")
                        print(f"Waktu Memasak: {selected_recipe['time']} menit")

                        while True:
                            print("\nPilih Opsi")
                            print("1. Edit Resep")
                            print("2. Hapus Resep")
                            print("3. Keluar")

                            sub_pilihan = input("Pilih Menu (1/2/3): ")

                            if sub_pilihan == '1':
                                edit_recipe_interactive(selected_recipe)
                            elif sub_pilihan == '2':
                                delete_recipe_interactive(selected_recipe)
                                print("Resep berhasil dihapus.")
                                break
                            elif sub_pilihan == '3':
                                break
                            else:
                                print("Pilihan tidak valid!")
                    else:
                        print("Pilihan tidak valid!")
                except ValueError:
                    print("Harap masukkan angka yang valid!")
        # elif pilihan == '4':
        #     edit_recipe(user)
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
            user_profile_menu(user)
        elif pilihan == '6':
            print("Logout berhasil. Kembali ke menu utama.")
            main_menu()
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
            quit()
        else:
            print("Pilihan tidak valid! Silakan pilih menu yang benar.")