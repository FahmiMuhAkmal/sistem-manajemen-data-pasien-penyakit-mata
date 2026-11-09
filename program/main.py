# main.py
# Program utama Sistem Manajemen Data Pasien Penyakit Mata.
# Cara menjalankan (dari dalam folder program): python main.py
# Hanya memakai library bawaan Python (csv dan os).
# Data: ODIR-5K (Ocular Disease Intelligent Recognition), file data/full_df.csv.

import csv
import os

from degenerasi_makula import DegenerasiMakula
from glaukoma import Glaukoma
from kelainan_lain import KelainanLain
from pasien_mata import PasienMata
from pemeriksaan_mata import PemeriksaanMata
from penyakit_mata import PenyakitMata
from retinopati_diabetik import RetinopatiDiabetik

# File CSV dicari di folder data/ (di samping main.py) atau di folder yang sama dengan main.py.
FOLDER_PROGRAM = os.path.dirname(os.path.abspath(__file__))
LOKASI_DATA = [os.path.join(FOLDER_PROGRAM, "data", "full_df.csv"),
               os.path.join(FOLDER_PROGRAM, "full_df.csv")]
JUMLAH_DITAMPILKAN = 10

# Kolom yang berisi data pasien. Satu pasien bisa muncul di 2 baris CSV
# (satu baris per foto mata), dan isi kolom-kolom ini harus sama di kedua baris.
KOLOM_PASIEN = ["ID", "Patient Age", "Patient Sex", "Left-Fundus", "Right-Fundus",
                "Left-Diagnostic Keywords", "Right-Diagnostic Keywords",
                "N", "D", "G", "C", "A", "H", "M", "O"]


def cetak_judul(judul):
    print()
    print("=" * 64)
    print(judul)
    print("=" * 64)


def cari_file_csv():
    """Mengembalikan lokasi file CSV, atau None jika tidak ditemukan."""
    for lokasi in LOKASI_DATA:
        if os.path.exists(lokasi):
            return lokasi
    return None


def ke_bilangan_bulat(teks, nama_kolom):
    """Mengubah teks menjadi bilangan bulat, dengan pesan error berbahasa Indonesia."""
    try:
        return int(teks)
    except ValueError:
        raise ValueError(f"{nama_kolom} harus berupa bilangan bulat, bukan '{teks.strip()}'")


def buat_daftar_jenis_penyakit():
    """[CLASS & OBJECT] Membuat 7 object jenis penyakit mata (satu per kolom penanda).
    Pengobatan & saran adalah informasi umum (sumber: NEI dan AAO), bukan resep dokter."""
    retinopati = RetinopatiDiabetik()
    glaukoma = Glaukoma()
    katarak = PenyakitMata(
        "C", "Katarak", "lensa mata", ["cataract"],
        pengobatan=["operasi katarak: lensa yang keruh diganti lensa buatan (IOL)",
                    "belum ada obat tetes atau obat minum yang terbukti menyembuhkan katarak"],
        saran=["tahap awal: kacamata baru dan penerangan ruangan yang lebih terang",
               "operasi bila penglihatan sudah mengganggu aktivitas sehari-hari",
               "pakai kacamata hitam atau topi saat terik, dan jangan merokok"])
    makula = DegenerasiMakula()
    hipertensi = PenyakitMata(
        "H", "Retinopati hipertensi", "retina", ["hypertensive retinopathy"],
        pengobatan=["menurunkan tekanan darah dengan obat antihipertensi dari dokter",
                    "kelainan retina umumnya membaik bila tekanan darah terkontrol"],
        saran=["cek tekanan darah rutin dan minum obat sesuai resep",
               "kurangi garam, rutin berolahraga, dan jangan merokok",
               "segera ke dokter bila penglihatan tiba-tiba kabur"])
    miopia = PenyakitMata(
        "M", "Miopia patologis", "retina", ["pathological myopia", "myopia retinopathy", "myopic maculopathy"],
        pengobatan=["kacamata atau lensa kontak untuk memperjelas penglihatan",
                    "bila ada komplikasi: suntikan anti-VEGF atau operasi retina"],
        saran=["periksa retina rutin karena retina lebih tipis dan mudah robek",
               "segera ke dokter bila muncul kilatan cahaya atau banyak bintik melayang",
               "atau bila ada bayangan seperti tirai yang menutupi pandangan"])
    enam_kelompok = [retinopati, glaukoma, katarak, makula, hipertensi, miopia]
    # KelainanLain perlu tahu kata kunci 6 kelompok lain agar tidak terhitung dua kali
    kata_kunci_lain = []
    for penyakit in enam_kelompok:
        kata_kunci_lain.extend(penyakit.kata_kunci)
    return enam_kelompok + [KelainanLain(kata_kunci_lain)]


