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

def search_recipe(keyword):
    recipes = load_recipes()
    # Menggunakan list comprehension untuk mencari resep yang judul atau deskripsi mengandung keyword
    results = [recipe for recipe in recipes if keyword.lower() in recipe['title'].lower() or keyword.lower() in recipe['description'].lower()]
    return results

# Fungsi menyimpan data resep ke file JSON
def save_recipes(data):
    with open(RECIPES_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Fungsi untuk membuat ID resep otomatis
def generate_recipe_id(recipes):
    if not recipes:
        return 1
    return max(recipe['id'] for recipe in recipes) + 1

def save_recipes_to_file(updated_recipe):
    recipes = load_recipes()
    for i, recipe in enumerate(recipes):
        if recipe['title'] == updated_recipe['title']:
            recipes[i] = updated_recipe
            break
    with open('recipes.json', 'w') as file:
        json.dump(recipes, file, indent=4)

def show_latest_recipes(recipes):
    recipes = load_recipes()
    recipes.sort(key=lambda x: x['id'], reverse=True)  # Asumsi 'id' bertambah
    latest_recipes = recipes[:5]  
    print("Notifikasi: Resep terbaru yang ditambahkan:\n")
    for recipe in latest_recipes:
        print(f"{recipe['title']} - {recipe['category']}")
        print('-' * 50)

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

    # menambahkan waktu memasak
    while True:
        time = input("Masukkan waktu memasak resep (menit): ").strip()
        if len(time) < 1:
            print("waktu memasak tidak boleh kosong")
        else:
            break

    # menambahkan visual memasak
    while True:
        link = input("Masukkan link video memasak resep (jika tidak ada kosongkan): ").strip()
        break

    # Buat ID resep otomatis
    recipe_id = generate_recipe_id(recipes)

    # Tambahkan resep ke dalam list
    recipes.append({
        "id": recipe_id,
        "title": title,
        "description": description,
        "ingredients": ingredients,
        "steps": steps,
        "category": category,
        "time": time,
        "link":link,
        "author": chef['username']  # Menyimpan nama Chef sebagai pembuat resep
    })

    # Simpan data ke file JSON
    save_recipes(recipes)
    print("Resep berhasil ditambahkan!")

# Fungsi untuk mengedit resep
def edit_recipe(user):
    print("\n=== Edit Resep Anda ===")
    my_recipes = [recipe for recipe in load_recipes() if recipe['author'] == user['username']]
    
    if not my_recipes:
        print("Anda belum memiliki resep untuk diedit.")
        return
    
    # Tampilkan resep pengguna
    for i, recipe in enumerate(my_recipes, 1):
        print(f"{i}. {recipe['title']}")

    try:
        choice = int(input("Pilih resep yang ingin diedit (masukkan nomor): ")) - 1
        if choice < 0 or choice >= len(my_recipes):
            print("Pilihan tidak valid!")
            return
        
        selected_recipe = my_recipes[choice]
        print(f"\nMengedit Resep: {selected_recipe['title']}")
        
        # Edit atribut resep
        selected_recipe['title'] = input(f"Judul ({selected_recipe['title']}): ").strip() or selected_recipe['title']
        selected_recipe['description'] = input(f"Deskripsi ({selected_recipe['description']}): ").strip() or selected_recipe['description']
        
        print("Edit Bahan (kosongkan untuk melewati):")
        for i, ingredient in enumerate(selected_recipe['ingredients'], 1):
            new_ingredient = input(f"Bahan {i} ({ingredient}): ").strip()
            if new_ingredient:
                selected_recipe['ingredients'][i-1] = new_ingredient
        
        print("Edit Langkah (kosongkan untuk melewati):")
        for i, step in enumerate(selected_recipe['steps'], 1):
            new_step = input(f"Langkah {i} ({step}): ").strip()
            if new_step:
                selected_recipe['steps'][i-1] = new_step

        save_recipes(load_recipes())  # Simpan semua resep yang diperbarui
        print("Resep berhasil diperbarui!")
    
    except ValueError:
        print("Masukkan angka yang valid!")

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

def edit_recipe_interactive(recipe):
    print(f"\nMengedit Resep: {recipe['title']}")
    
    # Edit Judul
    new_title = input(f"Judul ({recipe['title']}) klik 'enter' jika judulnya sama: ").strip()
    if new_title:
        recipe['title'] = new_title
    
    # Edit Deskripsi
    new_description = input(f"Deskripsi ({recipe['description']}) klik 'enter' jika deskripsinya sama: ").strip()
    if new_description:
        recipe['description'] = new_description
    
    # Edit Bahan-bahan
    print("\nEdit Bahan (ketik 'selesai' jika sudah selesai memasukkan bahan baru, data tidak diperbolehkan kosong):")
    new_ingredients = []
    index = 1
    while True:
        new_ingredient = input(f"Bahan {index}: ").strip()
        if new_ingredient.lower() == 'selesai':
            if len(new_ingredients) < 3:
                print("Minimal harus ada 3 bahan.")
            else:
                break
        elif new_ingredient.lower() == 'kembali':
            if new_ingredients:
                removed = new_ingredients.pop()
                print(f"Bahan terakhir '{removed}' dihapus.")
                index -= 1
            else:
                print("Tidak ada bahan yang bisa dihapus.")
        elif new_ingredient.lower() == 'keluar':
            print("Proses pengeditan resep dibatalkan.")
            return
        elif len(new_ingredient) < 1:
            print("Bahan tidak boleh kosong. Masukkan minimal 1 kalimat.")
        else:
            new_ingredients.append(new_ingredient)
            index += 1
    
    if new_ingredients:
        recipe['ingredients'] = new_ingredients  # Ganti semua bahan lama dengan yang baru
    
    # Edit Langkah-langkah
    print("\nEdit Langkah (ketik 'selesai' jika sudah selesai memasukkan langkah baru, data tidak diperbolehkan kosong):")
    new_steps = []
    step_index = 1
    while True:
        new_step = input(f"Langkah {step_index}: ").strip()
        if new_step.lower() == 'selesai':
            if len(new_steps) < 3:
                print("Minimal harus ada 3 langkah.")
            else:
                break
        elif new_step.lower() == 'kembali':
            if new_steps:
                removed = new_steps.pop()
                print(f"Langkah terakhir '{removed}' dihapus.")
                step_index -= 1
            else:
                print("Tidak ada langkah yang bisa dihapus.")
        elif new_step.lower() == 'keluar':
            print("Proses pengeditan resep dibatalkan.")
            return
        elif len(new_step) < 1:
            print("Langkah tidak boleh kosong. Masukkan minimal 1 kalimat.")
        else:
            new_steps.append(new_step)
            step_index += 1
    
    if new_steps:
        recipe['steps'] = new_steps  # Ganti semua langkah lama dengan yang baru

    new_time = input(f"Waktu ({recipe['time']} menit) klik 'enter' jika waktu memasaknya sama: ").strip()
    if new_time:
        recipe['time'] = new_time
    
    new_link = input(f"Link : ({recipe['link']}) klik 'enter' jika link video memasak sama: ").strip()
    if new_link:
        recipe['link'] = new_link
    
    print("\n✅ Resep berhasil diperbarui!")
    save_recipes_to_file(recipe)


def delete_recipe_interactive(recipe):
    confirm = input(f"Apakah Anda yakin ingin menghapus resep ini'? (y/n): ").lower()
    if confirm == 'y':
        recipes = load_recipes()
        recipes = [r for r in recipes if r != recipe]
        save_recipes(recipes)
        print(f"Resep telah dihapus.")
    elif confirm == 'n':
        print("Penghapusan dibatalkan.")
    else:
        print("Pilihan tidak valid")