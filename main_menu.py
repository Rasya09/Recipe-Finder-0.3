from auth_app import register, login, add_recipe, edit_recipe, delete_recipe, load_recipes

# Fungsi menu untuk pengguna dengan role User
def user_menu(user):
    while True:
        print(f"\n=== Main Menu, Halo selamat Datang {user['username']} ===")
        print("1. Lihat Resep")
        print("2. Favoritkan Resep")
        print("3. Logout")

        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == '1':
            recipes = load_recipes()
            if not recipes:
                print("Belum ada resep yang tersedia.")
            else:
                print("Resep yang tersedia:")
                for i, recipe in enumerate(recipes, 1):
                    print(f"{i}. {recipe['title']}")  # Menampilkan hanya judul resep

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
                except ValueError:
                    print("Pilihan tidak valid!")
        elif pilihan == '2':
            print("Menambahkan resep ke daftar favorit...")
        elif pilihan == '3':
            print("Logout berhasil. Kembali ke menu utama.")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih menu yang benar.")

# Fungsi menu untuk pengguna dengan role Chef
def chef_menu(user):
    while True:
        print(f"\n=== Main Menu, Halo Selamat Datang Chef {user['username']} ===")
        print("1. Tambahkan Resep Baru")
        print("2. Lihat Resep Saya")
        print("3. Edit Resep")
        print("4. Hapus Resep") 
        print("5. Logout")

        pilihan = input("Pilih menu (1/2/3/4/5): ")

        if pilihan == '1':
            add_recipe(user)  # Panggil fungsi untuk menambahkan resep
        elif pilihan == '2':
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
                except ValueError:
                    print("Pilihan tidak valid!")
        elif pilihan == '3':
            edit_recipe(user)  # Panggil fungsi untuk mengedit resep
        elif pilihan == '4':
            delete_recipe(user)  # Panggil fungsi untuk menghapus resep
        elif pilihan == '5':
            print("Logout berhasil. Kembali ke menu utama.")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih menu yang benar.")

# Fungsi menu utama
def main_menu():
    while True:
        print("\n=== Menu Utama Aplikasi ===")
        print("1. Register")
        print("2. Login")
        print("3. Keluar")

        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == '1':
            register()
        elif pilihan == '2':
            user = login()  # Login akan mengembalikan data user
            if user:  # Jika login berhasil
                if user['role'] == 'User':
                    user_menu(user)
                elif user['role'] == 'Chef':
                    chef_menu(user)
        elif pilihan == '3':
            print("Terima kasih telah menggunakan aplikasi. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih menu yang benar.")