def baca_kode_diagnosis(baris):
    """Menggabungkan penanda N, D, G, C, A, H, M, O yang bernilai 1, misalnya 'DO'."""
    kode = ""
    for huruf in PasienMata.KODE_PENANDA:
        nilai = baris[huruf].strip()
        if nilai not in ("0", "1"):
            raise ValueError(f"Penanda {huruf} harus 0 atau 1, bukan '{nilai}'")
        if nilai == "1":
            kode += huruf
    return kode


def deteksi_penyakit(mata_kiri, mata_kanan, daftar_jenis):
    """Mencari jenis penyakit yang kata kuncinya ada di mata kiri atau kanan."""
    hasil = []
    for penyakit in daftar_jenis:
        # [POLIMORFISME] ditemukan_di() milik KelainanLain bekerja berbeda dari induknya
        if penyakit.ditemukan_di(mata_kiri) or penyakit.ditemukan_di(mata_kanan):
            hasil.append(penyakit)
    return hasil


def buat_pasien(baris, daftar_jenis):
    """[CLASS & OBJECT] Mengubah satu baris CSV menjadi object PasienMata."""
    # [KOMPOSISI] Object PemeriksaanMata dibuat dulu, lalu dimasukkan ke PasienMata
    mata_kiri = PemeriksaanMata("kiri", baris["Left-Fundus"].strip(), baris["Left-Diagnostic Keywords"])
    mata_kanan = PemeriksaanMata("kanan", baris["Right-Fundus"].strip(), baris["Right-Diagnostic Keywords"])
    return PasienMata(
        ke_bilangan_bulat(baris["ID"], "ID"),
        ke_bilangan_bulat(baris["Patient Age"], "Umur"),
        baris["Patient Sex"].strip(),
        mata_kiri,
        mata_kanan,
        baca_kode_diagnosis(baris),
        deteksi_penyakit(mata_kiri, mata_kanan, daftar_jenis),
    )


def muat_data(lokasi_file, daftar_jenis):
    """Membaca CSV, menggabungkan baris milik pasien yang sama, dan mencatat baris tidak valid."""
    daftar_pasien = []
    isi_per_id = {}        # ID -> isi kolom pasien dari baris pertama yang valid
    baris_dilewati = []    # nomor baris CSV yang tidak valid
    baris_digabung = 0     # baris foto mata kedua dari pasien yang sama
    # utf-8-sig: tetap aman jika CSV pernah disimpan ulang lewat Excel (ada BOM)
    with open(lokasi_file, mode="r", encoding="utf-8-sig", newline="") as file:
        # restval="": kolom yang hilang dianggap teks kosong, jadi ikut ditolak validasi
        pembaca = csv.DictReader(file, restval="")
        for kolom in KOLOM_PASIEN:
            if kolom not in (pembaca.fieldnames or []):
                raise ValueError(f"Kolom '{kolom}' tidak ada di file CSV")
        for baris in pembaca:
            try:
                isi = tuple(baris[kolom] for kolom in KOLOM_PASIEN)
                id_teks = baris["ID"].strip()
                if id_teks in isi_per_id:
                    # Baris foto mata kedua: isinya harus sama dengan baris pertama
                    if isi != isi_per_id[id_teks]:
                        raise ValueError(f"Data pasien ID {id_teks} berbeda dengan baris sebelumnya")
                    baris_digabung += 1
                    continue
                daftar_pasien.append(buat_pasien(baris, daftar_jenis))
                isi_per_id[id_teks] = isi
            except ValueError as error:
                # Baris yang melanggar aturan dilewati dan dicatat, program tetap berjalan
                baris_dilewati.append(pembaca.line_num)
                print(f"[PERINGATAN] Baris {pembaca.line_num} dilewati: {error}")
    return daftar_pasien, baris_dilewati, baris_digabung


