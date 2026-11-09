# Sistem Manajemen Data Pasien Penyakit Mata

Tugas kelompok **Pemrograman Berorientasi Objek** — **Kelompok 3**. Program Python yang menerapkan **Class & Object**, **Enkapsulasi**, dan **Inheritance** (ditambah komposisi dan polimorfisme) untuk mengelola data nyata pasien poli mata dari dataset **ODIR-5K (Ocular Disease Intelligent Recognition)**.

Ringkasnya:

- Data asli: 6.392 baris (1 baris = 1 foto fundus) → 3.358 pasien, 7 kelompok penyakit mata + normal.
- Kode: 10 file di folder `program/` (9 file class, satu class satu file, + `main.py`).
- Hanya library bawaan Python (`csv`, `os`). Tidak perlu `pip install` apa pun.
- Pengujian: 34 dari 34 skenario berhasil (setter, CSV rusak, file hilang, semua menu).
- Semua angka dan output di presentasi, naskah, dan laporan berasal dari program yang benar-benar dijalankan, bukan karangan.

## 1. Struktur folder

```text
Tugas Kelompok/
├── README.md                ← catatan ini
├── PROMPT.md                ← prompt final project (versi penyakit mata)
├── program/                 ← KODE PROGRAM (jalankan dari sini)
│   ├── main.py                  Program utama: membaca CSV, demo validasi, menu interaktif
│   ├── orang.py                 class Orang: umur, jenis_kelamin
│   ├── pasien.py                class Pasien(Orang): id_pasien
│   ├── pasien_mata.py           class PasienMata(Pasien): mata kiri/kanan, kode diagnosis, daftar penyakit
│   ├── pemeriksaan_mata.py      class PemeriksaanMata: hasil foto satu mata
│   ├── penyakit_mata.py         class PenyakitMata: satu jenis penyakit mata
│   ├── retinopati_diabetik.py   class RetinopatiDiabetik(PenyakitMata)
│   ├── degenerasi_makula.py     class DegenerasiMakula(PenyakitMata)
│   ├── glaukoma.py              class Glaukoma(PenyakitMata)
│   ├── kelainan_lain.py         class KelainanLain(PenyakitMata)
│   └── data/full_df.csv         data asli ODIR-5K (6.392 baris)
├── ppt/
│   ├── Presentasi Kelompok 3 - Sistem Manajemen Data Pasien Penyakit Mata.html   ← presentasi utama (41 slide)
│   └── Presentasi Kelompok 3 - Sistem Manajemen Data Pasien Penyakit Mata.pdf    ← versi PDF (cadangan / cetak)
├── naskah/
│   ├── Naskah Presentasi Kelompok 3.docx
│   └── Naskah Presentasi Kelompok 3.pdf
├── penjelasan/
│   └── Penjelasan Project & Pembagian Materi Kelompok 3.pdf
├── laporan/
│   ├── Laporan Project PBO Kelompok 3 - Sistem Manajemen Data Pasien Penyakit Mata.docx
│   └── Laporan Project PBO Kelompok 3 - Sistem Manajemen Data Pasien Penyakit Mata.pdf
└── arsip/
    └── versi-1-rs-umum/     ← versi lama (data rumah sakit umum), tidak dipakai lagi
```

## 2. Cara menjalankan program

1. Pastikan Python 3 sudah terpasang (minimal 3.6; sudah diuji dengan Python 3.14). Cek dengan `python --version`.
2. Buka terminal (PowerShell/CMD) di folder `Tugas Kelompok`, lalu jalankan:

```powershell
cd program
python main.py
```

3. Program memuat data, menampilkan demo validasi, lalu menu. Ketik angka 1–6 dan tekan Enter.

| Pilihan | Fungsi | Contoh yang bisa dicoba |
|---|---|---|
| 1 | Lihat 10 data pertama | - |
| 2 | Cari pasien berdasarkan ID | `188` (3 kelompok penyakit), `12` (tidak ada), `abc` |
| 3 | Cari pasien berdasarkan penyakit | `2` = glaukoma (206 pasien) |
| 4 | Tambah pasien baru | umur `63`, `Female`, kiri `cataract`, kanan `moderate non proliferative retinopathy` |
| 5 | Tampilkan ringkasan | jumlah, rata-rata umur, tabel per penyakit |
| 6 | Keluar | - |

