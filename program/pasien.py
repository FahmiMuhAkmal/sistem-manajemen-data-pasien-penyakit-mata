# pasien.py
# [INHERITANCE] Pasien mewarisi Orang (Orang -> Pasien).
# Atribut tambahan dari kolom data: ID -> id_pasien.

from orang import Orang


class Pasien(Orang):
    """Pasien rumah sakit (turunan dari Orang)."""

    def __init__(self, id_pasien, umur, jenis_kelamin):
        # [INHERITANCE] Constructor chaining: umur & jenis kelamin diurus oleh Orang
        super().__init__(umur, jenis_kelamin)
        # [ENKAPSULASI] Diisi lewat setter agar tervalidasi
        self.id_pasien = id_pasien

    # ---------- [ENKAPSULASI] getter & setter ----------
    @property
    def id_pasien(self):
        return self.__id_pasien

    @id_pasien.setter
    def id_pasien(self, nilai):
        # Aturan: bilangan bulat 0 atau lebih (di data memang ada pasien dengan ID 0)
        if not isinstance(nilai, int) or nilai < 0:
            raise ValueError(f"ID pasien harus bilangan bulat 0 atau lebih, bukan {nilai}")
        self.__id_pasien = nilai

    # ---------- [INHERITANCE] Method overriding ----------
    def tampilkan_info(self):
        """Override tampilkan_info() milik Orang: tambah ID pasien."""
        print(f"ID Pasien        : {self.id_pasien}")
        super().tampilkan_info()  # memakai ulang tampilan umur & jenis kelamin dari Orang
