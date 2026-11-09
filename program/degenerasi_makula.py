# degenerasi_makula.py
# [INHERITANCE] DegenerasiMakula mewarisi PenyakitMata (kode A, age-related
# macular degeneration / AMD). Perilaku khusus: jenis() membedakan AMD kering dan basah,
# dan penanganan() menyesuaikan pengobatan dengan jenis tersebut.

from penyakit_mata import PenyakitMata


class DegenerasiMakula(PenyakitMata):
    """Kerusakan makula (pusat retina) yang berkaitan dengan usia."""

    # Penanganan umum (sumber: National Eye Institute & AAO), bukan resep dokter
    PENGOBATAN = ["AMD basah: suntikan obat anti-VEGF ke dalam mata",
                  "AMD kering tahap awal: belum ada obat, cukup dipantau dokter mata",
                  "AMD kering tahap menengah: suplemen vitamin & mineral formula AREDS2"]
    SARAN = ["berhenti merokok, rutin berolahraga, makan sayuran hijau dan ikan",
             "pantau penglihatan sendiri dengan kisi Amsler (Amsler grid)",
             "segera ke dokter mata bila garis lurus tampak bergelombang"]

    def __init__(self):
        # [INHERITANCE] Constructor chaining dengan nilai khusus degenerasi makula
        super().__init__("A", "Degenerasi makula", "makula (pusat retina)",
                         ["age-related macular degeneration"],
                         DegenerasiMakula.PENGOBATAN, DegenerasiMakula.SARAN)

    # ---------- Method khusus DegenerasiMakula ----------
    def jenis(self, pemeriksaan):
        """Jenis AMD di satu mata: kering (dry) atau basah (wet)."""
        if not self.ditemukan_di(pemeriksaan):
            return "-"
        for kata in pemeriksaan.daftar_kata_kunci():
            if "wet age-related macular degeneration" in kata:
                return "basah"
            if "dry age-related macular degeneration" in kata:
                return "kering"
        return "tidak disebutkan"

    # ---------- [INHERITANCE] Method overriding ----------
    def tampilkan_info(self, mata_kiri, mata_kanan):
        """Override: tambahkan jenis AMD di setiap mata."""
        super().tampilkan_info(mata_kiri, mata_kanan)
        print(f"      jenis: kiri {self.jenis(mata_kiri)}, kanan {self.jenis(mata_kanan)}")

    def penanganan(self, mata_kiri, mata_kanan):
        """Override: AMD basah dan AMD kering ditangani berbeda (bisa keduanya jika tiap mata berbeda)."""
        pengobatan, saran = super().penanganan(mata_kiri, mata_kanan)
        jenis_pasien = (self.jenis(mata_kiri), self.jenis(mata_kanan))
        pengobatan_khusus = []
        if "basah" in jenis_pasien:
            pengobatan_khusus.append("AMD basah: suntikan anti-VEGF ke dalam mata secara berkala, jangan ditunda")
        if "kering" in jenis_pasien:
            pengobatan_khusus.append("AMD kering: belum ada obat; tahap menengah dibantu suplemen AREDS2")
        if len(pengobatan_khusus) > 0:
            pengobatan = pengobatan_khusus
        return pengobatan, saran
