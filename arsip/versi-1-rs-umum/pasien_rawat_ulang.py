# pasien_rawat_ulang.py
# [INHERITANCE] Pewarisan bertingkat: Orang -> Pasien -> PasienRawatUlang.
# Object PasienRawatUlang dipakai untuk baris CSV dengan Readmission = Yes.
# Tidak ada atribut baru karena CSV tidak punya kolom tambahan; yang membedakannya
# adalah perilaku khusus: method status_rawat() (tidak dimiliki Pasien maupun Orang).

from pasien import Pasien


class PasienRawatUlang(Pasien):
    """Pasien yang kembali dirawat (Readmission = Yes)."""

    def __init__(self, patient_id, umur, jenis_kelamin, kepuasan):
        # [INHERITANCE] Constructor chaining: Pasien -> Orang
        super().__init__(patient_id, umur, jenis_kelamin, kepuasan)

    # ---------- Method khusus PasienRawatUlang ----------
    def status_rawat(self):
        """Mengembalikan keterangan status rawat pasien ini."""
        return "Pasien rawat ulang"

    # ---------- [INHERITANCE] Method overriding ----------
    def tampilkan_info(self):
        """Override tampilkan_info() milik Pasien: tambah status_rawat()."""
        super().tampilkan_info()  # tampilkan ID, umur, jenis kelamin, kepuasan
        print(f"Status Rawat   : {self.status_rawat()}")
