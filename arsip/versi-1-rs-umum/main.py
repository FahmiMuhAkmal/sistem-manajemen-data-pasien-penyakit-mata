# main.py
# Program utama Sistem Manajemen Data Pasien Rumah Sakit.
# Cara menjalankan: python main.py
# Hanya memakai library bawaan Python (csv dan os).

import csv
import os

from pasien import Pasien
from pasien_rawat_ulang import PasienRawatUlang
from rekam_medis import RekamMedis

# File CSV dicari di folder yang sama dengan main.py.
# Dua variasi nama didukung: memakai garis bawah atau memakai spasi.
FOLDER_PROJECT = os.path.dirname(os.path.abspath(__file__))
NAMA_FILE_CSV = ["hospital_data_analysis.csv", "hospital data analysis.csv"]
JUMLAH_DITAMPILKAN = 5


def cetak_judul(judul):
    print()
    print("=" * 60)
    print(judul)
    print("=" * 60)


def cari_file_csv():
    """Mengembalikan lokasi file CSV, atau None jika tidak ditemukan."""
    for nama_file in NAMA_FILE_CSV:
        lokasi = os.path.join(FOLDER_PROJECT, nama_file)
        if os.path.exists(lokasi):
            return lokasi
    return None


def buat_pasien(baris):
    """[CLASS & OBJECT] Membuat object Pasien / PasienRawatUlang dari satu baris CSV."""
    patient_id = int(baris["Patient_ID"])
    umur = int(baris["Age"])
    jenis_kelamin = baris["Gender"]
    kepuasan = int(baris["Satisfaction"])
    readmission = baris["Readmission"]

    # [INHERITANCE] Kolom Readmission menentukan class object yang dibuat
    if readmission == "Yes":
        return PasienRawatUlang(patient_id, umur, jenis_kelamin, kepuasan)
    elif readmission == "No":
        return Pasien(patient_id, umur, jenis_kelamin, kepuasan)
    else:
        raise ValueError(f"Readmission harus 'Yes' atau 'No', bukan '{readmission}'")


def buat_rekam_medis(baris):
    """[CLASS & OBJECT] Membuat object RekamMedis yang berisi object Pasien (komposisi)."""
    pasien = buat_pasien(baris)
    return RekamMedis(
        pasien,
        baris["Condition"],
        baris["Procedure"],
        float(baris["Cost"]),
        int(baris["Length_of_Stay"]),
        baris["Outcome"],
    )


def muat_data(lokasi_file):
    """Membaca CSV, membuat object tiap baris, dan mencatat baris yang tidak valid."""
    daftar_rekam = []
    baris_dilewati = []  # nomor baris CSV yang tidak valid
    # utf-8-sig: tetap aman jika CSV pernah disimpan ulang lewat Excel (ada BOM)
    with open(lokasi_file, mode="r", encoding="utf-8-sig", newline="") as file:
        # restval="": kolom yang hilang dianggap teks kosong, jadi ikut ditolak validasi
        pembaca = csv.DictReader(file, restval="")
        for baris in pembaca:
            try:
                daftar_rekam.append(buat_rekam_medis(baris))
            except ValueError as error:
                # Baris yang melanggar aturan dilewati dan dicatat, program tetap berjalan
                baris_dilewati.append(pembaca.line_num)
                print(f"[PERINGATAN] Baris {pembaca.line_num} dilewati: {error}")
    return daftar_rekam, baris_dilewati


def tampilkan_rekam_pertama(daftar_rekam):
    cetak_judul(f"{JUMLAH_DITAMPILKAN} REKAM MEDIS PERTAMA (dari {len(daftar_rekam)} data)")
    for nomor, rekam in enumerate(daftar_rekam[:JUMLAH_DITAMPILKAN], start=1):
        # type(object).__name__ = nama class tempat object tersebut dibuat
        nama_class = type(rekam.pasien).__name__
        print(f"\n[{nomor}] Object pasien dari class: {nama_class}")
        rekam.tampilkan_rekam()


