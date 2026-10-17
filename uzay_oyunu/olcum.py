import time

from uzay_oyunu.akis import rota_sayaci, rota_sayisi_onbelleksiz
from uzay_oyunu.oyun import galaksi_yukle


def olc() -> None:
    """Önbelleksiz ve önbellekli rota sayacının adim=20 süresini karşılaştırır."""
    baglantilar = galaksi_yukle()["baglantilar"]

    baslangic = time.perf_counter()
    sonuc_1 = rota_sayisi_onbelleksiz(baglantilar, "dünya", 20)
    onbelleksiz = time.perf_counter() - baslangic

    say = rota_sayaci(baglantilar)
    baslangic = time.perf_counter()
    sonuc_2 = say("dünya", 20)
    onbellekli = time.perf_counter() - baslangic

    print(f"Önbelleksiz : {onbelleksiz:.6f} saniye (sonuç {sonuc_1})")
    print(f"Önbellekli  : {onbellekli:.6f} saniye (sonuç {sonuc_2})")
    print(say.cache_info())


if __name__ == "__main__":
    olc()