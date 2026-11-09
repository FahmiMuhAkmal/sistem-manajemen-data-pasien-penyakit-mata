# Prompt final project (versi penyakit mata)

Prompt ini menggambarkan program yang sekarang ada di folder `program/`. Bisa dipakai untuk menjelaskan project ke
dosen atau untuk membuat ulang project dengan AI lain.

---

Buatkan saya project coding dalam bahasa Python bertema **SISTEM MANAJEMEN DATA PASIEN PENYAKIT MATA** yang
menerapkan konsep OOP: Class dan Object, Enkapsulasi, dan Inheritance.

**Sumber data (data nyata, bukan fiktif):** dataset ODIR-5K (Ocular Disease Intelligent Recognition) di Kaggle:
https://www.kaggle.com/datasets/andrewmvd/ocular-disease-recognition-odir5k
File `full_df.csv` (6.392 baris, 1 baris = 1 foto fundus; satu pasien bisa muncul di 2 baris).
Kolom yang dipakai: ID, Patient Age, Patient Sex, Left-Fundus, Right-Fundus, Left-Diagnostic Keywords,
Right-Diagnostic Keywords, N, D, G, C, A, H, M, O. Kolom filepath, labels, target, filename tidak dipakai.
Jangan menambah atribut di luar kolom data. Jika file tidak bisa diunduh, jangan membuat data karangan.

1. Class dan Object
- Orang (class induk): umur, jenis_kelamin.
- Pasien (mewarisi Orang): id_pasien.
- PasienMata (mewarisi Pasien): mata_kiri, mata_kanan (object PemeriksaanMata), kode_diagnosis (gabungan penanda
  bernilai 1, misalnya "DO"), daftar_penyakit (list object PenyakitMata). Method: apakah_normal(),
  jumlah_penyakit(), nama_penyakit(), tampilkan_info().
- PemeriksaanMata (tanpa pewarisan, dipakai lewat komposisi): sisi (kiri/kanan), nama_foto, diagnosis.
  Method daftar_kata_kunci() (pemisah koma biasa dan koma lebar "，"), catatan_foto() (lens dust, low image
  quality, dan catatan foto lain yang bukan penyakit).
- PenyakitMata (class induk penyakit): kode, nama, bagian_mata, kata_kunci. Method ditemukan_di(pemeriksaan),
  mata_terdampak(kiri, kanan), tampilkan_info(kiri, kanan).
- Turunan PenyakitMata: RetinopatiDiabetik (D, tingkat_keparahan()), DegenerasiMakula (A, jenis() kering/basah),
  Glaukoma (G, status() pasti/dugaan), KelainanLain (O, daftar_kelainan() dan override ditemukan_di()).
  Katarak (C), Retinopati hipertensi (H), dan Miopia patologis (M) cukup object dari PenyakitMata.
- Di main.py, baca CSV dengan modul csv, buat object untuk setiap pasien, dan simpan dalam list.

2. Enkapsulasi
- Semua atribut private (awalan double underscore), diakses lewat @property dan @nama.setter.
- Setter memakai raise ValueError: umur bilangan bulat 1-120; jenis kelamin Male/Female; ID bilangan bulat >= 0;
  sisi kiri/kanan; nama foto berakhiran _left.jpg/_right.jpg dan sesuai ID; diagnosis tidak kosong; kode diagnosis
  hanya huruf N D G C A H M O tanpa huruf ganda dan N tidak boleh bersama penyakit; daftar penyakit harus cocok
  dengan penanda dokter (validasi silang).
- Getter daftar_penyakit mengembalikan salinan list.
- Sertakan contoh data tidak valid di dalam try-except (umur -5, dan pasien berpenanda C tetapi diagnosis normal).

3. Inheritance
- Pewarisan bertingkat Orang -> Pasien -> PasienMata dengan super().__init__() dan override tampilkan_info() di
  setiap level.
- Hierarki PenyakitMata dengan 4 class turunan; tampilkan_info() di-override dan dipanggil secara polimorfis.

4. Struktur dan fitur
- Satu class per file ditambah main.py, penamaan snake_case. Data di program/data/full_df.csv.
- Baris kedua milik pasien yang sama digabung (isinya harus sama). Baris tidak valid dilewati, dicatat nomor
  barisnya, dan jumlahnya ditampilkan. Kolom wajib di header dicek lebih dulu.
- Menu interaktif: lihat 10 data pertama, cari pasien berdasarkan ID, cari pasien berdasarkan penyakit, tambah
  pasien baru (ID otomatis, divalidasi setter yang sama), tampilkan ringkasan (jumlah, laki-laki/perempuan,
  rata-rata umur, pasien normal, tabel per penyakit), keluar.
- Hanya library bawaan Python. Komentar singkat berbahasa Indonesia dan tandai bagian Class/Object, Enkapsulasi,
  dan Inheritance.
- Jangan mengarang contoh output. Jelaskan cara menjalankan (cd program, python main.py).
- Gaya kode sederhana yang mudah dipahami mahasiswa.

Di akhir, buat ringkasan singkat letak penerapan ketiga konsep OOP di dalam kode untuk bahan presentasi.
