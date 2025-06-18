import pygame
import heapq

# --- Pengaturan Tampilan ---
LEBAR = 600  # Lebar jendela, dibuat sama dengan tinggi agar grid persegi
LAYAR = pygame.display.set_mode((LEBAR, LEBAR))
pygame.display.set_caption("Visualisasi Algoritma Dijkstra pada Grid")

# --- Definisi Warna ---
MERAH = (255, 0, 0)      # Node sudah dikunjungi (Closed Set)
HIJAU = (0, 255, 0)      # Node sedang dipertimbangkan (Open Set)
PUTIH = (255, 255, 255)  # Node default (kosong)
HITAM = (0, 0, 0)        # Node rintangan (Dinding)
UNGU = (128, 0, 128)     # Node jalur terpendek (Path)
ORANYE = (255, 165, 0)   # Node awal (Start)
BIRU_LANGIT = (64, 224, 208) # Node akhir (End)
ABU_ABU = (128, 128, 128) # Garis grid

# ===============================================================
# LANGKAH 1: FONDASI - CLASS NODE DAN FUNGSI GRID
# ===============================================================

class Node:
    """Class untuk merepresentasikan satu kotak (node) pada grid."""
    def __init__(self, baris, kolom, lebar_kotak, total_baris):
        self.baris = baris
        self.kolom = kolom
        self.x = baris * lebar_kotak
        self.y = kolom * lebar_kotak
        self.warna = PUTIH
        self.tetangga = []
        self.lebar_kotak = lebar_kotak
        self.total_baris = total_baris

    def get_pos(self):
        return self.baris, self.kolom

    def is_closed(self):
        return self.warna == MERAH

    def is_open(self):
        return self.warna == HIJAU

    def is_wall(self):
        return self.warna == HITAM

    def is_start(self):
        return self.warna == ORANYE

    def is_end(self):
        return self.warna == BIRU_LANGIT

    def reset(self):
        self.warna = PUTIH

    def make_start(self):
        self.warna = ORANYE

    def make_closed(self):
        self.warna = MERAH

    def make_open(self):
        self.warna = HIJAU

    def make_wall(self):
        self.warna = HITAM

    def make_end(self):
        self.warna = BIRU_LANGIT

    def make_path(self):
        self.warna = UNGU

    def draw(self, layar):
        pygame.draw.rect(layar, self.warna, (self.x, self.y, self.lebar_kotak, self.lebar_kotak))

    def update_tetangga(self, grid):
        """Mencari tetangga yang valid (atas, bawah, kiri, kanan) dari node ini."""
        self.tetangga = []
        # Bawah
        if self.baris < self.total_baris - 1 and not grid[self.baris + 1][self.kolom].is_wall():
            self.tetangga.append(grid[self.baris + 1][self.kolom])
        # Atas
        if self.baris > 0 and not grid[self.baris - 1][self.kolom].is_wall():
            self.tetangga.append(grid[self.baris - 1][self.kolom])
        # Kanan
        if self.kolom < self.total_baris - 1 and not grid[self.baris][self.kolom + 1].is_wall():
            self.tetangga.append(grid[self.baris][self.kolom + 1])
        # Kiri
        if self.kolom > 0 and not grid[self.baris][self.kolom - 1].is_wall():
            self.tetangga.append(grid[self.baris][self.kolom - 1])

def buat_grid(baris, lebar):
    """Membuat struktur data grid (2D list) yang diisi dengan Node."""
    grid = []
    lebar_kotak = lebar // baris
    for i in range(baris):
        grid.append([])
        for j in range(baris):
            node = Node(i, j, lebar_kotak, baris)
            grid[i].append(node)
    return grid

def gambar_garis_grid(layar, baris, lebar):
    """Menggambar garis-garis untuk grid."""
    lebar_kotak = lebar // baris
    for i in range(baris):
        pygame.draw.line(layar, ABU_ABU, (0, i * lebar_kotak), (lebar, i * lebar_kotak))
        for j in range(baris):
            pygame.draw.line(layar, ABU_ABU, (j * lebar_kotak, 0), (j * lebar_kotak, lebar))

