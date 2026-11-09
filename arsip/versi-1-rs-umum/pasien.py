# pasien.py
# [INHERITANCE] Pasien mewarisi Orang (Orang -> Pasien).
# Atribut tambahan dari kolom CSV: Patient_ID -> patient_id, Satisfaction -> kepuasan.
# Object Pasien dipakai untuk baris CSV dengan Readmission = No.

from orang import Orang


class Pasien(Orang):
    """Pasien rumah sakit (turunan dari Orang)."""

    def __init__(self, patient_id, umur, jenis_kelamin, kepuasan):
        # [INHERITANCE] Constructor chaining: umur & jenis_kelamin diurus oleh Orang
        super().__init__(umur, jenis_kelamin)
        # [ENKAPSULASI] Diisi lewat setter agar tervalidasi
        self.patient_id = patient_id
        self.kepuasan = kepuasan

    # ---------- [ENKAPSULASI] getter & setter ----------
    @property
    def patient_id(self):
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, nilai):
        if not isinstance(nilai, int) or nilai <= 0:
            raise ValueError(f"Patient ID harus bilangan bulat positif, bukan {nilai}")
        self.__patient_id = nilai

    @property
    def kepuasan(self):
        return self.__kepuasan

    @kepuasan.setter
    def kepuasan(self, nilai):
        # Aturan data: Satisfaction bernilai 1 sampai 5
        if not isinstance(nilai, int) or nilai < 1 or nilai > 5:
            raise ValueError(f"Kepuasan harus bilangan bulat 1 sampai 5, bukan {nilai}")
        self.__kepuasan = nilai

    # ---------- [INHERITANCE] Method overriding ----------
    def tampilkan_info(self):
        """Override tampilkan_info() milik Orang: tambah ID pasien dan kepuasan."""
        print(f"ID Pasien      : {self.patient_id}")
        super().tampilkan_info()  # memakai ulang tampilan umur & jenis kelamin dari Orang
        print(f"Kepuasan       : {self.kepuasan}/5")
