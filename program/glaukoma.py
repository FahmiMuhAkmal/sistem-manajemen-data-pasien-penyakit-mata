# glaukoma.py
# [INHERITANCE] Glaukoma mewarisi PenyakitMata (kode G).
# Perilaku khusus: status() membedakan diagnosis pasti dan dugaan ("suspected glaucoma"),
# dan penanganan() membedakan pengobatan untuk keduanya.

from penyakit_mata import PenyakitMata


class Glaukoma(PenyakitMata):
    """Kerusakan saraf optik, sering berkaitan dengan tekanan bola mata."""

    # Penanganan umum (sumber: National Eye Institute & AAO), bukan resep dokter
    PENGOBATAN = ["obat tetes penurun tekanan bola mata (mis. prostaglandin, beta-blocker)",
                  "bila belum cukup: tindakan laser (misalnya SLT) atau operasi glaukoma"]
    SARAN = ["jika diberi obat tetes, pakai setiap hari dan jangan berhenti sendiri",
             "kontrol rutin: tekanan bola mata, saraf optik, dan lapang pandang",
             "kerusakan saraf optik tidak bisa pulih, jadi pengobatan dini penting"]

    def __init__(self):
        # [INHERITANCE] Constructor chaining dengan nilai khusus glaukoma
        super().__init__("G", "Glaukoma", "saraf optik", ["glaucoma"], Glaukoma.PENGOBATAN, Glaukoma.SARAN)

    # ---------- Method khusus Glaukoma ----------
    def status(self, pemeriksaan):
        """Status glaukoma di satu mata: pasti, dugaan, atau '-' jika tidak ada."""
        hasil = "-"
        for kata in pemeriksaan.daftar_kata_kunci():
            if "glaucoma" in kata:
                if "suspected" in kata and hasil == "-":
                    hasil = "dugaan"
                elif "suspected" not in kata:
                    hasil = "pasti"
        return hasil

    # ---------- [INHERITANCE] Method overriding ----------
    def tampilkan_info(self, mata_kiri, mata_kanan):
        """Override: tambahkan status diagnosis di setiap mata."""
        super().tampilkan_info(mata_kiri, mata_kanan)
        print(f"      status: kiri {self.status(mata_kiri)}, kanan {self.status(mata_kanan)}")

    def penanganan(self, mata_kiri, mata_kanan):
        """Override: glaukoma yang masih dugaan perlu dipastikan dulu sebelum diobati."""
        pengobatan, saran = super().penanganan(mata_kiri, mata_kanan)
        if "pasti" not in (self.status(mata_kiri), self.status(mata_kanan)):
            pengobatan = ["belum tentu perlu obat; perlu dipastikan dulu oleh dokter mata",
                          "pemeriksaan lanjutan: tekanan bola mata, lapang pandang, OCT saraf optik"]
        return pengobatan, saran
