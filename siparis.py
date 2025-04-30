class Siparis:
    siparis_sayisi = 1

    def __init__(self, urun_ismi, miktar):
        self.order_id = Siparis.siparis_sayisi
        Siparis.siparis_sayisi += 1
        self.urun_ismi = urun_ismi
        self.miktar = miktar

    def __str__(self):
        return f"Sipariş #{self.order_id} - {self.urun_ismi} x {self.miktar}"