def tampilkan_ringkasan(daftar_rekam):
    total_pasien = len(daftar_rekam)
    jumlah_rawat_ulang = 0
    total_biaya = 0
    total_lama_rawat = 0
    jumlah_per_kondisi = {}

    for rekam in daftar_rekam:
        # [INHERITANCE] isinstance() mengenali object dari class PasienRawatUlang
        if isinstance(rekam.pasien, PasienRawatUlang):
            jumlah_rawat_ulang += 1
        # [ENKAPSULASI] Data dibaca lewat property, bukan atribut private langsung
        total_biaya += rekam.biaya
        total_lama_rawat += rekam.lama_rawat
        jumlah_per_kondisi[rekam.kondisi] = jumlah_per_kondisi.get(rekam.kondisi, 0) + 1

    rata_rata_biaya = total_biaya / total_pasien
    rata_rata_lama_rawat = total_lama_rawat / total_pasien
    persen_rawat_ulang = jumlah_rawat_ulang / total_pasien * 100

    # Kondisi terbanyak bisa lebih dari satu jika jumlahnya sama (seri)
    jumlah_terbanyak = max(jumlah_per_kondisi.values())
    kondisi_terbanyak = []
    for kondisi, jumlah in jumlah_per_kondisi.items():
        if jumlah == jumlah_terbanyak:
            kondisi_terbanyak.append(kondisi)

    if len(kondisi_terbanyak) > 1:
        keterangan = f"masing-masing {jumlah_terbanyak} pasien"
    else:
        keterangan = f"{jumlah_terbanyak} pasien"

    cetak_judul("RINGKASAN DATA")
    print(f"Total pasien              : {total_pasien}")
    print(f"Jumlah pasien rawat ulang : {jumlah_rawat_ulang} ({persen_rawat_ulang:.2f}%)")
    print(f"Rata-rata biaya           : {rata_rata_biaya:,.2f}")
    print(f"Rata-rata lama rawat      : {rata_rata_lama_rawat:.2f} hari")
    print(f"Kondisi paling sering     : {', '.join(kondisi_terbanyak)} ({keterangan})")


def demo_validasi_setter(daftar_rekam):
    """[ENKAPSULASI] Contoh setter menolak data yang tidak valid."""
    cetak_judul("DEMO ENKAPSULASI (setter dengan data tidak valid)")
    pasien = daftar_rekam[0].pasien
    print(f"Kepuasan pasien ID {pasien.patient_id} sebelum diubah : {pasien.kepuasan}")
    print("Mencoba mengubah: pasien.kepuasan = 7")
    try:
        pasien.kepuasan = 7  # tidak valid, karena aturan kepuasan 1 sampai 5
    except ValueError as error:
        print(f"ValueError tertangkap: {error}")
    print(f"Kepuasan pasien ID {pasien.patient_id} sesudahnya     : {pasien.kepuasan} (tidak berubah)")


# ======================== MENU INTERAKTIF ========================
JUMLAH_DATA_MENU = 10

# Pertanyaan saat menambah pasien baru: (nama kolom CSV, teks pertanyaan)
PERTANYAAN_PASIEN_BARU = [
    ("Age", "Umur"),
    ("Gender", "Jenis kelamin (Male/Female)"),
    ("Condition", "Kondisi"),
    ("Procedure", "Prosedur"),
    ("Cost", "Biaya"),
    ("Length_of_Stay", "Lama rawat (hari)"),
    ("Readmission", "Rawat ulang (Yes/No)"),
    ("Outcome", "Hasil (Recovered/Stable)"),
    ("Satisfaction", "Kepuasan (1-5)"),
]


def menu_lihat_data(daftar_rekam):
    """Menu 1: menampilkan 10 data pertama dalam bentuk tabel singkat."""
    cetak_judul(f"{JUMLAH_DATA_MENU} DATA PERTAMA (dari {len(daftar_rekam)} data)")
    print(f"{'ID':<5}{'Umur':<6}{'Gender':<8}{'Kondisi':<23}{'Biaya':>10}  Rawat Ulang")
    for rekam in daftar_rekam[:JUMLAH_DATA_MENU]:
        pasien = rekam.pasien
        if isinstance(pasien, PasienRawatUlang):
            rawat_ulang = "Ya"
        else:
            rawat_ulang = "Tidak"
        print(f"{pasien.patient_id:<5}{pasien.umur:<6}{pasien.jenis_kelamin:<8}"
              f"{rekam.kondisi:<23}{rekam.biaya:>10,.2f}  {rawat_ulang}")


