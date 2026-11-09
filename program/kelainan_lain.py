# kelainan_lain.py
# [INHERITANCE] KelainanLain mewarisi PenyakitMata (kode O = other).
# Kelainan lain tidak punya daftar kata kunci tetap (ada puluhan jenis, misalnya
# drusen dan membran epiretina), jadi cara mengenalinya BERBEDA dari induknya:
# kata kunci yang bukan hasil normal, bukan catatan foto, dan bukan milik
# 6 kelompok penyakit lain dianggap kelainan lain.
# [POLIMORFISME] Method ditemukan_di() di-override.

from penyakit_mata import PenyakitMata
from pemeriksaan_mata import PemeriksaanMata


class KelainanLain(PenyakitMata):
    """Kelainan mata di luar 6 kelompok penyakit utama."""

    # Penanganan umum: jenis kelainan lain sangat beragam, jadi perlu pemeriksaan lanjutan
    PENGOBATAN = ["tergantung jenis kelainannya (lihat keterangan 'jenis' di atas)"]
    SARAN = ["periksa ke dokter mata untuk pemeriksaan lanjutan",
             "dokter menentukan apakah perlu diobati atau cukup dipantau"]

    def __init__(self, kata_kunci_kelompok_lain):
        # [INHERITANCE] Kata kunci induk dikosongkan karena cara mengenalinya berbeda
        super().__init__("O", "Kelainan lain", "bervariasi", [], KelainanLain.PENGOBATAN, KelainanLain.SARAN)
        self.kata_kunci_kelompok_lain = kata_kunci_kelompok_lain

    # ---------- [ENKAPSULASI] getter & setter ----------
    @property
    def kata_kunci_kelompok_lain(self):
        return self.__kata_kunci_kelompok_lain

    @kata_kunci_kelompok_lain.setter
    def kata_kunci_kelompok_lain(self, nilai):
        if not isinstance(nilai, list) or len(nilai) == 0:
            raise ValueError("Kata kunci kelompok penyakit lain harus list yang tidak kosong")
        self.__kata_kunci_kelompok_lain = nilai

    # ---------- Method khusus KelainanLain ----------
    def daftar_kelainan(self, pemeriksaan):
        """Kata kunci di satu mata yang termasuk kelainan lain."""
        hasil = []
        for kata in pemeriksaan.daftar_kata_kunci():
            if kata in PemeriksaanMata.BUKAN_PENYAKIT:
                continue
            milik_kelompok_lain = False
            for kunci in self.kata_kunci_kelompok_lain:
                if kunci in kata:
                    milik_kelompok_lain = True
            if not milik_kelompok_lain:
                hasil.append(kata)
        return hasil

    # ---------- [POLIMORFISME] Method overriding ----------
    def ditemukan_di(self, pemeriksaan):
        """Override: kelainan lain ditemukan jika daftar_kelainan() tidak kosong."""
        return len(self.daftar_kelainan(pemeriksaan)) > 0

    def tampilkan_info(self, mata_kiri, mata_kanan):
        """Override: tambahkan jenis kelainan yang ditemukan."""
        super().tampilkan_info(mata_kiri, mata_kanan)
        semua = []
        for kata in self.daftar_kelainan(mata_kiri) + self.daftar_kelainan(mata_kanan):
            if kata not in semua:
                semua.append(kata)
        print(f"      jenis: {', '.join(semua)}")
