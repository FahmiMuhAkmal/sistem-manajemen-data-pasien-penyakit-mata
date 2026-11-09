# penyakit_mata.py
# [CLASS & OBJECT] Class induk untuk SATU JENIS penyakit mata.
# Jenis penyakit dikenali dari kata kunci diagnosis dokter. Kode mengikuti
# kolom penanda di data: D, G, C, A, H, M, O. (Kolom N = normal, bukan penyakit.)
# Setiap penyakit juga menyimpan penanganan umum: pengobatan dan hal yang harus dilakukan.
# [INHERITANCE] Diturunkan menjadi RetinopatiDiabetik, DegenerasiMakula,
# Glaukoma, dan KelainanLain.


class PenyakitMata:
    """Satu jenis penyakit mata beserta kata kunci pengenal dan penanganan umumnya."""

    KODE_VALID = ("D", "G", "C", "A", "H", "M", "O")

    def __init__(self, kode, nama, bagian_mata, kata_kunci, pengobatan, saran):
        # [ENKAPSULASI] Semua nilai lewat setter agar tervalidasi
        self.kode = kode
        self.nama = nama
        self.bagian_mata = bagian_mata
        self.kata_kunci = kata_kunci
        self.pengobatan = pengobatan
        self.saran = saran

    # ---------- [ENKAPSULASI] getter & setter ----------
    @property
    def kode(self):
        return self.__kode

    @kode.setter
    def kode(self, nilai):
        if nilai not in PenyakitMata.KODE_VALID:
            raise ValueError(f"Kode penyakit harus salah satu dari {PenyakitMata.KODE_VALID}, bukan '{nilai}'")
        self.__kode = nilai

    @property
    def nama(self):
        return self.__nama

    @nama.setter
    def nama(self, nilai):
        if not isinstance(nilai, str) or nilai.strip() == "":
            raise ValueError("Nama penyakit tidak boleh kosong")
        self.__nama = nilai

    @property
    def bagian_mata(self):
        return self.__bagian_mata

    @bagian_mata.setter
    def bagian_mata(self, nilai):
        if not isinstance(nilai, str) or nilai.strip() == "":
            raise ValueError("Bagian mata tidak boleh kosong")
        self.__bagian_mata = nilai

    @property
    def kata_kunci(self):
        return self.__kata_kunci

    @kata_kunci.setter
    def kata_kunci(self, nilai):
        # Aturan: list berisi teks (boleh kosong untuk class turunan yang
        # mengenali penyakit dengan cara lain, misalnya KelainanLain)
        if not isinstance(nilai, list):
            raise ValueError("Kata kunci harus berupa list")
        for kata in nilai:
            if not isinstance(kata, str) or kata.strip() == "":
                raise ValueError("Setiap kata kunci harus teks yang tidak kosong")
        self.__kata_kunci = nilai

    # Penanganan = informasi umum tentang penyakit (bukan data pasien dari CSV) dan BUKAN resep dokter.
    # Sumber: National Eye Institute (nei.nih.gov) dan American Academy of Ophthalmology (aao.org).
    @property
    def pengobatan(self):
        return list(self.__pengobatan)  # kirim salinan agar isi asli tidak diubah dari luar

    @pengobatan.setter
    def pengobatan(self, nilai):
        self.__pengobatan = self.__cek_daftar_teks(nilai, "Pengobatan")

    @property
    def saran(self):
        return list(self.__saran)

    @saran.setter
    def saran(self, nilai):
        self.__saran = self.__cek_daftar_teks(nilai, "Saran")

    def __cek_daftar_teks(self, nilai, nama):
        """Method private: nilai harus list berisi minimal satu teks yang tidak kosong."""
        if not isinstance(nilai, list) or len(nilai) == 0:
            raise ValueError(f"{nama} harus berupa list yang tidak kosong")
        for teks in nilai:
            if not isinstance(teks, str) or teks.strip() == "":
                raise ValueError(f"Setiap isi {nama.lower()} harus teks yang tidak kosong")
        return list(nilai)

    # ---------- Method ----------
    def ditemukan_di(self, pemeriksaan):
        """True jika salah satu kata kunci penyakit ini ada di diagnosis satu mata."""
        for kata in pemeriksaan.daftar_kata_kunci():
            for kunci in self.kata_kunci:
                if kunci in kata:
                    return True
        return False

    def mata_terdampak(self, mata_kiri, mata_kanan):
        """Mata yang terkena penyakit ini: kedua mata, mata kiri, atau mata kanan."""
        kiri = self.ditemukan_di(mata_kiri)
        kanan = self.ditemukan_di(mata_kanan)
        if kiri and kanan:
            return "kedua mata"
        if kiri:
            return "mata kiri"
        if kanan:
            return "mata kanan"
        return "tidak ada"

    def tampilkan_info(self, mata_kiri, mata_kanan):
        """Menampilkan nama penyakit dan mata yang terkena. Di-override class turunan."""
        print(f"  - {self.nama} ({self.bagian_mata}): {self.mata_terdampak(mata_kiri, mata_kanan)}")

    def penanganan(self, mata_kiri, mata_kanan):
        """Penanganan penyakit ini: (list pengobatan, list hal yang harus dilakukan).
        Di-override class turunan agar menyesuaikan kondisi mata pasien (tingkat, jenis, atau status)."""
        return self.pengobatan, self.saran

    def tampilkan_penanganan(self, mata_kiri, mata_kanan):
        """Menampilkan pengobatan dan hal yang harus dilakukan (informasi umum, bukan resep dokter)."""
        # [POLIMORFISME] self.penanganan() menjalankan versi milik class object ini
        pengobatan, saran = self.penanganan(mata_kiri, mata_kanan)
        print("      pengobatan:")
        for teks in pengobatan:
            print(f"        * {teks}")
        print("      yang harus dilakukan:")
        for teks in saran:
            print(f"        * {teks}")
