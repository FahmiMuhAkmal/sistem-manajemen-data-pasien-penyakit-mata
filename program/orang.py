# orang.py
# [CLASS & OBJECT] Class Orang adalah class induk (parent class) paling atas.
# Atribut diambil dari kolom data: Patient Age -> umur, Patient Sex -> jenis_kelamin.


class Orang:
    """Menyimpan data dasar seseorang: umur dan jenis kelamin."""

    # Nilai jenis kelamin yang ada di data (dicek dari nilai unik kolom Patient Sex)
    JENIS_KELAMIN_VALID = ("Male", "Female")

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
        # Aturan: umur bilangan bulat 1 sampai 120 tahun
        if not isinstance(nilai, int) or nilai < 1 or nilai > 120:
            raise ValueError(f"Umur harus bilangan bulat 1 sampai 120, bukan {nilai}")
        self.__umur = nilai

    @property
    def jenis_kelamin(self):
        return self.__jenis_kelamin

    @jenis_kelamin.setter
    def jenis_kelamin(self, nilai):
        # Aturan: hanya Male atau Female, sesuai isi data
        if nilai not in Orang.JENIS_KELAMIN_VALID:
            raise ValueError(f"Jenis kelamin harus 'Male' atau 'Female', bukan '{nilai}'")
        self.__jenis_kelamin = nilai

    # ---------- Method ----------
    def tampilkan_info(self):
        """Menampilkan data dasar. Method ini di-override oleh class turunan."""
        print(f"Umur             : {self.umur} tahun")
        print(f"Jenis Kelamin    : {self.jenis_kelamin}")
