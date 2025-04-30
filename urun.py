class Urun:
    def __init__(self, ad, miktar):
        self.ad = ad
        self.miktar = miktar

    def stok_guncelle(self, adet):
        self.miktar += adet

    def __str__(self):
        return f"{self.ad} - Stok: {self.miktar}"