def cari_rekam(daftar_rekam, patient_id):
    """Mengembalikan rekam medis dengan Patient_ID tersebut, atau None jika tidak ada."""
    for rekam in daftar_rekam:
        if rekam.pasien.patient_id == patient_id:
            return rekam
    return None


def menu_cari_pasien(daftar_rekam):
    """Menu 2: mencari pasien berdasarkan Patient_ID."""
    cetak_judul("CARI PASIEN BERDASARKAN PATIENT_ID")
    try:
        patient_id = int(input("Masukkan Patient_ID: "))
    except ValueError:
        print("Patient_ID harus berupa angka.")
        return
    rekam = cari_rekam(daftar_rekam, patient_id)
    if rekam is None:
        print(f"Pasien dengan Patient_ID {patient_id} tidak ditemukan.")
    else:
        print(f"Pasien ditemukan (object dari class: {type(rekam.pasien).__name__})")
        rekam.tampilkan_rekam()


def menu_tambah_pasien(daftar_rekam):
    """Menu 3: menambah pasien baru ke list (file CSV asli tidak diubah)."""
    cetak_judul("TAMBAH PASIEN BARU")
    # Patient_ID dibuat otomatis (ID terbesar + 1) agar tidak ada ID ganda
    id_baru = max(rekam.pasien.patient_id for rekam in daftar_rekam) + 1
    print(f"Patient_ID baru (otomatis)  : {id_baru}")
    baris = {"Patient_ID": str(id_baru)}
    for kolom, pertanyaan in PERTANYAAN_PASIEN_BARU:
        baris[kolom] = input(f"{pertanyaan:<28}: ").strip()
    try:
        # [ENKAPSULASI] Input diperiksa oleh setter yang sama dengan data CSV
        rekam_baru = buat_rekam_medis(baris)
    except ValueError as error:
        print(f"Data tidak valid: {error}")
        print("Pasien baru tidak ditambahkan.")
        return
    daftar_rekam.append(rekam_baru)
    print(f"Pasien ID {id_baru} berhasil ditambahkan. Jumlah data sekarang: {len(daftar_rekam)}")


def jalankan_menu(daftar_rekam):
    """Menampilkan menu berulang-ulang sampai pengguna memilih Keluar."""
    while True:
        cetak_judul("MENU")
        print(f"1. Lihat {JUMLAH_DATA_MENU} data pertama")
        print("2. Cari pasien berdasarkan Patient_ID")
        print("3. Tambah pasien baru")
        print("4. Keluar")
        pilihan = input("Pilih menu (1-4): ").strip()
        if pilihan == "1":
            menu_lihat_data(daftar_rekam)
        elif pilihan == "2":
            menu_cari_pasien(daftar_rekam)
        elif pilihan == "3":
            menu_tambah_pasien(daftar_rekam)
        elif pilihan == "4":
            print("Terima kasih. Program selesai.")
            break
        else:
            print("Pilihan tidak tersedia. Masukkan angka 1 sampai 4.")


def main():
    cetak_judul("SISTEM MANAJEMEN DATA PASIEN RUMAH SAKIT")

    lokasi_file = cari_file_csv()
    if lokasi_file is None:
        print("File CSV tidak ditemukan!")
        print("Letakkan 'hospital_data_analysis.csv' di folder yang sama dengan main.py.")
        return

    # [CLASS & OBJECT] Setiap baris CSV menjadi object, lalu disimpan di list
    daftar_rekam, baris_dilewati = muat_data(lokasi_file)
    print(f"File data         : {os.path.basename(lokasi_file)}")
    print(f"Object RekamMedis : {len(daftar_rekam)} object tersimpan di list")
    print(f"Baris dilewati    : {len(baris_dilewati)}")
    if len(baris_dilewati) > 0:
        print(f"Nomor baris CSV   : {baris_dilewati}")

    if len(daftar_rekam) == 0:
        print("Tidak ada data valid yang bisa diproses.")
        return

    tampilkan_rekam_pertama(daftar_rekam)
    tampilkan_ringkasan(daftar_rekam)
    demo_validasi_setter(daftar_rekam)
    jalankan_menu(daftar_rekam)


if __name__ == "__main__":
    main()
