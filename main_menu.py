from auth_app import register, login, add_recipe, edit_recipe, delete_recipe, load_recipes, json, os

# Fungsi menu untuk pengguna dengan role User
def user_menu(user):
    while True:
        print(f"\n=== Main Menu, Halo selamat datang {user['username']} ===")
        print("1. Lihat Resep")
        print("2. Favoritkan Resep")
        print("3. Logout")

        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == '1':
            recipes = load_recipes()
            if not recipes:
                print("Belum ada resep yang tersedia.")
                continue

            # Daftar kategori yang tersedia
            categories = ["Makanan Ringan", "Makanan Berat", "Makanan Penutup", "Makanan Pembuka", "Cemilan", "Minuman"]
            print("\nPilih kategori resep yang ingin dilihat:")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")

            try:
                selected_category_index = int(input("Masukkan nomor kategori: ")) - 1
                if selected_category_index < 0 or selected_category_index >= len(categories):
                    print("Pilihan kategori tidak valid!")
                    continue

                selected_category = categories[selected_category_index]
                filtered_recipes = [recipe for recipe in recipes if recipe.get("category") == selected_category]

                if not filtered_recipes:
                    print(f"Tidak ada resep tersedia untuk kategori '{selected_category}'.")
                    continue

                print(f"\nResep yang tersedia di kategori '{selected_category}':")
                for i, recipe in enumerate(filtered_recipes, 1):
                    print(f"{i}. {recipe['title']}")

                try:
                    selected_recipe_index = int(input("Pilih resep untuk melihat detail (masukkan nomor): ")) - 1
                    if selected_recipe_index < 0 or selected_recipe_index >= len(filtered_recipes):
                        print("Pilihan tidak valid!")
                        continue

                    selected_recipe = filtered_recipes[selected_recipe_index]
                    print("\nDetail Resep:")
                    print(f"Judul: {selected_recipe['title']}")
                    print(f"Deskripsi: {selected_recipe['description']}")
                    print(f"Bahan-bahan: {', '.join(selected_recipe['ingredients'])}")
                    print(f"Langkah-langkah: {', '.join(selected_recipe['steps'])}")
                    print(f"Kategori: {selected_recipe['category']}")

                    #Menampilkan penilaian rata-rata jika ada
                    if "nilai" in selected_recipe and selected_recipe["nilai"]:
                        rata_rata_nilai = sum(selected_recipe["nilai"]) / len(selected_recipe["nilai"])
                        print(f"Penilaian rata-rata: {rata_rata_nilai} dari {len(selected_recipe["nilai"])} penilaian")
                    else:
                        print("Belum ada penilaian untuk resep ini")
                    
                    #Menampilkan ulasan jika ada
                    if "ulasan" in selected_recipe and selected_recipe["ulasan"]:
                        print("\nUlasan pengguna:")
                        for komentar in selected_recipe["ulasan"]:
                            print(f"-{komentar}")
                    else:
                        print("Belum ada ulasan untuk resep ini")
                    
                    #Function untuk menambah nilai
                    def add_nilai():
                        nilai = int(input("Berikan penilaian untuk resep ini (1-5): "))
                        if 1<= nilai <= 5:
                            selected_recipe.setdefault("nilai", []).append(nilai)
                            print("Nilai berhasil ditambahkan")
                            return True                           
                        else:
                            print("Nilai harus dalam rentang 1-5")
                            return False
                    #Function untuk menambah ulasan
                    def add_ulasan():
                        ulasan = input("Tuliskan ulasan Anda: ").strip()
                        if not ulasan:
                            print("Ulasan tidak boleh kosong")
                            return False
                        else:
                            selected_recipe.setdefault("ulasan", []).append(ulasan)
                            print("Ulasan berhasil ditambahkan")
                            return True

                    #Menambahkan nilai pada resep
                    memberi_nilai = input("\nApakah Anda ingin memberikan penilaian pada resep ini? (y/n): ")
                    if memberi_nilai.lower() == "y":
                        add_nilai()
                    
                    #Menambahkan ulasan pada resep
                    memberi_ulasan = input("Apakah Anda ingin memberikan ulasan pada resep ini? (y/n): ")
                    if memberi_ulasan.lower() == "y":
                        add_ulasan()

                    # Menyimpan perubahan ke file JSON
                    with open("recipes.json", "w") as file:
                        json.dump(recipes, file, indent=4)
                    print("Data berhasil diperbarui.")

                except ValueError:
                    print("Pilihan tidak valid!")
            except ValueError:
                print("Masukkan angka yang sesuai untuk memilih kategori.")
        elif pilihan == '2':
            print("Menambahkan resep ke daftar favorit... (fitur belum diimplementasikan)")
        elif pilihan == '3':
            print("Logout berhasil. Kembali ke menu utama.")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih menu yang benar.")


# Fungsi menu untuk pengguna dengan role Chef
def chef_menu(user):
    while True:
        print(f"\n=== Main Menu, Halo selamat datang Chef {user['username']} ===")
        print("1. Tambahkan Resep Baru")
        print("2. Lihat Resep Keseluruhan")
        print("3. Lihat Resep Saya")
        print("4. Edit Resep")
        print("5. Hapus Resep") 
        print("6. Logout")

        pilihan = input("Pilih menu (1/2/3/4/5/6): ")

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
        elif pilihan == '4':
            edit_recipe(user)  # Panggil fungsi untuk mengedit resep
        elif pilihan == '5':
            delete_recipe(user)  # Panggil fungsi untuk menghapus resep
        elif pilihan == '6':
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