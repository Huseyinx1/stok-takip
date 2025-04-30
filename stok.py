class Stok:
    def __init__(self):
        self.urunler = {}
        
    def urun_ekle(self, urun):
        if urun.ad in self.urunler:
            self.urunler[urun.ad].stok_guncelle(urun.miktar)
        else:
            self.urunler[urun.ad] = urun
            
    def stok_guncelle(self, urun_adi, adet):
        if urun_adi in self.urunler:
            self.urunler[urun_adi].stok_guncelle(adet)
        else:
            print("Ürün bulunamadı.")
            
    def urun_sil(self, urun_adi):
        if urun_adi in self.urunler:
            del self.urunler[urun_adi]
            return True
        return False
            
    def stok_goster(self):
        for urun in self.urunler.values():
            print(urun)
            
    def urun_getir(self, urun_adi):
        return self.urunler.get(urun_adi, None)