Pasien baru hanya tersimpan selama program berjalan; file CSV asli tidak pernah diubah. Jika muncul `File CSV tidak ditemukan!`, pastikan `full_df.csv` ada di `program/data/`. Setelah program dijalankan, Python bisa membuat folder `program/__pycache__`; itu file cache otomatis dan boleh dihapus.

Contoh awal output asli (tanpa diubah):

```text
================================================================
SISTEM MANAJEMEN DATA PASIEN PENYAKIT MATA
================================================================
File data          : full_df.csv
Pasien dimuat      : 3358 object PasienMata
Baris digabung     : 3034 (foto mata kedua dari pasien yang sama)
Baris dilewati     : 0
```

## 3. Isi folder `program/` (file per file)

| File | Class | Mewarisi | Isi penting | Konsep OOP |
|---|---|---|---|---|
| `orang.py` | `Orang` | - | atribut `umur` (1–120) dan `jenis_kelamin` (Male/Female), method `tampilkan_info()` | Class & Object, Enkapsulasi |
| `pasien.py` | `Pasien` | `Orang` | atribut `id_pasien` (≥ 0), `super().__init__()`, override `tampilkan_info()` | Inheritance, Enkapsulasi |
| `pasien_mata.py` | `PasienMata` | `Pasien` | `mata_kiri`, `mata_kanan` (object PemeriksaanMata), `kode_diagnosis`, `daftar_penyakit` (validasi silang), method private `__cek_pemeriksaan()`, `apakah_normal()`, `jumlah_penyakit()`, `nama_penyakit()`, override `tampilkan_info()` | Inheritance bertingkat, Enkapsulasi, Komposisi, Polimorfisme |
| `pemeriksaan_mata.py` | `PemeriksaanMata` | - | `sisi`, `nama_foto`, `diagnosis` satu mata; `daftar_kata_kunci()` (menangani koma lebar ，), `catatan_foto()` | Komposisi, Enkapsulasi |
| `penyakit_mata.py` | `PenyakitMata` | - | `kode`, `nama`, `bagian_mata`, `kata_kunci`; `ditemukan_di()`, `mata_terdampak()`, `tampilkan_info()` | Class induk penyakit, Enkapsulasi |
| `retinopati_diabetik.py` | `RetinopatiDiabetik` | `PenyakitMata` | `tingkat_keparahan()` (ringan, sedang, berat, proliferatif) | Inheritance, Overriding |
| `degenerasi_makula.py` | `DegenerasiMakula` | `PenyakitMata` | `jenis()` (kering/basah) | Inheritance, Overriding |
| `glaukoma.py` | `Glaukoma` | `PenyakitMata` | `status()` (pasti/dugaan) | Inheritance, Overriding |
| `kelainan_lain.py` | `KelainanLain` | `PenyakitMata` | `daftar_kelainan()`, override `ditemukan_di()` | Inheritance, Polimorfisme |
| `main.py` | - | - | membaca CSV (`muat_data()`), membuat object (`buat_pasien()`), demo validasi, menu 6 pilihan (`jalankan_menu()`) | Class & Object (pembuatan object), try-except |

Hubungan antar class:

```text
Orang ──▷ Pasien ──▷ PasienMata      (inheritance bertingkat, “adalah”)
                          │
                          ├── memiliki 2 PemeriksaanMata  (komposisi: mata kiri & kanan)
                          └── memakai 0..7 PenyakitMata    (daftar_penyakit)

PenyakitMata ──▷ RetinopatiDiabetik | DegenerasiMakula | Glaukoma | KelainanLain
(Katarak, Retinopati hipertensi, Miopia patologis = object langsung dari PenyakitMata)
```

Alur `main.py`: cari file CSV → buat 7 object jenis penyakit → `muat_data()` membaca setiap baris (baris kedua pasien yang sama digabung, baris tidak valid dilewati dan dicatat nomornya) → tampilkan hasil pemuatan → `demo_validasi()` → `jalankan_menu()`.

