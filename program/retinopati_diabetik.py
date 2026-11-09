# retinopati_diabetik.py
# [INHERITANCE] RetinopatiDiabetik mewarisi PenyakitMata (kode D).
# Perilaku khusus: tingkat_keparahan() membaca tingkat retinopati di setiap mata
# dari kata kunci dokter (ringan, sedang, berat, proliferatif), dan penanganan()
# menyesuaikan pengobatan dengan tingkat yang paling berat.

from penyakit_mata import PenyakitMata


class RetinopatiDiabetik(PenyakitMata):
    """Kerusakan pembuluh darah retina akibat diabetes."""

    # Urutan dari yang paling berat: (kata kunci di data, nama tingkat)
    TINGKAT = (
        ("proliferative diabetic retinopathy", "proliferatif"),
        ("severe nonproliferative retinopathy", "berat"),
        ("moderate non proliferative retinopathy", "sedang"),
        ("mild nonproliferative retinopathy", "ringan"),
    )
    # Penanganan umum (sumber: National Eye Institute & AAO), bukan resep dokter
    PENGOBATAN = ["tahap awal: belum perlu tindakan, retina cukup dipantau dokter mata",
                  "tahap lanjut: suntikan obat anti-VEGF, laser retina, atau operasi vitrektomi"]
    SARAN = ["kontrol gula darah (cek HbA1c), tekanan darah, dan kolesterol",
             "periksa retina dengan pupil dilebarkan minimal setahun sekali",
             "segera ke dokter mata bila muncul bintik hitam atau penglihatan kabur"]
    # Pengobatan menurut tingkat yang paling berat di mata pasien
    PENGOBATAN_PER_TINGKAT = {
        "proliferatif": ["perlu penanganan segera oleh dokter mata spesialis retina",
                         "laser panretina (PRP), suntikan anti-VEGF, atau operasi vitrektomi"],
        "berat": ["perlu diperiksa dokter mata spesialis retina",
                  "dapat dipertimbangkan laser panretina (PRP) atau suntikan anti-VEGF"],
        "sedang": ["biasanya belum perlu tindakan, tetapi retina diperiksa lebih sering",
                   "suntikan anti-VEGF atau laser bila makula membengkak (edema makula)"],
        "ringan": ["belum perlu obat atau tindakan pada mata, cukup dipantau"],
    }

    def __init__(self):
        # [INHERITANCE] Constructor chaining dengan nilai khusus retinopati diabetik
        super().__init__("D", "Retinopati diabetik", "retina",
                         ["nonproliferative retinopathy", "non proliferative retinopathy",
                          "proliferative diabetic retinopathy", "diabetic retinopathy"],
                         RetinopatiDiabetik.PENGOBATAN, RetinopatiDiabetik.SARAN)

    # ---------- Method khusus RetinopatiDiabetik ----------
    def tingkat_keparahan(self, pemeriksaan):
        """Tingkat retinopati diabetik di satu mata (dicari dari yang paling berat)."""
        if not self.ditemukan_di(pemeriksaan):
            return "-"
        for kunci, tingkat in RetinopatiDiabetik.TINGKAT:
            for kata in pemeriksaan.daftar_kata_kunci():
                if kunci in kata:
                    return tingkat
        return "tidak disebutkan"

    # ---------- [INHERITANCE] Method overriding ----------
    def tampilkan_info(self, mata_kiri, mata_kanan):
        """Override: tambahkan tingkat keparahan di setiap mata."""
        super().tampilkan_info(mata_kiri, mata_kanan)
        print(f"      tingkat: kiri {self.tingkat_keparahan(mata_kiri)}, "
              f"kanan {self.tingkat_keparahan(mata_kanan)}")

    def penanganan(self, mata_kiri, mata_kanan):
        """Override: pengobatan disesuaikan dengan tingkat yang paling berat di kedua mata."""
        pengobatan, saran = super().penanganan(mata_kiri, mata_kanan)
        tingkat_pasien = (self.tingkat_keparahan(mata_kiri), self.tingkat_keparahan(mata_kanan))
        for _, tingkat in RetinopatiDiabetik.TINGKAT:  # dicek dari yang paling berat
            if tingkat in tingkat_pasien:
                return list(RetinopatiDiabetik.PENGOBATAN_PER_TINGKAT[tingkat]), saran
        return pengobatan, saran  # tingkat tidak disebutkan dokter: pakai penanganan umum
