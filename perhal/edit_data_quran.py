import json

def add_word_codes(json_file_path):
    # Baca file JSON
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    # Iterasi setiap halaman
    for page, page_content in data.items():
        # Iterasi setiap ayat
        for verse_key, verse_data in page_content.items():
            # Iterasi setiap kata dalam ayat
            for index, word in enumerate(verse_data['words'], start=1):
                # Tambahkan kode urutan kata
                word['kode'] = index
    
    # Simpan kembali data ke file JSON
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("Kode urutan kata berhasil ditambahkan ke quran_data.json.")

json_file_path='quran_data.json'
add_word_codes(json_file_path)
