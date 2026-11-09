# rekam_medis.py
# [CLASS & OBJECT] RekamMedis TIDAK mewarisi class lain, tetapi memakai KOMPOSISI:
# di dalamnya tersimpan sebuah object Pasien (hubungan "has-a", bukan "is-a").
# Atribut dari kolom CSV: Condition, Procedure, Cost, Length_of_Stay, Outcome.

from pasien import Pasien


class RekamMedis:
    """Rekam medis satu perawatan milik seorang pasien."""

    def __init__(self, pasien, kondisi, prosedur, biaya, lama_rawat, hasil):
        # [ENKAPSULASI] Semua nilai diisi lewat setter agar tervalidasi
        self.pasien = pasien
        self.kondisi = kondisi
        self.prosedur = prosedur
        self.biaya = biaya
        self.lama_rawat = lama_rawat
        self.hasil = hasil

    # ---------- [ENKAPSULASI] getter & setter ----------
    @property
    def pasien(self):
        return self.__pasien

    @pasien.setter
    def pasien(self, nilai):
        # Menerima object Pasien maupun turunannya (PasienRawatUlang)
        if not isinstance(nilai, Pasien):
            raise ValueError("Pasien harus berupa object dari class Pasien")
        self.__pasien = nilai

    @property
    def kondisi(self):
        return self.__kondisi

    @kondisi.setter
    def kondisi(self, nilai):
        # Aturan data: Condition tidak boleh kosong
        if not isinstance(nilai, str) or nilai.strip() == "":
            raise ValueError("Kondisi tidak boleh kosong")
        self.__kondisi = nilai

    @property
    def prosedur(self):
        return self.__prosedur

    @prosedur.setter
    def prosedur(self, nilai):
        # Aturan data: Procedure tidak boleh kosong
        if not isinstance(nilai, str) or nilai.strip() == "":
            raise ValueError("Prosedur tidak boleh kosong")
        self.__prosedur = nilai

    @property
    def biaya(self):
        return self.__biaya

    @biaya.setter
    def biaya(self, nilai):
        # Aturan data: Cost harus bilangan positif
        if not isinstance(nilai, (int, float)) or nilai <= 0:
            raise ValueError(f"Biaya harus bilangan positif, bukan {nilai}")
        self.__biaya = nilai

    @property
    def lama_rawat(self):
        return self.__lama_rawat

    @lama_rawat.setter
    def lama_rawat(self, nilai):
        # Aturan data: Length_of_Stay bulat > 0 (mencegah pembagian nol)
        if not isinstance(nilai, int) or nilai <= 0:
            raise ValueError(f"Lama rawat harus bilangan bulat positif, bukan {nilai}")
        self.__lama_rawat = nilai

    @property
    def hasil(self):
        return self.__hasil

    @hasil.setter
    def hasil(self, nilai):
        # Aturan data: Outcome hanya Recovered atau Stable
        if nilai not in ("Recovered", "Stable"):
            raise ValueError(f"Hasil harus 'Recovered' atau 'Stable', bukan '{nilai}'")
        self.__hasil = nilai

    # ---------- Method ----------
    def hitung_biaya_per_hari(self):
        """Menghitung biaya rata-rata untuk setiap hari rawat."""
        return self.biaya / self.lama_rawat

    def tampilkan_rekam(self):
        """Menampilkan data pasien dan data medis."""
        print("--- Data Pasien ---")
        # Polimorfisme: versi tampilkan_info() yang dipanggil
        # menyesuaikan class object-nya (Pasien atau PasienRawatUlang).
        self.pasien.tampilkan_info()
        print("--- Data Medis ---")
        print(f"Kondisi        : {self.kondisi}")
        print(f"Prosedur       : {self.prosedur}")
        print(f"Biaya          : {self.biaya:,.2f}")
        print(f"Lama Rawat     : {self.lama_rawat} hari")
        print(f"Biaya per Hari : {self.hitung_biaya_per_hari():,.2f}")
        print(f"Hasil          : {self.hasil}")