## 4. Letak konsep OOP di kode (untuk presentasi)

Nomor baris di bawah ini sama persis dengan file di `program/`.

**Class & Object**

- `orang.py` baris 6: class induk paling atas (umur, jenis kelamin)
- `pasien.py` baris 8: class Pasien (id_pasien)
- `pasien_mata.py` baris 12: class pasien poli mata
- `pemeriksaan_mata.py` baris 8: class hasil foto satu mata
- `penyakit_mata.py` baris 9: class satu jenis penyakit mata
- `main.py` baris 54: membuat 7 object jenis penyakit
- `main.py` baris 93: satu baris CSV → object PemeriksaanMata & PasienMata
- `main.py` baris 132: object disimpan di list

**Enkapsulasi**

- `orang.py` baris 23: setter umur: bilangan bulat 1–120
- `orang.py` baris 34: setter jenis kelamin: Male/Female
- `pasien.py` baris 22: setter ID: bilangan bulat ≥ 0
- `pemeriksaan_mata.py` baris 40: setter nama foto: akhiran sesuai sisi
- `pasien_mata.py` baris 45: method private: object mata harus sesuai ID
- `pasien_mata.py` baris 58: setter kode diagnosis: N D G C A H M O
- `pasien_mata.py` baris 75: validasi silang penanda vs kata kunci
- `main.py` baris 141: contoh data tidak valid dalam try-except

**Inheritance**

- `pasien.py` baris 13: constructor chaining Pasien → Orang
- `pasien.py` baris 30: override tampilkan_info() milik Orang
- `pasien_mata.py` baris 20: chaining PasienMata → Pasien
- `pasien_mata.py` baris 110: override tampilkan_info() milik Pasien
- `retinopati_diabetik.py` baris 9: turunan PenyakitMata (kode D)
- `degenerasi_makula.py` baris 8: turunan PenyakitMata (kode A)
- `glaukoma.py` baris 8: turunan PenyakitMata (kode G)
- `kelainan_lain.py` baris 48: override ditemukan_di() (polimorfisme)
- `pasien_mata.py` baris 121: polimorfisme: versi method mengikuti class

## 5. Data: `program/data/full_df.csv`

- Sumber: ODIR-5K (Ocular Disease Intelligent Recognition), diunduh dari Kaggle: <https://www.kaggle.com/datasets/andrewmvd/ocular-disease-recognition-odir5k>. Data dikumpulkan Shanggong Medical Technology dari beberapa rumah sakit di Tiongkok untuk kompetisi ODIR-2019 Peking University. Lisensi di Kaggle tertulis “not specified”, jadi pakai untuk keperluan belajar dan sebutkan sumbernya.
- Kolom yang dipakai (15): `ID`, `Patient Age`, `Patient Sex`, `Left-Fundus`, `Right-Fundus`, `Left-Diagnostic Keywords`, `Right-Diagnostic Keywords`, dan penanda `N D G C A H M O`.
- Arti penanda: **N** normal, **D** retinopati diabetik, **G** glaukoma, **C** katarak, **A** degenerasi makula, **H** retinopati hipertensi, **M** miopia patologis, **O** kelainan lain.
- Kolom yang tidak dipakai: `filepath`, `labels`, `target`, `filename` (label per foto buatan pengunggah Kaggle, turunan dari kolom lain).

| Kode | Penyakit | Pasien | Rata-rata umur | Kena kedua mata |
|---|---|---|---|---|
| D | Retinopati diabetik | 1.105 | 56,4 | 659 |
| G | Glaukoma | 206 | 62,6 | 110 |
| C | Katarak | 208 | 66,4 | 99 |
| A | Degenerasi makula | 163 | 60,9 | 116 |
| H | Retinopati hipertensi | 103 | 56,2 | 90 |
| M | Miopia patologis | 171 | 57,0 | 91 |
| O | Kelainan lain | 905 | 59,1 | 173 |

Catatan jujur tentang data (sudah dicek dengan program):

