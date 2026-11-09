# Sistem Manajemen Data Pasien Rumah Sakit (OOP Python)

Program Python untuk mengelola **data nyata** pasien rumah sakit dari file
`hospital_data_analysis.csv` (984 baris, 10 kolom). Program ini menerapkan tiga
konsep OOP: **Class & Object**, **Enkapsulasi**, dan **Inheritance**.
Semuanya hanya memakai library bawaan Python (`csv` dan `os`).

Fitur program:
- Membaca CSV dan mengubah setiap baris menjadi object. Baris yang tidak valid **dilewati, nomor barisnya
  dicatat**, dan jumlahnya ditampilkan, sehingga satu baris rusak tidak menghentikan program.
- Menampilkan 5 rekam medis pertama, ringkasan data, dan demo validasi setter.
- **Menu interaktif**: lihat 10 data pertama, cari pasien berdasarkan Patient_ID, tambah pasien baru, keluar.

## Struktur File

```
Tugas Kelompok/
├── hospital data analysis.csv   # data asli (nama dengan underscore juga didukung)
├── orang.py                     # class Orang            (class induk)
├── pasien.py                    # class Pasien           (mewarisi Orang)
├── pasien_rawat_ulang.py        # class PasienRawatUlang (mewarisi Pasien, punya method khusus status_rawat)
├── rekam_medis.py               # class RekamMedis       (komposisi, berisi object Pasien)
├── main.py                      # program utama + menu interaktif
├── Laporan Project PBO Kelompok 3 - Sistem Manajemen Data Pasien.docx   # laporan format Word
├── Penjelasan Project Kelompok 3 - Pembagian Materi 9 Anggota.pdf       # bahan presentasi 9 anggota
├── Naskah Presentasi Kelompok 3.docx                                    # naskah lisan (versi Word)
├── naskah/
│   └── Naskah Presentasi Kelompok 3.pdf                                 # naskah lisan per slide untuk 9 anggota
├── ppt/
│   └── Presentasi Kelompok 3 - Sistem Manajemen Data Pasien.pptx        # slide presentasi (style Navy Klasik)
└── Pilihan Style PPT/                                                   # isi sama, style berbeda
    ├── Presentasi Kelompok 3 - Style Swiss Modern.pptx
    └── Presentasi Kelompok 3 - Style Medis Hijau.pptx
```

### Presentasi (PPT)

- 39 slide: judul, pembagian materi, dan 9 bagian (1 slide pembatas + 2–5 slide isi per anggota), kesimpulan,
  penutup, serta 2 slide cadangan **tersembunyi** (bank tanya jawab dan panduan latihan).
- Setiap slide punya **catatan pembicara** berisi naskah, target waktu, dan kalimat estafet. Buka dengan
  **Presenter View** (Alt+F5) agar catatan hanya terlihat oleh pembicara. Isinya sama persis dengan
  **Naskah Presentasi Kelompok 3**, yang juga memuat kata kunci dan persiapan tanya jawab per anggota
  (±2.800 kata, total ±29,5 menit tampil).
- Di slide yang menampilkan kode, naskah membahas kode **baris demi baris**, misalnya "Baris 6, `class Orang`,
  fungsinya membuat class baru bernama Orang." Dokumen naskah dan PDF penjelasan juga memuat tabel
  **Baris | Kode | Fungsinya** di bawah setiap potongan kode, dengan nomor baris yang sama persis dengan file `.py`.
- Semua output di slide, naskah, dan laporan diambil dari program yang **benar-benar dijalankan**, termasuk
  sesi demo menu.
- Kartu di slide *Pembagian Materi* bisa diklik untuk melompat ke bagian anggota, dan tombol **← Agenda** di setiap
  slide pembatas kembali ke daftar tersebut. Slide dikelompokkan dalam **section** per anggota.
- Style Swiss Modern memakai font Bahnschrift dan Medis Hijau memakai Segoe UI (ada di Windows 10/11). Jika
  presentasi dibuka di Mac, pakai style Navy Klasik (Calibri).

Pemetaan kolom CSV ke atribut (tidak ada atribut tambahan di luar kolom data):

