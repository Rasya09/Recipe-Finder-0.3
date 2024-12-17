from auth_app import register, login

# Fungsi menu untuk pengguna dengan role User
def user_menu(user):
    while True:
        print(f"\n=== Main Menu, Halo selamat Datang {user['username']} ===")
        print("1. Lihat Resep")
        print("2. Favoritkan Resep")
        print("3. Logout")

        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == '1':
            print("Menampilkan resep-resep yang tersedia...")
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
        print("3. Logout")

        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == '1':
            print("Menambahkan resep baru...")
        elif pilihan == '2':
            print("Menampilkan daftar resep Anda...")
        elif pilihan == '3':
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
