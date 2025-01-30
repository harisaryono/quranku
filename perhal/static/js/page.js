document.addEventListener("DOMContentLoaded", function () {
    let displayMode = document.getElementById("displayMode");
    let words = document.querySelectorAll(".quran-word");
    let container = document.querySelector(".container")
    // 1. Ambil mode tampilan dari localStorage
    let savedMode = localStorage.getItem("displayMode");
    if (savedMode) {
        displayMode.value = savedMode;
    
    // 2. Pastikan tampilan sesuai dengan pilihan user
    toggleWordDisplay();
    toggleLanguageMode(); // 🔹 Tambahkan ini untuk memastikan RTL tetap aktif saat halaman dimua
    // 3. Simpan pilihan user di localStorage saat berubah
    displayMode.addEventListener("change", function () {
        localStorage.setItem("displayMode", displayMode.value);
        toggleWordDisplay();
        toggleLanguageMode(); // 🔹 Tambahkan ini agar perubahan mode langsung berpengaruh
    })
    // 4. Atur tooltip agar tetap dalam container
    words.forEach(word => {
        word.addEventListener("mouseenter", function () {
            let tooltip = word.querySelector(".tooltip");
            let container = document.querySelector(".container")
            if (tooltip && container) {
                // Gunakan setTimeout untuk menunggu rendering selesai
                setTimeout(() => {
                    let wordRect = word.getBoundingClientRect();
                    let containerRect = container.getBoundingClientRect();
                    let tooltipRect = tooltip.getBoundingClientRect()
                    // Reset posisi tooltip ke tengah elemen
                    tooltip.style.left = "50%";
                    tooltip.style.transform = "translateX(-50%)"
                    // Jika tooltip melebihi batas kiri container
                    if (tooltipRect.left < containerRect.left) {
                        tooltip.style.left = "0";
                        tooltip.style.transform = "translateX(0)";
                    
                    // Jika tooltip melebihi batas kanan container
                    if (tooltipRect.right > containerRect.right) {
                        tooltip.style.left = "100%";
                        tooltip.style.transform = "translateX(-100%)";
                    }
                }, 10); // 🔹 Memberikan sedikit jeda agar render selesai
            }
        });
    });
})
// Fungsi untuk mengubah tampilan teks & tooltip
function toggleWordDisplay() {
    let mode = document.getElementById("displayMode").value;
    let words = document.querySelectorAll(".quran-word")
    // Tambahkan atau hapus kelas 'ar-id-mode' pada body
    document.body.classList.toggle('ar-id-mode', mode === "ar-id")
    words.forEach(word => {
        let idText = word.getAttribute("data-id");
        let arText = word.getAttribute("data-ar");
        let tooltip = word.querySelector(".tooltip-text")
        if (mode === "id-ar") {
            word.querySelector(".word-text").textContent = idText; // ID sebagai teks utama
            tooltip.textContent = arText; // AR sebagai tooltip
            tooltip.classList.add('tooltip-ar');
            tooltip.classList.remove('tooltip-id');
        } else {
            word.querySelector(".word-text").textContent = arText; // AR sebagai teks utama
            tooltip.textContent = idText; // ID sebagai tooltip
            tooltip.classList.add('tooltip-id');
            tooltip.classList.remove('tooltip-ar');
        }
    });

// Fungsi untuk mode tampilan RTL/LTR
function toggleLanguageMode() {
    document.querySelectorAll('.ayat').forEach(ayat => {
        ayat.classList.toggle('rtl', document.getElementById("displayMode").value === "ar-id");
    });
