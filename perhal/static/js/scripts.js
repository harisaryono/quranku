// navigatePageByDirection.js
function navigatePageByDirection(direction) {
    let currentPage = parseInt(document.getElementById('page-input').value);
    if (direction === 'prev' && currentPage > 1) {
        currentPage--;
    } else if (direction === 'next' && currentPage < 604) {
        currentPage++;
    }
    document.getElementById('page-input').value = currentPage;
    window.location.href = '/page/' + currentPage;
}

// navigateToPage.js
function navigateToPage() {
    let page = parseInt(document.getElementById('page-input').value);
    if (page >= 1 && page <= 604) {
        window.location.href = '/page/' + page;
    } else {
        alert('Nomor halaman tidak valid!');
    }
}

// playAudio.js
function playAudio(surat, ayat) {
    var audio = document.getElementById('audio-' + surat + '-' + ayat);
    audio.play();
}

function PerpageAudio(page_number) {
    var audio = document.getElementById('Perpage-' + page_number);
    audio.play();
}

// navigateJuz.js
function navigatePage(page) {
    window.location.href = `/page/${page}`;
}

function navigateJuz(direction) {
    let currentJuz = parseInt(document.getElementById('juz-value').getAttribute('data-juz'));;
    let targetJuz = direction === 'prev' ? currentJuz - 1 : currentJuz + 1;
    if (targetJuz < 1 || targetJuz > 30) return;

    // Meminta data halaman awal untuk Juz dari endpoint JSON
    fetch(`/api/juz/${targetJuz}`)
        .then(response => response.json())
        .then(data => {
            if (data.start_page) {
                window.location.href = `/page/${data.start_page}`;
            } else {
                alert('Invalid Juz number');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Terjadi kesalahan saat mengambil data Juz.');
        });
}
