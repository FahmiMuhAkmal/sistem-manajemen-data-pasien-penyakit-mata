# pasien_mata.py
# [INHERITANCE] Pewarisan bertingkat: Orang -> Pasien -> PasienMata.
# [KOMPOSISI] PasienMata MEMILIKI dua object PemeriksaanMata (mata kiri & kanan)
# dan daftar object PenyakitMata (satu pasien bisa punya lebih dari satu penyakit).
# Atribut dari kolom data: penanda N, D, G, C, A, H, M, O -> kode_diagnosis.

from pasien import Pasien
from pemeriksaan_mata import PemeriksaanMata
from penyakit_mata import PenyakitMata


class PasienMata(Pasien):
    """Pasien poli mata yang kedua matanya sudah difoto fundus."""

    KODE_PENANDA = "NDGCAHMO"  # urutan kolom penanda diagnosis di data (N = normal)

    def __init__(self, id_pasien, umur, jenis_kelamin, mata_kiri, mata_kanan,
                 kode_diagnosis, daftar_penyakit):
        # [INHERITANCE] Constructor chaining: Pasien -> Orang
        super().__init__(id_pasien, umur, jenis_kelamin)
        # [ENKAPSULASI] Urutan penting: kode_diagnosis diisi sebelum daftar_penyakit
        # karena setter daftar_penyakit mencocokkan keduanya.
        self.mata_kiri = mata_kiri
        self.mata_kanan = mata_kanan
        self.kode_diagnosis = kode_diagnosis
        self.daftar_penyakit = daftar_penyakit

    # ---------- [ENKAPSULASI] getter & setter ----------
    @property
    def mata_kiri(self):
        return self.__mata_kiri

    @mata_kiri.setter
    def mata_kiri(self, nilai):
        self.__mata_kiri = self.__cek_pemeriksaan(nilai, "kiri", "_left.jpg")

    @property
    def mata_kanan(self):
        return self.__mata_kanan

    @mata_kanan.setter
    def mata_kanan(self, nilai):
        self.__mata_kanan = self.__cek_pemeriksaan(nilai, "kanan", "_right.jpg")

    def __cek_pemeriksaan(self, nilai, sisi, akhiran):
        """Method private: pemeriksaan harus object PemeriksaanMata, sisinya benar,
        dan nama fotonya sesuai ID pasien (contoh: ID 7 -> 7_left.jpg)."""
        if not isinstance(nilai, PemeriksaanMata) or nilai.sisi != sisi:
            raise ValueError(f"Mata {sisi} harus berupa object PemeriksaanMata sisi {sisi}")
        if nilai.nama_foto != f"{self.id_pasien}{akhiran}":
            raise ValueError(f"Nama foto '{nilai.nama_foto}' tidak sesuai dengan ID pasien {self.id_pasien}")
        return nilai

    @property
    def kode_diagnosis(self):
        return self.__kode_diagnosis

    @kode_diagnosis.setter
    def kode_diagnosis(self, nilai):
        # Aturan data: minimal satu penanda, hurufnya dari N D G C A H M O,
        # tidak ada huruf ganda, dan N (normal) tidak boleh bersamaan dengan penyakit.
        if not isinstance(nilai, str) or nilai == "":
            raise ValueError("Kode diagnosis tidak boleh kosong")
        for huruf in nilai:
            if huruf not in PasienMata.KODE_PENANDA or nilai.count(huruf) > 1:
                raise ValueError(f"Kode diagnosis tidak valid: '{nilai}'")
        if "N" in nilai and len(nilai) > 1:
            raise ValueError("Penanda normal (N) tidak boleh bersamaan dengan penyakit")
        self.__kode_diagnosis = nilai

    @property
    def daftar_penyakit(self):
        return list(self.__daftar_penyakit)  # kirim salinan agar isi asli tidak diubah dari luar

    @daftar_penyakit.setter
    def daftar_penyakit(self, nilai):
        if not isinstance(nilai, list):
            raise ValueError("Daftar penyakit harus berupa list")
        kode_ditemukan = ""
        for penyakit in nilai:
            if not isinstance(penyakit, PenyakitMata):
                raise ValueError("Isi daftar penyakit harus object PenyakitMata")
            kode_ditemukan += penyakit.kode
        # Validasi silang: penyakit yang dikenali dari kata kunci diagnosis harus sama
        # dengan penanda yang diberi dokter (kolom D, G, C, A, H, M, O).
        kode_penanda = self.kode_diagnosis.replace("N", "")
        if sorted(kode_ditemukan) != sorted(kode_penanda):
            raise ValueError(f"Penanda diagnosis '{self.kode_diagnosis}' tidak cocok dengan "
                             f"kata kunci diagnosis (terbaca: '{kode_ditemukan or 'N'}')")
        self.__daftar_penyakit = list(nilai)

    # ---------- Method ----------
    def apakah_normal(self):
        """True jika pasien tidak memiliki penyakit mata."""
        return len(self.__daftar_penyakit) == 0

    def jumlah_penyakit(self):
        return len(self.__daftar_penyakit)

    def nama_penyakit(self):
        """Nama semua penyakit pasien dalam satu teks, atau 'Normal'."""
        if self.apakah_normal():
            return "Normal"
        nama = []
        for penyakit in self.__daftar_penyakit:
            nama.append(penyakit.nama)
        return ", ".join(nama)

    # ---------- [INHERITANCE] Method overriding ----------
    def tampilkan_info(self):
        """Override tampilkan_info() milik Pasien: tambah hasil pemeriksaan, penyakit, dan penanganannya."""
        super().tampilkan_info()  # tampilkan ID, umur, jenis kelamin
        self.mata_kiri.tampilkan_info()
        self.mata_kanan.tampilkan_info()
        if self.apakah_normal():
            print("Penyakit         : tidak ada (normal)")
        else:
            print(f"Penyakit         : {self.jumlah_penyakit()} kelompok")
            for penyakit in self.__daftar_penyakit:
                # [POLIMORFISME] Versi tampilkan_info() dan penanganan() mengikuti class object penyakitnya
                penyakit.tampilkan_info(self.mata_kiri, self.mata_kanan)
                penyakit.tampilkan_penanganan(self.mata_kiri, self.mata_kanan)
            print("Catatan          : pengobatan di atas informasi umum, bukan resep dokter")
