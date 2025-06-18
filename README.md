# 📍 Pencari Rute Kampus UIN Saizu

> Sebuah skrip Python untuk mencari dan memvisualisasikan rute terpendek antara dua lokasi kampus UIN Saizu menggunakan data dari OpenStreetMap.

Proyek ini adalah implementasi dari algoritma pathfinding (seperti Dijkstra) pada data geografis dunia nyata untuk menyelesaikan masalah pencarian rute antar dua titik yang berada di kabupaten yang berbeda (Banyumas dan Purbalingga).

## 📸 Tampilan Hasil

Berikut adalah contoh hasil akhir rute yang divisualisasikan dalam sebuah peta interaktif.

![image](https://github.com/user-attachments/assets/f53b90ab-e5d7-4ffc-829e-979426f9a215)



## ✨ Fitur Utama

- **Pencarian Rute Dinamis**: Menemukan rute jalan terpendek berdasarkan jarak fisik.
- **Data Geografis Dunia Nyata**: Menggunakan data jalan dari OpenStreetMap (OSM) yang selalu ter-update oleh komunitas.
- **Penanganan Lintas Wilayah**: Mampu mengunduh dan menggabungkan data peta dari dua kabupaten yang berbeda (Banyumas dan Purbalingga) untuk memastikan rute dapat ditemukan.
- **Visualisasi Interaktif**: Menghasilkan file HTML dengan peta interaktif dari Folium, lengkap dengan penanda lokasi dan garis rute yang jelas.
- **Input Presisi**: Menggunakan koordinat Lintang dan Bujur untuk akurasi lokasi yang maksimal.

## 🛠️ Teknologi yang Digunakan

- **Python 3**
- **OSMnx**: Untuk mengunduh dan memodelkan data jalan dari OpenStreetMap.
- **NetworkX**: Untuk merepresentasikan data sebagai graf dan menjalankan algoritma pencarian rute terpendek.
- **Folium**: Untuk membuat visualisasi peta interaktif.

## 🚀 Cara Menjalankan

Untuk menjalankan proyek ini di komputer lokal Anda, ikuti langkah-langkah berikut:

1.  **Clone Repository**
    ```bash
    git clone https://github.com/Nvianafn/algoritma-djikstra.git
    cd algoritma-djikstra
    ```

2.  **Buat Virtual Environment (Sangat Direkomendasikan)**
    ```bash
    # Untuk Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Untuk macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Semua Library yang Dibutuhkan**
    Pastikan Anda sudah memiliki file `requirements.txt` di repository Anda.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Skrip Python**
    ```bash
    python rute_osm.py 
    ```
    *(Pastikan nama file skrip Anda sesuai)*

5.  **Lihat Hasilnya**
    Setelah program selesai berjalan, akan ada file baru bernama `rute_kampus_uin_saizu_presisi.html`. Buka file tersebut di web browser favorit Anda untuk melihat peta rute interaktif.

## 📝 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk detailnya.

## ✍️ Author

- **apan** -