def demo_validasi(daftar_pasien):
    """[ENKAPSULASI] Contoh data tidak valid yang ditolak setter."""
    cetak_judul("DEMO ENKAPSULASI (data tidak valid ditolak)")
    pasien = daftar_pasien[0]
    print(f"Umur pasien ID {pasien.id_pasien} sebelum diubah : {pasien.umur}")
    print("Mencoba mengubah: pasien.umur = -5")
    try:
        pasien.umur = -5  # tidak valid, umur harus 1 sampai 120
    except ValueError as error:
        print(f"ValueError tertangkap: {error}")
    print(f"Umur pasien ID {pasien.id_pasien} sesudahnya     : {pasien.umur} (tidak berubah)")
    print()
    print("Mencoba membuat pasien berpenanda katarak (C), tetapi diagnosisnya normal")
    try:
        mata_kiri = PemeriksaanMata("kiri", "9999_left.jpg", "normal fundus")
        mata_kanan = PemeriksaanMata("kanan", "9999_right.jpg", "normal fundus")
        PasienMata(9999, 50, "Male", mata_kiri, mata_kanan, "C", [])
    except ValueError as error:
        print(f"ValueError tertangkap: {error}")


# ======================== MENU INTERAKTIF ========================

def menu_lihat_data(daftar_pasien, awal):
    """Menu 1: menampilkan 10 pasien mulai dari index `awal`, lalu mengembalikan index berikutnya.
    Setiap kali menu 1 dipilih, data berlanjut: 1-10, lalu 11-20, lalu 21-30, dan seterusnya."""
    akhir = min(awal + JUMLAH_DITAMPILKAN, len(daftar_pasien))
    cetak_judul(f"DATA PASIEN {awal + 1}-{akhir} (dari {len(daftar_pasien)} pasien)")
    print(f"{'No':<6}{'ID':<6}{'Umur':<6}{'Kelamin':<9}Penyakit")
    for nomor, pasien in enumerate(daftar_pasien[awal:akhir], start=awal + 1):
        print(f"{nomor:<6}{pasien.id_pasien:<6}{pasien.umur:<6}{pasien.jenis_kelamin:<9}{pasien.nama_penyakit()}")
    if akhir == len(daftar_pasien):
        # Data terakhir sudah tampil: pilihan menu 1 berikutnya mulai lagi dari data pertama
        print("\nSemua data sudah ditampilkan. Pilih menu 1 lagi untuk mulai dari data pertama.")
        return 0
    return akhir


def cari_pasien(daftar_pasien, id_pasien):
    """Mengembalikan pasien dengan ID tersebut, atau None jika tidak ada."""
    for pasien in daftar_pasien:
        if pasien.id_pasien == id_pasien:
            return pasien
    return None


def menu_cari_id(daftar_pasien):
    """Menu 2: mencari pasien berdasarkan ID."""
    cetak_judul("CARI PASIEN BERDASARKAN ID")
    try:
        id_pasien = int(input("Masukkan ID pasien: "))
    except ValueError:
        print("ID pasien harus berupa angka.")
        return
    pasien = cari_pasien(daftar_pasien, id_pasien)
    if pasien is None:
        print(f"Pasien dengan ID {id_pasien} tidak ditemukan.")
    else:
        pasien.tampilkan_info()