def gambar(layar, grid, baris, lebar):
    """Fungsi utama untuk menggambar semua elemen ke layar."""
    layar.fill(PUTIH)
    for row in grid:
        for node in row:
            node.draw(layar)
    gambar_garis_grid(layar, baris, lebar)
    pygame.display.update()

# ===============================================================
# LANGKAH 2: INTERAKTIVITAS - FUNGSI MENDAPATKAN POSISI KLIK
# ===============================================================

def dapatkan_posisi_klik(pos, baris, lebar):
    """Mengubah koordinat pixel mouse menjadi koordinat grid (baris, kolom)."""
    lebar_kotak = lebar // baris
    y, x = pos
    baris_klik = y // lebar_kotak
    kolom_klik = x // lebar_kotak
    return baris_klik, kolom_klik

# ===============================================================
# LANGKAH 3: OTAK PROGRAM - ALGORITMA DIJKSTRA
# ===============================================================

def gambar_jalur(path_sebelumnya, saat_ini, draw):
    """Menggambar jalur terpendek setelah algoritma selesai."""
    while saat_ini in path_sebelumnya:
        saat_ini = path_sebelumnya[saat_ini]
        saat_ini.make_path()
        draw()

def algoritma_dijkstra(draw, grid, start, end):
    """Implementasi algoritma Dijkstra untuk sistem grid."""
    count = 0
    antrian_prioritas = [(0, count, start)] # (jarak, count, node)
    path_sebelumnya = {}
    jarak = {node: float("inf") for row in grid for node in row}
    jarak[start] = 0

    while antrian_prioritas:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        jarak_saat_ini, _, node_saat_ini = heapq.heappop(antrian_prioritas)

        if node_saat_ini == end:
            gambar_jalur(path_sebelumnya, end, draw)
            end.make_end()
            start.make_start()
            return True # Jalur ditemukan

        for tetangga in node_saat_ini.tetangga:
            temp_jarak = jarak[node_saat_ini] + 1 # Jarak antar node di grid selalu 1

            if temp_jarak < jarak[tetangga]:
                path_sebelumnya[tetangga] = node_saat_ini
                jarak[tetangga] = temp_jarak
                count += 1
                heapq.heappush(antrian_prioritas, (jarak[tetangga], count, tetangga))
                tetangga.make_open()

        draw()

        if node_saat_ini != start:
            node_saat_ini.make_closed()

    return False # Jalur tidak ditemukan

# ===============================================================
# LANGKAH 4: SEMUANYA JADI SATU - FUNGSI MAIN
# ===============================================================

def main(layar, lebar):
    JUMLAH_BARIS = 30
    grid = buat_grid(JUMLAH_BARIS, lebar)

    start = None
    end = None

    berjalan = True
    mulai_algoritma = False

    while berjalan:
        gambar(layar, grid, JUMLAH_BARIS, lebar)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                berjalan = False

            # --- Input Mouse ---
            if pygame.mouse.get_pressed()[0]: # Klik Kiri
                pos = pygame.mouse.get_pos()
                baris, kolom = dapatkan_posisi_klik(pos, JUMLAH_BARIS, lebar)
                node = grid[baris][kolom]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_wall()

            elif pygame.mouse.get_pressed()[2]: # Klik Kanan
                pos = pygame.mouse.get_pos()
                baris, kolom = dapatkan_posisi_klik(pos, JUMLAH_BARIS, lebar)
                node = grid[baris][kolom]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            # --- Input Keyboard ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_tetangga(grid)
                    
                    algoritma_dijkstra(lambda: gambar(layar, grid, JUMLAH_BARIS, lebar), grid, start, end)

                if event.key == pygame.K_c: # Tombol 'c' untuk Clear
                    start = None
                    end = None
                    grid = buat_grid(JUMLAH_BARIS, lebar)

    pygame.quit()

# --- Menjalankan Program ---
if __name__ == "__main__":
    main(LAYAR, LEBAR)