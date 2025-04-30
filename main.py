import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from urun import Urun
from stok import Stok
from siparis import Siparis

class StokTakipUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Stok Takip Sistemi")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Stok ve sipariş verilerini oluştur
        self.stok = Stok()
        self.tum_siparisler = []
        
        # Ana çerçeve oluştur
        self.ana_cerceve = ttk.Frame(root, padding=10)
        self.ana_cerceve.pack(fill=tk.BOTH, expand=True)
        
        # Uygulama başlığı
        baslik = ttk.Label(self.ana_cerceve, text="STOK TAKİP SİSTEMİ", font=("Arial", 16, "bold"))
        baslik.pack(pady=10)
        
        # Ürün ekle çerçevesi
        self.urun_ekle_cerceve = ttk.LabelFrame(self.ana_cerceve, text="Ürün Ekle")
        self.urun_ekle_cerceve.pack(fill=tk.X, pady=10)
        
        # Ürün adı girişi
        ttk.Label(self.urun_ekle_cerceve, text="Ürün Adı:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.urun_adi_var = tk.StringVar()
        ttk.Entry(self.urun_ekle_cerceve, textvariable=self.urun_adi_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        # Ürün miktarı girişi
        ttk.Label(self.urun_ekle_cerceve, text="Miktar:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.miktar_var = tk.StringVar()
        ttk.Entry(self.urun_ekle_cerceve, textvariable=self.miktar_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        # Ürün ekle butonu
        ttk.Button(self.urun_ekle_cerceve, text="Ürün Ekle", command=self.urun_ekle).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Butonlar çerçevesi
        butonlar_cerceve = ttk.Frame(self.ana_cerceve)
        butonlar_cerceve.pack(fill=tk.X, pady=10)
        
        # İşlem butonları
        ttk.Button(butonlar_cerceve, text="Stok Durumunu Göster", command=self.stok_durumu_goster, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(butonlar_cerceve, text="Sipariş Ver", command=self.siparis_ver, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(butonlar_cerceve, text="Siparişleri Görüntüle", command=self.siparisleri_goruntule, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(butonlar_cerceve, text="Ürün Sil", command=self.urun_silme_penceresi, width=20).pack(side=tk.LEFT, padx=5)
        
        # Stok listesi çerçevesi
        stok_liste_cerceve = ttk.LabelFrame(self.ana_cerceve, text="Stok Listesi")
        stok_liste_cerceve.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Stok listesi için Treeview widget
        self.stok_listesi = ttk.Treeview(stok_liste_cerceve, columns=("Ürün Adı", "Stok Miktarı"), show="headings")
        self.stok_listesi.heading("Ürün Adı", text="Ürün Adı")
        self.stok_listesi.heading("Stok Miktarı", text="Stok Miktarı")
        self.stok_listesi.column("Ürün Adı", width=400)
        self.stok_listesi.column("Stok Miktarı", width=100)
        self.stok_listesi.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Stok listesi için scrollbar
        scrollbar = ttk.Scrollbar(stok_liste_cerceve, orient=tk.VERTICAL, command=self.stok_listesi.yview)
        self.stok_listesi.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Stok listesi için sağ tık menüsü
        self.stok_menu = tk.Menu(self.root, tearoff=0)
        self.stok_menu.add_command(label="Ürünü Sil", command=self.urun_sil)
        
        # Sağ tık menüsü için binding
        self.stok_listesi.bind("<Button-3>", self.show_stok_menu)
        
        # Durum çubuğu
        self.durum_cubugu = ttk.Label(self.ana_cerceve, text="Hazır", relief=tk.SUNKEN, anchor=tk.W)
        self.durum_cubugu.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        # Tema ve stil ayarları
        self.apply_style()
        
        # Başlangıçta stok listesini güncelle
        self.stok_listesini_guncelle()
    
    def apply_style(self):
        """Uygulama stilini ayarlar"""
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10))
        style.configure("TLabelframe.Label", font=("Arial", 10, "bold"))
        
    def urun_ekle(self):
        """Ürün ekleme işlemini gerçekleştirir"""
        try:
            urun_adi = self.urun_adi_var.get().strip()
            miktar = int(self.miktar_var.get().strip())
            
            if not urun_adi:
                messagebox.showerror("Hata", "Ürün adı boş olamaz!")
                return
                
            if miktar <= 0:
                messagebox.showerror("Hata", "Miktar pozitif olmalıdır!")
                return
                
            yeni_urun = Urun(urun_adi, miktar)
            self.stok.urun_ekle(yeni_urun)
            
            # Giriş alanlarını temizle
            self.urun_adi_var.set("")
            self.miktar_var.set("")
            
            self.durum_cubugu.config(text=f"{urun_adi} ürünü başarıyla eklendi.")
            
            # Stok listesini güncelle
            self.stok_listesini_guncelle()
            
        except ValueError:
            messagebox.showerror("Hata", "Miktar sayısal bir değer olmalıdır!")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
    
    def stok_listesini_guncelle(self):
        """Stok listesi görüntüsünü günceller"""
        # Mevcut öğeleri temizle
        for item in self.stok_listesi.get_children():
            self.stok_listesi.delete(item)
            
        # Ürünleri listele
        for urun_adi, urun in self.stok.urunler.items():
            self.stok_listesi.insert("", tk.END, values=(urun.ad, urun.miktar))
    
    def stok_durumu_goster(self):
        """Stok durumunu gösteren pencereyi açar"""
        stok_pencere = tk.Toplevel(self.root)
        stok_pencere.title("Stok Durumu")
        stok_pencere.geometry("400x300")
        
        # Başlık
        ttk.Label(stok_pencere, text="MEVCUT STOK DURUMU", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Stok listesi için frame
        liste_frame = ttk.Frame(stok_pencere)
        liste_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview widget
        stok_tree = ttk.Treeview(liste_frame, columns=("Ürün Adı", "Stok Miktarı"), show="headings")
        stok_tree.heading("Ürün Adı", text="Ürün Adı")
        stok_tree.heading("Stok Miktarı", text="Stok Miktarı")
        stok_tree.column("Ürün Adı", width=200)
        stok_tree.column("Stok Miktarı", width=100)
        stok_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(liste_frame, orient=tk.VERTICAL, command=stok_tree.yview)
        stok_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Ürünleri listele
        for urun_adi, urun in self.stok.urunler.items():
            stok_tree.insert("", tk.END, values=(urun.ad, urun.miktar))
        
        ttk.Button(stok_pencere, text="Kapat", command=stok_pencere.destroy).pack(pady=10)
        
        self.durum_cubugu.config(text="Stok durumu görüntülendi.")
    
    def siparis_ver(self):
        """Sipariş verme işlemini gerçekleştirir"""
        # Sipariş penceresini aç
        siparis_pencere = tk.Toplevel(self.root)
        siparis_pencere.title("Sipariş Ver")
        siparis_pencere.geometry("400x300")
        
        # Başlık
        ttk.Label(siparis_pencere, text="SİPARİŞ VERME EKRANI", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Sipariş formu
        form_frame = ttk.Frame(siparis_pencere)
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(form_frame, text="Ürün Adı:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        urun_combo = ttk.Combobox(form_frame, width=25)
        urun_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Combobox'a ürünleri ekle
        urun_listesi = list(self.stok.urunler.keys())
        urun_combo['values'] = urun_listesi
        if urun_listesi:
            urun_combo.current(0)
        
        ttk.Label(form_frame, text="Sipariş Miktarı:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        miktar_entry = ttk.Entry(form_frame, width=25)
        miktar_entry.grid(row=1, column=1, padx=5, pady=5)
        miktar_entry.insert(0, "1")
        
        # Sipariş onay fonksiyonu
        def siparisi_onayla():
            try:
                secilen_urun = urun_combo.get()
                miktar = int(miktar_entry.get())
                
                if not secilen_urun:
                    messagebox.showerror("Hata", "Lütfen bir ürün seçin!")
                    return
                    
                if miktar <= 0:
                    messagebox.showerror("Hata", "Sipariş miktarı pozitif olmalıdır!")
                    return
                
                urun = self.stok.urun_getir(secilen_urun)
                
                if urun is None:
                    messagebox.showerror("Hata", "Ürün bulunamadı!")
                    return
                    
                if urun.miktar < miktar:
                    messagebox.showerror("Hata", f"Yetersiz stok! Mevcut stok: {urun.miktar}")
                    return
                
                # Siparişi oluştur ve stok güncelle
                urun.stok_guncelle(-miktar)
                yeni_siparis = Siparis(secilen_urun, miktar)
                self.tum_siparisler.append(yeni_siparis)
                
                # Bilgi mesajı göster ve pencereyi kapat
                messagebox.showinfo("Başarılı", f"Sipariş oluşturuldu: {yeni_siparis}")
                siparis_pencere.destroy()
                
                # Ana penceredeki stok listesini güncelle
                self.stok_listesini_guncelle()
                self.durum_cubugu.config(text=f"{secilen_urun} için sipariş verildi.")
                
            except ValueError:
                messagebox.showerror("Hata", "Miktar sayısal bir değer olmalıdır!")
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
        
        # Butonlar
        buton_frame = ttk.Frame(siparis_pencere)
        buton_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(buton_frame, text="Siparişi Onayla", command=siparisi_onayla).pack(side=tk.LEFT, padx=5)
        ttk.Button(buton_frame, text="İptal", command=siparis_pencere.destroy).pack(side=tk.RIGHT, padx=5)
    
    def show_stok_menu(self, event):
        """Stok listesinde sağ tıklama menüsünü gösterir"""
        # Fare tıklaması konumundaki öğeyi belirle
        item = self.stok_listesi.identify_row(event.y)
        if item:
            # Öğeyi seç
            self.stok_listesi.selection_set(item)
            # Menüyü göster
            self.stok_menu.post(event.x_root, event.y_root)
            
    def urun_sil(self):
        """Seçili ürünü siler"""
        secili = self.stok_listesi.selection()
        if not secili:
            messagebox.showinfo("Bilgi", "Silmek için bir ürün seçin.")
            return
            
        secili_urun = self.stok_listesi.item(secili)["values"]
        urun_adi = secili_urun[0]
        
        # Silme işlemini onayla
        onay = messagebox.askyesno("Onay", f"{urun_adi} ürününü silmek istediğinize emin misiniz?")
        if onay:
            # Ürünü sil
            if self.stok.urun_sil(urun_adi):
                self.stok_listesi.delete(secili)
                messagebox.showinfo("Bilgi", f"{urun_adi} ürünü başarıyla silindi.")
                self.durum_cubugu.config(text=f"{urun_adi} ürünü silindi.")
            else:
                messagebox.showerror("Hata", "Ürün silinirken bir hata oluştu.")
                
    def urun_silme_penceresi(self):
        """Ürün silme penceresini açar"""
        if not self.stok.urunler:
            messagebox.showinfo("Bilgi", "Silinecek ürün bulunmamaktadır.")
            return
            
        silme_pencere = tk.Toplevel(self.root)
        silme_pencere.title("Ürün Sil")
        silme_pencere.geometry("400x300")
        
        # Başlık
        ttk.Label(silme_pencere, text="ÜRÜN SİLME EKRANI", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Listbox yerine Combobox kullanarak ürün seçimi
        ttk.Label(silme_pencere, text="Silinecek Ürün:").pack(pady=5)
        
        urun_combo = ttk.Combobox(silme_pencere, width=30)
        urun_combo["values"] = list(self.stok.urunler.keys())
        urun_combo.pack(pady=10)
        
        if urun_combo["values"]:
            urun_combo.current(0)
            
        # Silme işlemi
        def sil():
            urun_adi = urun_combo.get()
            if not urun_adi:
                messagebox.showinfo("Bilgi", "Lütfen bir ürün seçin.")
                return
                
            # Silme işlemini onayla
            onay = messagebox.askyesno("Onay", f"{urun_adi} ürününü silmek istediğinize emin misiniz?")
            if onay:
                # Ürünü sil
                if self.stok.urun_sil(urun_adi):
                    # Combobox'tan ürünü kaldır
                    yeni_urunler = list(self.stok.urunler.keys())
                    urun_combo["values"] = yeni_urunler
                    if yeni_urunler:
                        urun_combo.current(0)
                    else:
                        urun_combo.set("")
                    
                    # Stok listesini güncelle
                    self.stok_listesini_guncelle()
                    
                    messagebox.showinfo("Bilgi", f"{urun_adi} ürünü başarıyla silindi.")
                    self.durum_cubugu.config(text=f"{urun_adi} ürünü silindi.")
                else:
                    messagebox.showerror("Hata", "Ürün silinirken bir hata oluştu.")
        
        # Butonlar
        buton_frame = ttk.Frame(silme_pencere)
        buton_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(buton_frame, text="Sil", command=sil).pack(side=tk.LEFT, padx=10)
        ttk.Button(buton_frame, text="İptal", command=silme_pencere.destroy).pack(side=tk.RIGHT, padx=10)
    
    def siparisleri_goruntule(self):
        """Siparişleri görüntüleyen pencereyi açar"""
        if not self.tum_siparisler:
            messagebox.showinfo("Bilgi", "Henüz sipariş bulunmamaktadır.")
            return
            
        siparis_pencere = tk.Toplevel(self.root)
        siparis_pencere.title("Siparişler")
        siparis_pencere.geometry("500x400")
        
        # Başlık
        ttk.Label(siparis_pencere, text="SİPARİŞ LİSTESİ", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Sipariş listesi için frame
        liste_frame = ttk.Frame(siparis_pencere)
        liste_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview widget
        siparis_tree = ttk.Treeview(liste_frame, columns=("Sipariş No", "Ürün Adı", "Miktar"), show="headings")
        siparis_tree.heading("Sipariş No", text="Sipariş No")
        siparis_tree.heading("Ürün Adı", text="Ürün Adı")
        siparis_tree.heading("Miktar", text="Miktar")
        siparis_tree.column("Sipariş No", width=100)
        siparis_tree.column("Ürün Adı", width=200)
        siparis_tree.column("Miktar", width=100)
        siparis_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(liste_frame, orient=tk.VERTICAL, command=siparis_tree.yview)
        siparis_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Siparişleri listele
        for siparis in self.tum_siparisler:
            siparis_tree.insert("", tk.END, values=(f"#{siparis.order_id}", siparis.urun_ismi, siparis.miktar))
            
        # Sipariş silme butonu ve fonksiyonu
        def siparis_sil():
            secili = siparis_tree.selection()
            if not secili:
                messagebox.showinfo("Bilgi", "Silmek için bir sipariş seçin.")
                return
                
            secili_siparis = siparis_tree.item(secili)["values"]
            siparis_id = int(secili_siparis[0].replace("#", ""))
            
            # Seçilen siparişi bul ve sil
            for i, siparis in enumerate(self.tum_siparisler):
                if siparis.order_id == siparis_id:
                    # Siparişi silmeden önce onay iste
                    onay = messagebox.askyesno("Onay", f"Sipariş #{siparis.order_id} silinecek. Onaylıyor musunuz?")
                    if onay:
                        del self.tum_siparisler[i]
                        siparis_tree.delete(secili)
                        messagebox.showinfo("Bilgi", f"Sipariş #{siparis_id} silindi.")
                        self.durum_cubugu.config(text=f"Sipariş #{siparis_id} silindi.")
                    break
        
        # Butonlar için frame
        buton_frame = ttk.Frame(siparis_pencere)
        buton_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buton_frame, text="Siparişi Sil", command=siparis_sil).pack(side=tk.LEFT, padx=10)
        ttk.Button(buton_frame, text="Kapat", command=siparis_pencere.destroy).pack(side=tk.RIGHT, padx=10)
        
        self.durum_cubugu.config(text="Siparişler görüntülendi.")

def main():
    root = tk.Tk()
    app = StokTakipUygulamasi(root)
    root.mainloop()

if __name__ == "__main__":
    main()