def menu_cari_penyakit(daftar_pasien, daftar_jenis):
    """Menu 3: menampilkan pasien yang memiliki penyakit tertentu."""
    cetak_judul("CARI PASIEN BERDASARKAN PENYAKIT")
    for nomor, penyakit in enumerate(daftar_jenis, start=1):
        print(f"{nomor}. {penyakit.nama}")
    try:
        pilihan = int(input(f"Pilih penyakit (1-{len(daftar_jenis)}): "))
    except ValueError:
        print("Pilihan harus berupa angka.")
        return
    if pilihan < 1 or pilihan > len(daftar_jenis):
        print("Pilihan tidak tersedia.")
        return
    penyakit = daftar_jenis[pilihan - 1]
    hasil = []
    for pasien in daftar_pasien:
        if penyakit in pasien.daftar_penyakit:
            hasil.append(pasien)
    print(f"\n{penyakit.nama}: {len(hasil)} pasien. {JUMLAH_DITAMPILKAN} pertama:")
    print(f"{'ID':<6}{'Umur':<6}{'Kelamin':<9}Mata terkena")
    for pasien in hasil[:JUMLAH_DITAMPILKAN]:
        mata = penyakit.mata_terdampak(pasien.mata_kiri, pasien.mata_kanan)
        print(f"{pasien.id_pasien:<6}{pasien.umur:<6}{pasien.jenis_kelamin:<9}{mata}")


def menu_tambah_pasien(daftar_pasien, daftar_jenis):
    """Menu 4: menambah pasien baru ke list (file CSV asli tidak diubah)."""
    cetak_judul("TAMBAH PASIEN BARU")
    # ID dibuat otomatis (ID terbesar + 1) agar tidak ada ID ganda
    id_baru = max(pasien.id_pasien for pasien in daftar_pasien) + 1
    print(f"ID pasien baru (otomatis)    : {id_baru}")
    print("Tulis diagnosis dengan istilah dokter seperti di data, pisahkan dengan koma.")
    print("Contoh: normal fundus / cataract / glaucoma / mild nonproliferative retinopathy")
    try:
        umur = ke_bilangan_bulat(input("Umur                         : "), "Umur")
        jenis_kelamin = input("Jenis kelamin (Male/Female)  : ").strip()
        mata_kiri = PemeriksaanMata("kiri", f"{id_baru}_left.jpg", input("Diagnosis mata kiri          : "))
        mata_kanan = PemeriksaanMata("kanan", f"{id_baru}_right.jpg", input("Diagnosis mata kanan         : "))
        daftar_penyakit = deteksi_penyakit(mata_kiri, mata_kanan, daftar_jenis)
        kode = ""
        for penyakit in daftar_penyakit:
            kode += penyakit.kode
        # [ENKAPSULASI] Data baru diperiksa oleh setter yang sama dengan data CSV
        pasien = PasienMata(id_baru, umur, jenis_kelamin, mata_kiri, mata_kanan, kode or "N", daftar_penyakit)
    except ValueError as error:
        print(f"Data tidak valid: {error}")
        print("Pasien baru tidak ditambahkan.")
        return
    daftar_pasien.append(pasien)
    print(f"Pasien ID {id_baru} berhasil ditambahkan ({pasien.nama_penyakit()}). "
          f"Jumlah pasien sekarang: {len(daftar_pasien)}")


