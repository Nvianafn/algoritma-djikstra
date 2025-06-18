import osmnx as ox
import networkx as nx
import folium

print("--- Aplikasi Pencari Rute Kampus UIN Saizu ---")
print("Menggunakan koordinat presisi dari Anda.")

try:
    # 1. Unduh data peta untuk KEDUA kabupaten lalu gabungkan
    places = ["Banyumas, Central Java, Indonesia", "Purbalingga, Central Java, Indonesia"]
    
    print(f"\n[1/4] Mengunduh data peta untuk {len(places)} kabupaten...")
    # Proses ini mungkin memakan waktu beberapa menit. Harap sabar.
    G = ox.graph_from_place(places, network_type='drive', retain_all=True)
    print("      -> Selesai. Peta gabungan berhasil dibuat.")

    # 2. Definisikan koordinat awal dan akhir secara manual
    # Formatnya adalah (Latitude, Longitude)
    titik_awal_coords = (-7.410320408090181, 109.231287179008)      # Koordinat Kampus 1 (BARU)
    titik_akhir_coords = (-7.388018015327295, 109.34781290790698)  # Koordinat Kampus 2 (BARU)

    print(f"\n[2/4] Mencari node peta terdekat dari koordinat yang diberikan...")
    # Langsung cari node terdekat dari koordinat yang sudah pasti
    # Perhatikan: X adalah Longitude (koordinat kedua), Y adalah Latitude (koordinat pertama)
    node_awal = ox.nearest_nodes(G, X=titik_awal_coords[1], Y=titik_awal_coords[0])
    node_akhir = ox.nearest_nodes(G, X=titik_akhir_coords[1], Y=titik_akhir_coords[0])
    print("      -> Selesai. Node peta terdekat ditemukan.")

    # 3. Hitung rute terpendek menggunakan Dijkstra (default di NetworkX)
    print("\n[3/4] Menghitung rute terpendek menggunakan algoritma Dijkstra...")
    rute = nx.shortest_path(G, node_awal, node_akhir, weight='length')
    total_jarak_meter = nx.shortest_path_length(G, node_awal, node_akhir, weight='length')
    total_jarak_km = total_jarak_meter / 1000
    print(f"      -> Selesai. Rute ditemukan dengan total jarak {total_jarak_km:.2f} km.")

    # 4. Buat visualisasi peta interaktif secara manual
    print("\n[4/4] Membuat visualisasi peta interaktif...")
    
    # Hitung center peta berdasarkan koordinat tengah
    center_lat = (titik_awal_coords[0] + titik_akhir_coords[0]) / 2
    center_lon = (titik_awal_coords[1] + titik_akhir_coords[1]) / 2
    
    # Buat peta dasar
    peta_rute = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Ambil koordinat untuk setiap node dalam rute
    rute_coords = []
    for node in rute:
        lat = G.nodes[node]['y']
        lon = G.nodes[node]['x']
        rute_coords.append([lat, lon])
    
    # Gambar garis rute
    folium.PolyLine(
        locations=rute_coords,
        color='blue',
        weight=5,
        opacity=0.8,
        popup=f"Rute terpendek: {total_jarak_km:.2f} km"
    ).add_to(peta_rute)
    
    # Tambahkan marker untuk titik awal
    folium.Marker(
        location=titik_awal_coords,
        popup=f"Kampus 1 UIN Saizu (Awal)<br>Koordinat: {titik_awal_coords}",
        icon=folium.Icon(color='green', icon='play')
    ).add_to(peta_rute)

    # Tambahkan marker untuk titik akhir
    folium.Marker(
        location=titik_akhir_coords,
        popup=f"Kampus 2 UIN Saizu (Tujuan)<br>Koordinat: {titik_akhir_coords}<br>Jarak: {total_jarak_km:.2f} km",
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(peta_rute)
    
    # Tambahkan informasi jarak di pojok peta
    legend_html = f'''
    <div style="position: fixed; 
                top: 10px; right: 10px; width: 200px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>Informasi Rute</b></p>
    <p>Total Jarak: <b>{total_jarak_km:.2f} km</b></p>
    <p>Algoritma: <b>Dijkstra</b></p>
    </div>
    '''
    peta_rute.get_root().html.add_child(folium.Element(legend_html))

    # Simpan peta
    nama_file = "rute_kampus_uin_saizu_presisi.html"
    peta_rute.save(nama_file)
    print(f"      -> Selesai. Peta berhasil disimpan sebagai '{nama_file}'.")
    
    print("\n--- SELESAI ---")
    print("Silakan buka file HTML tersebut di browser Anda untuk melihat hasilnya.")
    print(f"Total jarak antar kampus: {total_jarak_km:.2f} km")

except Exception as e:
    print(f"\nOops, terjadi kesalahan: {e}")
    print("Pastikan Anda terhubung ke internet dan semua library terinstall dengan benar.")
    print("\nUntuk install library yang diperlukan:")
    print("pip install osmnx networkx folium")