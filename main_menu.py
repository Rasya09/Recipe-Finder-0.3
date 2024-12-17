from auth_app import register, login

# Fungsi menu setelah login berhasil
def after_login_menu():
    while True:
        print("\n=== Menu Setelah Login ===")
        print("1. Lihat Profil")
        print("2. Logout")

        pilihan = input("Pilih menu (1/2): ")

        if pilihan == '1':
            print("Ini adalah menu profil (bisa dikembangkan lebih lanjut).")
        elif pilihan == '2':
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
            if login():  # Jika login berhasil
                after_login_menu()
        elif pilihan == '3':
            print("Terima kasih telah menggunakan aplikasi. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih menu yang benar.")