def menu_ringkasan(daftar_pasien, daftar_jenis):
    """Menu 5: ringkasan jumlah pasien, umur, dan setiap penyakit."""
    cetak_judul("RINGKASAN DATA")
    total = len(daftar_pasien)
    laki_laki = 0
    total_umur = 0
    normal = 0
    lebih_dari_satu = 0
    for pasien in daftar_pasien:
        total_umur += pasien.umur
        if pasien.jenis_kelamin == "Male":
            laki_laki += 1
        if pasien.apakah_normal():
            normal += 1
        if pasien.jumlah_penyakit() > 1:
            lebih_dari_satu += 1
    print(f"Jumlah pasien             : {total}")
    print(f"Laki-laki / Perempuan     : {laki_laki} / {total - laki_laki}")
    print(f"Rata-rata umur            : {total_umur / total:.1f} tahun")
    print(f"Pasien normal             : {normal}")
    print(f"Pasien > 1 kelompok       : {lebih_dari_satu}")
    print()
    print(f"{'Penyakit':<24}{'Pasien':>7}{'Rata umur':>11}{'Kedua mata':>12}")
    terbanyak = None
    jumlah_terbanyak = 0
    for penyakit in daftar_jenis:
        jumlah = 0
        total_umur_penyakit = 0
        kedua_mata = 0
        for pasien in daftar_pasien:
            if penyakit in pasien.daftar_penyakit:
                jumlah += 1
                total_umur_penyakit += pasien.umur
                if penyakit.mata_terdampak(pasien.mata_kiri, pasien.mata_kanan) == "kedua mata":
                    kedua_mata += 1
        rata_umur = total_umur_penyakit / jumlah if jumlah > 0 else 0
        print(f"{penyakit.nama:<24}{jumlah:>7}{rata_umur:>11.1f}{kedua_mata:>12}")
        if jumlah > jumlah_terbanyak:
            terbanyak = penyakit
            jumlah_terbanyak = jumlah
    if terbanyak is not None:
        print(f"\nPenyakit terbanyak        : {terbanyak.nama} ({jumlah_terbanyak} pasien)")


def jalankan_menu(daftar_pasien, daftar_jenis):
    """Menampilkan menu berulang-ulang sampai pengguna memilih Keluar."""
    awal = 0  # index data yang ditampilkan menu 1 berikutnya (bertambah 10 setiap kali menu 1 dipilih)
    while True:
        akhir = min(awal + JUMLAH_DITAMPILKAN, len(daftar_pasien))
        cetak_judul("MENU")
        print(f"1. Lihat data pasien {awal + 1}-{akhir}")
        print("2. Cari pasien berdasarkan ID")
        print("3. Cari pasien berdasarkan penyakit")
        print("4. Tambah pasien baru")
        print("5. Tampilkan ringkasan")
        print("6. Keluar")
        pilihan = input("Pilih menu (1-6): ").strip()
        if pilihan == "1":
            awal = menu_lihat_data(daftar_pasien, awal)
        elif pilihan == "2":
            menu_cari_id(daftar_pasien)
        elif pilihan == "3":
            menu_cari_penyakit(daftar_pasien, daftar_jenis)
        elif pilihan == "4":
            menu_tambah_pasien(daftar_pasien, daftar_jenis)
        elif pilihan == "5":
            menu_ringkasan(daftar_pasien, daftar_jenis)
        elif pilihan == "6":
            print("Terima kasih. Program selesai.")
            break
        else:
            print("Pilihan tidak tersedia. Masukkan angka 1 sampai 6.")


def main():
    cetak_judul("SISTEM MANAJEMEN DATA PASIEN PENYAKIT MATA")

    lokasi_file = cari_file_csv()
    if lokasi_file is None:
        print("File CSV tidak ditemukan!")
        print("Letakkan 'full_df.csv' di folder data/ di samping main.py.")
        return

    # [CLASS & OBJECT] 7 object jenis penyakit, lalu setiap pasien menjadi object PasienMata
    daftar_jenis = buat_daftar_jenis_penyakit()
    try:
        daftar_pasien, baris_dilewati, baris_digabung = muat_data(lokasi_file, daftar_jenis)
    except ValueError as error:
        print(f"File CSV tidak sesuai format: {error}")
        return
    print(f"File data          : {os.path.basename(lokasi_file)}")
    print(f"Pasien dimuat      : {len(daftar_pasien)} object PasienMata")
    print(f"Baris digabung     : {baris_digabung} (foto mata kedua dari pasien yang sama)")
    print(f"Baris dilewati     : {len(baris_dilewati)}")
    if len(baris_dilewati) > 0:
        print(f"Nomor baris CSV    : {baris_dilewati}")

    if len(daftar_pasien) == 0:
        print("Tidak ada data valid yang bisa diproses.")
        return

    demo_validasi(daftar_pasien)
    jalankan_menu(daftar_pasien, daftar_jenis)


if __name__ == "__main__":
    main()
