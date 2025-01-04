import pandas as pd
from bottle import Bottle, run, template, redirect,request

# Membaca data terjemahan dari file JSON
data = pd.read_json('master_quran.json')

app = Bottle()

# Fungsi untuk mendapatkan halaman awal dari Juz
def get_first_page_of_juz(juz):
    # Filter data untuk mendapatkan halaman yang sesuai dengan Juz
    juz_data = data[data['juz'] == juz]  # Asumsi kolom 'juz' ada dalam data
    if juz_data.empty:
        return None
    # Urutkan berdasarkan halaman dan ambil halaman terkecil
    first_page = juz_data['hal'].min()
    return first_page

# Fungsi untuk mendapatkan terjemahan berdasarkan halaman
def get_translation(page):
    # Filter data berdasarkan kolom 'hal' (halaman)
    translation_data = data[data['hal'] == page][['id', 'kode']].values.tolist()

    # Menghitung nomor surat dan ayat dari kode (konversi kode ke integer terlebih dahulu)
    translations = []
    for id_text, kode_str in translation_data:
        kode = int(kode_str)  # Konversi kode dari string ke integer
        surat = kode // 1000  # Nomor surat
        ayat = kode % 1000    # Nomor ayat
        translations.append((surat, ayat, id_text))

    return translations


@app.route('/')
def index():
    # Daftar Juz dari 1 hingga 30
    juz_list = list(range(1, 31))
    return template('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pilih Juz</title>
        </head>
        <body>
            <h1>Pilih Juz Al-Qur'an</h1>
            <form action="/juz" method="get">
                <select name="juz">
                    % for juz in juz_list:
                        <option value="{{juz}}">Juz {{juz}}</option>
                    % end
                </select>
                <button type="submit">Tampilkan Terjemah</button>
            </form>
        </body>
        </html>
    ''', juz_list=juz_list)

@app.route('/juz')
def show_juz():
    juz = int(request.query.juz)  # Ambil Juz dari query parameter
    first_page = get_first_page_of_juz(juz)

    if first_page is None:
        return "Juz tidak ditemukan."

    # Arahkan ke halaman pertama dari Juz yang dipilih
    return redirect(f'/terjemah/{first_page}')  # Mengarahkan ke halaman terjemah pertama


@app.route('/<mode>/<page:int>')
def show_quran_page(mode, page):
    # Validasi halaman Al-Quran
    if page < 1 or page > 604:
        return "Halaman tidak valid. Halaman Al-Quran antara 1 hingga 604."

    # URL gambar Mushaf sesuai halaman
    image_url = f"https://media.qurankemenag.net/khat2/QK_{page:03d}.webp"

    # Mendapatkan terjemahan jika mode adalah 'terjemah'
    translation = get_translation(page) if mode == 'terjemah' else None

    # Template HTML untuk menampilkan mushaf dan terjemahan secara berdampingan (gambar di kanan dan terjemahan di kiri)
    return template('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Halaman Al-Qur'an {{page}} - {{mode}}</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                padding: 20px;
                font-family: Arial, sans-serif;
            }
            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 80%;
                max-height: 100vh;
            }
            .navigation {
                display: flex;
                justify-content: space-between;
                align-items: center; /* Align center vertically */
                width: 100%;
                margin-bottom: 10px;
            }
            .content {
                display: flex;
                width: 100%;
                height: 80vh;
                justify-content: space-between;
                align-items: flex-start;
            }
            .translation {
                width: 48%;
                height: 100%;
                overflow-y: scroll;
                text-align: justify;
                font-size: 18px;
                line-height: 1.6;
                padding-right: 10px;
            }
            .ayah {
                margin-bottom: 20px;
            }
            .ayah-header {
                font-weight: bold;
                margin-bottom: 5px;
            }
            .quran-image-container {
                display: flex;
                justify-content: flex-start; /* Left align */
                width: 48%; /* 48% of the total width for image container */
                height: 100%; /* Full height */
                overflow-y: scroll; /* Enable vertical scrolling */
                overflow-x: scroll; /* Enable horizontal scrolling to prevent cut-off */
                position: relative;
            }

            .quran-image {
                width: 150%; /* Increase the width to 150% of the container */
                height: auto; /* Automatically adjust the height */
                object-fit: contain; /* Ensure the image scales correctly */
            }

            .button {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
                border-radius: 5px;
            }
            .button:hover {
                background-color: #45a049;
            }

            .juz-form select {
                padding: 5px;
                font-size: 16px;
            }
            .juz-form button {
                padding: 5px 10px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Navigation buttons at the top -->
            <div class="navigation">
                <a href="/{{mode}}/{{next_page}}" class="button">← Berikutnya</a>

                <!-- Form Pemilihan Juz di tengah -->
                <form action="/juz" method="get" class="juz-form">
                    <select name="juz">
                        % for i in range(1, 31):
                            <option value="{{i}}">Juz {{i}}</option>
                        % end
                    </select>
                    <button type="submit">Pilih Juz</button>
                </form>

                <a href="/{{mode}}/{{prev_page}}" class="button">Sebelumnya →</a>
            </div>

            <div class="content">
                <!-- Terjemahan di sisi kiri dengan scroll -->
                % if mode == 'terjemah':
                    <div class="translation">
                        <h2>Terjemahan Halaman {{page}}</h2>
                        % for surat, ayat, id_text in translation:
                            <div class="ayah">
                                <p><b>{{ayat}}</b>. {{id_text}}</p>
                            </div>
                        % end
                    </div>
                % end

                <!-- Gambar Mushaf di sisi kanan -->
                <div class="quran-image-container">
                    <img src="{{image_url}}" alt="Qur'an page {{page}}" class="quran-image">
                </div>
            </div>

            <!-- Navigation buttons at the bottom -->
            <div class="navigation">
                <a href="/{{mode}}/{{next_page}}" class="button">← Berikutnya</a>

                <!-- Form Pemilihan Juz di tengah -->
                <form action="/juz" method="get" class="juz-form">
                    <select name="juz">
                        % for i in range(1, 31):
                            <option value="{{i}}">Juz {{i}}</option>
                        % end
                    </select>
                    <button type="submit">Pilih Juz</button>
                </form>

                <a href="/{{mode}}/{{prev_page}}" class="button">Sebelumnya →</a>
            </div>
        </div>
    </body>
    </html>
''', mode=mode, page=page, image_url=image_url, translation=translation,
   prev_page=page-1 if page > 1 else 1, next_page=page+1 if page < 604 else 604)

    # Ganti dengan ini:
application = app