| Kolom CSV      | Atribut / Class                  | Aturan validasi                  |
|----------------|----------------------------------|----------------------------------|
| Patient_ID     | `Pasien.patient_id`              | bilangan bulat positif           |
| Age            | `Orang.umur`                     | bilangan bulat positif           |
| Gender         | `Orang.jenis_kelamin`            | `Male` / `Female`                |
| Condition      | `RekamMedis.kondisi`             | tidak boleh kosong               |
| Procedure      | `RekamMedis.prosedur`            | tidak boleh kosong               |
| Cost           | `RekamMedis.biaya`               | bilangan positif                 |
| Length_of_Stay | `RekamMedis.lama_rawat`          | bilangan bulat lebih dari 0      |
| Readmission    | class `Pasien` / `PasienRawatUlang` | `Yes` / `No` (dicek di `main.py`) |
| Outcome        | `RekamMedis.hasil`               | `Recovered` / `Stable`           |
| Satisfaction   | `Pasien.kepuasan`                | bilangan bulat 1 sampai 5        |

Data tidak punya kolom nama pasien maupun data dokter/perawat, jadi class `Orang` hanya menyimpan umur dan jenis
kelamin, dan class `Dokter`/`Perawat` tidak dibuat.

## Cara Menjalankan

1. Pastikan Python 3 sudah terpasang (`python --version`).
2. Letakkan file CSV di folder yang sama dengan `main.py`.
3. Buka terminal di folder project, lalu jalankan:

```
python main.py
```

4. Setelah output awal tampil, ketik angka **1–4** pada menu lalu tekan Enter:
   - `1` lihat 10 data pertama
   - `2` cari pasien berdasarkan Patient_ID (contoh: `2`; ID `60` memang tidak ada di data)
   - `3` tambah pasien baru (Patient_ID dibuat otomatis = ID terbesar + 1; data diperiksa setter yang sama dengan data CSV)
   - `4` keluar

Tidak perlu `pip install` apa pun. Pasien yang ditambahkan hanya disimpan di list selama program berjalan;
file CSV asli tidak diubah.

## Format Output yang Diharapkan

Bagian dalam `<...>` diisi oleh program saat dijalankan. Angka sebenarnya dapat dilihat dengan menjalankan
`python main.py` sendiri.

```
============================================================
SISTEM MANAJEMEN DATA PASIEN RUMAH SAKIT
============================================================
[PERINGATAN] Baris <n> dilewati: <alasan>      <- hanya muncul jika ada baris tidak valid
File data         : <nama file CSV>
Object RekamMedis : <jumlah> object tersimpan di list
Baris dilewati    : <jumlah>
Nomor baris CSV   : [<n>, ...]                 <- hanya muncul jika ada baris yang dilewati

============================================================
5 REKAM MEDIS PERTAMA (dari <jumlah> data)
============================================================

[<nomor>] Object pasien dari class: <Pasien | PasienRawatUlang>
--- Data Pasien ---
ID Pasien      : <Patient_ID>
Umur           : <Age> tahun
Jenis Kelamin  : <Gender>
Kepuasan       : <Satisfaction>/5
Status Rawat   : Pasien rawat ulang            <- hanya untuk object PasienRawatUlang
--- Data Medis ---
Kondisi        : <Condition>
Prosedur       : <Procedure>
Biaya          : <Cost, 2 desimal>
Lama Rawat     : <Length_of_Stay> hari
Biaya per Hari : <Cost / Length_of_Stay>
Hasil          : <Outcome>
(... diulang sampai 5 rekam medis ...)

============================================================
RINGKASAN DATA
============================================================
Total pasien              : <jumlah>
Jumlah pasien rawat ulang : <jumlah> (<persen>%)
Rata-rata biaya           : <angka>
Rata-rata lama rawat      : <angka> hari
Kondisi paling sering     : <kondisi> (<jumlah> pasien)

============================================================
DEMO ENKAPSULASI (setter dengan data tidak valid)
============================================================
Kepuasan pasien ID <id> sebelum diubah : <nilai>
Mencoba mengubah: pasien.kepuasan = 7
ValueError tertangkap: <pesan dari setter>
Kepuasan pasien ID <id> sesudahnya     : <nilai yang sama> (tidak berubah)

============================================================
MENU
============================================================
1. Lihat 10 data pertama
2. Cari pasien berdasarkan Patient_ID
3. Tambah pasien baru
4. Keluar
Pilih menu (1-4): <ketikan pengguna>
```

Hasil tiap pilihan menu:
- **1**: tabel `ID | Umur | Gender | Kondisi | Biaya | Rawat Ulang` untuk 10 data pertama.
- **2**: `Pasien ditemukan (object dari class: <class>)` lalu rekam medis lengkap, atau
  `Pasien dengan Patient_ID <id> tidak ditemukan.`, atau `Patient_ID harus berupa angka.`
