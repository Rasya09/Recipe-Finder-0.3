import json
import os

# File JSON tempat menyimpan data resep
RECIPES_FILE = 'recipes.json'

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

# Fungsi untuk membuat ID resep otomatis
def generate_recipe_id(recipes):
    if not recipes:
        return 1
    return max(recipe['id'] for recipe in recipes) + 1


# Fungsi untuk menambahkan resep
def add_recipe(chef):
    print("\n=== Tambahkan Resep Baru ===")
    recipes = load_recipes()

    # Pilih kategori resep
    categories = ["Makanan Ringan", "Makanan Berat", "Makanan Penutup", "Makanan Pembuka", "Minuman"]
    print("\nPilih Kategori Resep:")
    for idx, category in enumerate(categories, 1):
        print(f"{idx}. {category}")

    while True:
        try:
            category_choice = int(input("Pilih kategori (1/2/3/4/5): "))
            if 1 <= category_choice <= len(categories):
                category = categories[category_choice - 1]
                break
            else:
                print("Pilihan tidak valid! Pilih kategori antara 1 hingga 5!")
        except ValueError:
            print("Pilihan tidak valid! Masukkan angka yang sesuai.")

    # Input data resep
    while True:
        title = input("Masukkan judul resep: ").strip()
        if len(title) < 1:
            print("Judul tidak boleh kosong. Masukkan minimal 1 kalimat.")
        else:
            break

    while True:
        description = input("Masukkan deskripsi resep: ").strip()
        if len(description) < 1:
            print("Deskripsi tidak boleh kosong. Masukkan minimal 1 kalimat.")
        else:
            break

    # Input bahan-bahan secara satu per satu
    ingredients = []
    print("Masukkan bahan-bahan (ketik 'selesai' jika sudah, 'kembali' untuk kembali, 'keluar' untuk membatalkan):")
    while True:
        ingredient = input("Bahan: ").strip()
        if ingredient.lower() == 'selesai':
            if len(ingredients) < 3:
                print("Minimal harus ada 3 bahan.")
            else:
                break
        elif ingredient.lower() == 'kembali':
            if ingredients:
                removed = ingredients.pop()
                print(f"Bahan terakhir '{removed}' dihapus.")
            else:
                print("Tidak ada bahan yang bisa dihapus.")
        elif ingredient.lower() == 'keluar':
            print("Proses penambahan resep dibatalkan.")
            return
        elif len(ingredient) < 1:
            print("Bahan tidak boleh kosong. Masukkan minimal 1 kalimat.")
        else:
            ingredients.append(ingredient)

    # Input langkah-langkah secara satu per satu
    steps = []
    print("Masukkan langkah-langkah (ketik 'selesai' jika sudah, 'kembali' untuk kembali, 'keluar' untuk membatalkan):")
    while True:
        step = input("Langkah: ").strip()
        if step.lower() == 'selesai':
            if len(steps) < 3:
                print("Minimal harus ada 3 langkah.")
            else:
                break
        elif step.lower() == 'kembali':
            if steps:
                removed = steps.pop()
                print(f"Langkah terakhir '{removed}' dihapus.")
            else:
                print("Tidak ada langkah yang bisa dihapus.")
        elif step.lower() == 'keluar':
            print("Proses penambahan resep dibatalkan.")
            return
        elif len(step) < 1:
            print("Langkah tidak boleh kosong. Masukkan minimal 1 kalimat.")
        else:
            steps.append(step)

    # Buat ID resep otomatis
    recipe_id = generate_recipe_id(recipes)

    # Tambahkan resep ke dalam list
    recipes.append({
        "id": recipe_id,
        "title": title,
        "description": description,
        "ingredients": ingredients,
        "steps": steps,
        "category": category,  # Menyimpan kategori resep
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
    
    # Mengubah bahan-bahan secara satu per satu
    new_ingredients = []
    print("Masukkan bahan-bahan baru (ketik 'selesai' jika sudah):")
    while True:
        ingredient = input("Bahan: ")
        if ingredient.lower() == 'selesai':
            break
        new_ingredients.append(ingredient.strip())
    
    # Mengubah langkah-langkah secara satu per satu
    new_steps = []
    print("Masukkan langkah-langkah baru (ketik 'selesai' jika sudah):")
    while True:
        step = input("Langkah: ")
        if step.lower() == 'selesai':
            break
        new_steps.append(step.strip())

    recipe_to_edit['title'] = new_title
    recipe_to_edit['description'] = new_description
    recipe_to_edit['ingredients'] = new_ingredients
    recipe_to_edit['steps'] = new_steps

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
