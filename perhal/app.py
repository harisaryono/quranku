from flask import Flask, render_template,redirect, url_for, request
import json

app = Flask(__name__,static_folder='static')

JSON_FILE = 'quran_data.json'

def load_quran_data():
    with open(JSON_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_quran_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def convert_page_to_juz(page_number):
    # Menentukan rentang halaman per juz
    juz_ranges = {
        1: (1, 21),
        2: (22, 41),
        3: (42, 61),
        4: (62, 81),
        5: (82, 101),
        6: (102, 121),
        7: (122, 141),
        8: (142, 161),
        9: (162, 181),
        10: (182, 201),
        11: (202, 221),
        12: (222, 241),
        13: (242, 261),
        14: (262, 281),
        15: (282, 301),
        16: (302, 321),
        17: (322, 341),
        18: (342, 361),
        19: (362, 381),
        20: (382, 401),
        21: (402, 421),
        22: (422, 441),
        23: (442, 461),
        24: (462, 481),
        25: (482, 501),
        26: (502, 521),
        27: (522, 541),
        28: (542, 561),
        29: (562, 581),
        30: (582, 604)
    }

    # Menentukan juz berdasarkan halaman
    for juz, (start_page, end_page) in juz_ranges.items():
        if start_page <= page_number <= end_page:
            # Menentukan nomor dalam juz
            nomor_dalam_juz = page_number - start_page + 1
            return juz, nomor_dalam_juz

    return "Halaman tidak valid"

def get_page_data(page_number):
    # Baca data dari file JSON
    json_file_path = 'quran_data.json'
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Ambil data untuk halaman tertentu
    page_data = data.get(str(page_number), {})  # Mengambil data halaman dengan kunci string (page_number)
    
    verses = {}

    # Mengorganisir data berdasarkan ayat
    for verse_key, verse_data in page_data.items():
        surah_number, ayah_number = verse_key.split('_')  # Pisahkan nomor surah dan ayah dari kunci
        surah_number = int(surah_number)
        ayah_number = int(ayah_number)
        
        verses[(surah_number, ayah_number)] = {
            'nama_surat': verse_data['nama_surat'],
            'tashkeel': verse_data['tashkeel'],
            'juz': verse_data['juz'],
            'words': verse_data['words']
        }

    return verses

@app.route('/page/<int:page_number>')
def show_page(page_number):
    verses = get_page_data(page_number)
    # Ambil `nama_surat` dari ayat pertama jika ada data
    nama_surat = next(iter(verses.values()))['nama_surat'] if verses else None

    juz,nomor=convert_page_to_juz(page_number)

    return render_template('page.html', page_number=page_number, verses=verses,juz=juz,nomor=nomor,nama_surat1=nama_surat)

# Fungsi rentang Juz ke halaman
def get_start_page_for_juz(juz):
    juz_ranges = {
        1: (1, 21), 2: (22, 41), 3: (42, 61), 4: (62, 81), 5: (82, 101),
        6: (102, 121), 7: (122, 141), 8: (142, 161), 9: (162, 181), 10: (182, 201),
        11: (202, 221), 12: (222, 241), 13: (242, 261), 14: (262, 281), 15: (282, 301),
        16: (302, 321), 17: (322, 341), 18: (342, 361), 19: (362, 381), 20: (382, 401),
        21: (402, 421), 22: (422, 441), 23: (442, 461), 24: (462, 481), 25: (482, 501),
        26: (502, 521), 27: (522, 541), 28: (542, 561), 29: (562, 581), 30: (582, 604)
    }

    if juz in juz_ranges:
        return juz_ranges[juz][0]  # Halaman awal Juz
    return None

# Endpoint untuk Juz tertentu
@app.route('/juz/<int:juz>')
def redirect_to_juz(juz):
    start_page = get_start_page_for_juz(juz)
    if start_page:
        return redirect(url_for('show_page', page_number=start_page))
    else:
        return f"Juz {juz} tidak valid", 404

#untuk mencari halaman awal bila diminta juz
@app.route('/api/juz/<int:juz>')
def get_juz_start_page(juz):
    start_page = get_start_page_for_juz(juz)
    if start_page:
        return {"start_page": start_page}, 200
    else:
        return {"error": "Invalid Juz number"}, 404    

# Endpoint untuk Surat dan Ayat dengan default ayat = 1
@app.route('/surah/<int:surah>/', defaults={'ayah': 1})
@app.route('/surah/<int:surah>/ayah/<int:ayah>')
def redirect_to_verse(surah, ayah):
    # Menentukan halaman berdasarkan surat dan ayat
    page_number = get_page_number_for_verse(surah, ayah)
    if page_number:
        return redirect(url_for('show_page', page_number=page_number))
    else:
        return f"Surah {surah} dan Ayah {ayah} tidak ditemukan", 404

# Fungsi untuk mencari halaman berdasarkan surah dan ayah
def get_page_number_for_verse(surah, ayah):
    # Baca data dari file JSON
    json_file_path = 'quran_data.json'
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Cari surat dan ayat
    for page_number, page_data in data.items():
        for verse_key, verse_data in page_data.items():
            verse_surah, verse_ayah = map(int, verse_key.split('_'))
            if verse_surah == surah and verse_ayah == ayah:
                return int(page_number)
    return None

#editing data
@app.route('/edit/<int:hal>/<surat_ayat>/<int:word_code>', methods=['GET', 'POST'])
def edit_word(hal,surat_ayat, word_code):
    data = load_quran_data()
    word_to_edit = None
    halaman = hal
    ayat = surat_ayat.split("_")[1]  # Mengambil bagian setelah "_"

    # Cari pasangan surat_ayat
    for page in data.values():
        if surat_ayat in page:
            # Cari kata berdasarkan kode
            for word in page[surat_ayat]['words']:
                if word['kode'] == word_code:
                    word_to_edit = word
                    break
            

    if not word_to_edit:
        return "Kata tidak ditemukan!", 404

    if request.method == 'POST':
        # Update data berdasarkan input pengguna
        word_to_edit['ar'] = request.form['ar']
        word_to_edit['id'] = request.form['id']
        word_to_edit['en'] = request.form['en']
        save_quran_data(data)
        #print(halaman)
        return redirect(f'/page/{halaman}#{ayat}')  # Redirect ke halaman asal

    return render_template('edit_word.html', word=word_to_edit, surat_ayat=surat_ayat,  halaman=halaman,ayat=ayat)


if __name__ == '__main__':
    app.run(debug=True)