- **3**: pertanyaan untuk setiap kolom, lalu `Pasien ID <id> berhasil ditambahkan. Jumlah data sekarang: <jumlah>`,
  atau `Data tidak valid: <pesan setter>` dan `Pasien baru tidak ditambahkan.`
- **4**: `Terima kasih. Program selesai.`; pilihan lain: `Pilihan tidak tersedia. Masukkan angka 1 sampai 4.`

## Ringkasan Konsep OOP (Bahan Presentasi)

### 1. Class & Object
| Letak | Penjelasan |
|---|---|
| `orang.py` baris 6, `pasien.py` baris 9, `pasien_rawat_ulang.py` baris 10, `rekam_medis.py` baris 9 | Empat class, masing-masing di file sendiri. |
| `main.py` baris 46, 48, 56 | Object dibuat (`PasienRawatUlang(...)`, `Pasien(...)`, `RekamMedis(...)`) untuk setiap baris CSV. |
| `main.py` baris 73 & 76 | CSV dibaca dengan `csv.DictReader`, lalu setiap object disimpan ke list `daftar_rekam`. |
| `rekam_medis.py` baris 14 | **Komposisi**: `RekamMedis` menyimpan object `Pasien` ("has-a"), bukan mewarisinya. |
| `rekam_medis.py` baris 89 & 93 | Method `hitung_biaya_per_hari()` dan `tampilkan_rekam()`. |
| `main.py` baris 86 | Hanya 5 object pertama yang ditampilkan (`daftar_rekam[:JUMLAH_DITAMPILKAN]`). |
| `main.py` baris 221–240 | Menu interaktif `jalankan_menu()`: lihat (baris 163), cari (baris 177 & 185), tambah (baris 201). |

### 2. Enkapsulasi
| Letak | Penjelasan |
|---|---|
| `orang.py` baris 25, 36; `pasien.py` baris 28, 39; `rekam_medis.py` baris 31–86 | Atribut private memakai double underscore (`self.__umur`, `self.__biaya`, dan seterusnya). |
| `@property` + `@nama.setter` di ketiga file tersebut | Atribut hanya bisa dibaca dan diubah lewat getter/setter. |
| `orang.py` baris 24 & 35, `pasien.py` baris 38, `rekam_medis.py` baris 41, 52, 63, 74 & 85 | Validasi `raise ValueError` untuk Age, Gender, Satisfaction, Condition, Procedure, Cost, Length_of_Stay, dan Outcome. |
| `main.py` baris 50 | Validasi Readmission (`Yes`/`No`) saat menentukan class yang dipakai. |
| `orang.py` baris 12–13 (pola yang sama ada di semua constructor) | Constructor mengisi nilai lewat setter, sehingga data dari CSV langsung tervalidasi. |
| `main.py` baris 139–143 | Demo `try-except`: `pasien.kepuasan = 7` ditolak, dan nilai lama tetap aman. |
| `main.py` baris 75–80 | Baris CSV yang ditolak setter dilewati dan nomornya dicatat (`baris_dilewati`). |
| `main.py` baris 212 | Data dari menu tambah pasien diperiksa oleh setter yang sama dengan data CSV. |

### 3. Inheritance
| Letak | Penjelasan |
|---|---|
| `pasien.py` baris 9, `pasien_rawat_ulang.py` baris 10 | Pewarisan bertingkat **Orang → Pasien → PasienRawatUlang**. |
| `pasien.py` baris 14, `pasien_rawat_ulang.py` baris 15 | **Constructor chaining** dengan `super().__init__()`. |
| `pasien_rawat_ulang.py` baris 18–20 | Method khusus `status_rawat()`: perilaku yang hanya dimiliki `PasienRawatUlang`. |
| `orang.py` baris 39 → `pasien.py` baris 42 → `pasien_rawat_ulang.py` baris 23 | **Method overriding** `tampilkan_info()`. Setiap level memanggil `super().tampilkan_info()` lalu menambah barisnya sendiri; `PasienRawatUlang` menambah baris dari `status_rawat()`. |
| `rekam_medis.py` baris 98 | Polimorfisme: `self.pasien.tampilkan_info()` otomatis memanggil versi milik class object-nya. |
| `main.py` baris 102 & 169, `rekam_medis.py` baris 29 | `isinstance()` mengenali hubungan pewarisan (menghitung pasien rawat ulang, kolom Rawat Ulang di menu, dan `PasienRawatUlang` diterima sebagai `Pasien`). |
