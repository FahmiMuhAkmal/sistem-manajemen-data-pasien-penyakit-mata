# pemeriksaan_mata.py
# [CLASS & OBJECT] Hasil pemeriksaan foto fundus (foto retina) untuk SATU mata.
# [KOMPOSISI] Satu object PasienMata memiliki dua object PemeriksaanMata: kiri dan kanan.
# Atribut dari kolom data: Left-Fundus / Right-Fundus -> nama_foto,
# Left-Diagnostic Keywords / Right-Diagnostic Keywords -> diagnosis.


class PemeriksaanMata:
    """Hasil foto fundus satu mata beserta kata kunci diagnosis dari dokter."""

    SISI_VALID = ("kiri", "kanan")
    # Kata kunci yang BUKAN penyakit: hasil normal dan catatan kualitas foto
    # (contoh: "lens dust" = ada debu di lensa kamera saat memotret).
    BUKAN_PENYAKIT = ("normal fundus", "lens dust", "low image quality", "image offset",
                      "no fundus image", "anterior segment image", "optic disk photographically invisible")
    KOMA_LEBAR = "\uff0c"  # tanda koma lebar (，) yang dipakai di data sebagai pemisah

    def __init__(self, sisi, nama_foto, diagnosis):
        # [ENKAPSULASI] Semua nilai lewat setter; sisi diisi lebih dulu
        # karena aturan nama_foto bergantung pada sisi mata.
        self.sisi = sisi
        self.nama_foto = nama_foto
        self.diagnosis = diagnosis

    # ---------- [ENKAPSULASI] getter & setter ----------
    @property
    def sisi(self):
        return self.__sisi

    @sisi.setter
    def sisi(self, nilai):
        if nilai not in PemeriksaanMata.SISI_VALID:
            raise ValueError(f"Sisi mata harus 'kiri' atau 'kanan', bukan '{nilai}'")
        self.__sisi = nilai

    @property
    def nama_foto(self):
        return self.__nama_foto

    @nama_foto.setter
    def nama_foto(self, nilai):
        # Aturan data: foto mata kiri berakhiran _left.jpg, mata kanan _right.jpg
        akhiran = "_left.jpg" if self.sisi == "kiri" else "_right.jpg"
        if not isinstance(nilai, str) or not nilai.endswith(akhiran):
            raise ValueError(f"Nama foto mata {self.sisi} harus berakhiran {akhiran}, bukan '{nilai}'")
        self.__nama_foto = nilai

    @property
    def diagnosis(self):
        return self.__diagnosis

    @diagnosis.setter
    def diagnosis(self, nilai):
        # Aturan: diagnosis tidak boleh kosong (spasi saja juga dianggap kosong)
        if not isinstance(nilai, str) or nilai.strip() == "":
            raise ValueError(f"Diagnosis mata {self.sisi} tidak boleh kosong")
        self.__diagnosis = nilai.strip()

    # ---------- Method ----------
    def daftar_kata_kunci(self):
        """Memecah diagnosis menjadi daftar kata kunci berhuruf kecil."""
        teks = self.diagnosis.replace(PemeriksaanMata.KOMA_LEBAR, ",").lower()
        hasil = []
        for kata in teks.split(","):
            if kata.strip() != "":
                hasil.append(kata.strip())
        return hasil

    def catatan_foto(self):
        """Catatan kualitas foto (bukan penyakit), misalnya 'lens dust'."""
        hasil = []
        for kata in self.daftar_kata_kunci():
            if kata in PemeriksaanMata.BUKAN_PENYAKIT and kata != "normal fundus":
                hasil.append(kata)
        return hasil

    def tampilkan_info(self):
        """Menampilkan diagnosis asli dari dokter untuk mata ini."""
        print(f"Mata {self.sisi:<5}       : {self.diagnosis}")