- 1.080 pasien normal; 556 pasien punya lebih dari satu kelompok penyakit (jika kelainan lain tidak dihitung: 182 pasien).
- 15 pasien tercatat berumur 1 tahun (kemungkinan salah catat di sumber). Data tidak diubah.
- 567 pasien memakai koma lebar (，) sebagai pemisah diagnosis; program menanganinya.
- Deteksi penyakit dari kata kunci cocok 100% dengan penanda dokter untuk 3.358 pasien.
- Data hanya memuat penyakit yang terlihat di foto fundus. Program ini mengelola data diagnosis dokter, bukan alat diagnosis.

## 6. Presentasi (`ppt/`)

- Buka `Presentasi Kelompok 3 - Sistem Manajemen Data Pasien Penyakit Mata.html` dengan Chrome atau Edge (klik dua kali). Tekan **F11** untuk layar penuh.
- Navigasi: **→ / Spasi / PageDown** maju, **← / PageUp** mundur, **Home/End** awal/akhir, roda mouse atau geser layar sentuh juga bisa.
- **N** = buka/tutup naskah pembicara slide yang sedang tampil (untuk latihan).
- **E** = mode edit: klik teks untuk mengubah; tersimpan otomatis di browser. **Ctrl+S** mengunduh salinan HTML yang sudah diedit. Tombol “Kembalikan teks asli” menghapus perubahan.
- Di slide 2, klik nama anggota untuk melompat ke bagiannya (berguna saat tanya jawab).
- Font sudah ditanam di dalam file, jadi tampilan tetap sama walau tanpa internet. File PDF di folder yang sama adalah cadangan jika laptop tidak bisa membuka HTML.
- Gaya visual: tabel periksa mata (Snellen) — krem, tinta hitam, oranye fundus. Warna bisa diubah di bagian `:root` pada file HTML.

## 7. Pembagian materi 9 anggota

| No | Nama | Bagian | Slide | Durasi |
|---|---|---|---|---|
| 1 | Riswan | Latar Belakang & Struktur Project | 1–5 | ± 3,5 menit |
| 2 | Yus Aidil | Dataset ODIR-5K & Pemetaan Kolom | 6–9 | ± 3,5 menit |
| 3 | Fahmi | Class & Object | 10–13 | ± 3,5 menit |
| 4 | Diva Nurislamia Agfa | Enkapsulasi | 14–18 | ± 4 menit |
| 5 | Rosa Ramadani | Inheritance: Pewarisan Bertingkat | 19–22 | ± 3 menit |
| 6 | Sofiang | Komposisi: Pemeriksaan Mata | 23–26 | ± 3 menit |
| 7 | Revalinda | Hierarki Class Penyakit & Polimorfisme | 27–30 | ± 3,5 menit |
| 8 | Andi Rezky Nabila | Program Utama: Membaca CSV & Menu | 31–34 | ± 4 menit |
| 9 | Alfira Yunita Syam | Hasil Program, Demo Menu & Kesimpulan | 35–41 | ± 5 menit |

Total ± 33 menit (41 slide). Naskah lisan lengkap + penjelasan kode per baris ada di `naskah/`, materi per anggota + tanya jawab ada di `penjelasan/`.

## 8. Dokumen

- `naskah/`: naskah lisan per slide (sama dengan catatan pembicara di presentasi), tabel fungsi setiap baris kode yang tampil, kalimat estafet, dan persiapan tanya jawab.
- `penjelasan/`: gambaran project (struktur, data, diagram class, flowchart, letak konsep OOP) lalu materi setiap anggota lengkap dengan kode, output, dan tanya jawab.
- `laporan/`: laporan format umum (sampul, kata pengantar, daftar isi/tabel/gambar, BAB I–IV, daftar pustaka, lampiran kode & output). Bagian berwarna **kuning** wajib diisi sendiri: NIM, nama dosen, program studi, fakultas, universitas, dan kota. Setelah mengedit, klik kanan daftar isi → *Update Field* (atau tekan Ctrl+A lalu F9).

## 9. Arsip

`arsip/versi-1-rs-umum/` berisi versi pertama (data `hospital data analysis.csv`, class Orang → Pasien → PasienRawatUlang + RekamMedis) beserta PPT, naskah, dan laporannya. Disimpan hanya sebagai riwayat; tidak dipakai di versi penyakit mata.
