from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_page_data(page_number):
    db_path = "/home/harry/Documents/pCloudSync/database/quran/alquran2.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to get verses for the given page
    cursor.execute("""
        SELECT d.kode, d.nomor_surat, d.nomor_ayat, d.nama_surat, d.tashkeel, q.nomorkata, q.ar, q.id
        FROM data d
        JOIN qkata q ON d.kode = q.kode
        WHERE d.hal = ?
        ORDER BY d.nomor_surat, d.nomor_ayat, q.nomorkata
    """, (page_number,))

    rows = cursor.fetchall()
    conn.close()

    # Group words by verse
    verses = {}
    for row in rows:
        verse_key = (row['nomor_surat'], row['nomor_ayat'])
        if verse_key not in verses:
            verses[verse_key] = {
                'nama_surat': row['nama_surat'],
                'tashkeel': row['tashkeel'],
                'words': []
            }
        verses[verse_key]['words'].append({'ar': row['ar'], 'id': row['id']})

    return verses

@app.route('/page/<int:page_number>')
def show_page(page_number):
    verses = get_page_data(page_number)
    return render_template('page.html', page_number=page_number, verses=verses)

if __name__ == '__main__':
    app.run(debug=True)
