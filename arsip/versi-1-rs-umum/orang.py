# orang.py
# [CLASS & OBJECT] Class Orang adalah class induk (parent class).
# Atribut diambil dari kolom CSV: Age -> umur, Gender -> jenis_kelamin.


class Orang:
    """Menyimpan data dasar seseorang: umur dan jenis kelamin."""

    def __init__(self, umur, jenis_kelamin):
        # [ENKAPSULASI] Nilai diisi lewat setter, jadi langsung divalidasi
        # sebelum disimpan ke atribut private (self.__umur, self.__jenis_kelamin).
        self.umur = umur
        self.jenis_kelamin = jenis_kelamin

    # ---------- [ENKAPSULASI] getter & setter ----------
    @property
    def umur(self):
        return self.__umur

    @umur.setter
    def umur(self, nilai):
        # Aturan data: Age harus bilangan positif
        if not isinstance(nilai, int) or nilai <= 0:
            raise ValueError(f"Umur harus bilangan bulat positif, bukan {nilai}")
        self.__umur = nilai

    @property
    def jenis_kelamin(self):
        return self.__jenis_kelamin

    @jenis_kelamin.setter
    def jenis_kelamin(self, nilai):
        # Aturan data: Gender hanya Male atau Female
        if nilai not in ("Male", "Female"):
            raise ValueError(f"Jenis kelamin harus 'Male' atau 'Female', bukan '{nilai}'")
        self.__jenis_kelamin = nilai

    # ---------- Method ----------
    def tampilkan_info(self):
        """Menampilkan info dasar. Method ini di-override oleh class turunan."""
        print(f"Umur           : {self.umur} tahun")
        print(f"Jenis Kelamin  : {self.jenis_kelamin}")
