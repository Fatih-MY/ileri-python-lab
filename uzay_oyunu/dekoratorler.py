import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def sure_olc(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Fonksiyonun çalışma süresini ölçüp 'ad: 0.0123 sn' biçiminde yazdırır.

    Fonksiyonun sonucunu değiştirmeden döndürür.
    """

    @wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        baslangic = time.perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        gecen = time.perf_counter() - baslangic
        print(f"{fonksiyon.__name__}: {gecen:.4f} sn")
        return sonuc

    return sarmalayici


if __name__ == "__main__":
    from uzay_oyunu.akis import rota_sayisi_onbelleksiz
    from uzay_oyunu.oyun import galaksi_yukle

    olculen = sure_olc(rota_sayisi_onbelleksiz)
    sonuc = olculen(galaksi_yukle()["baglantilar"], "dünya", 20)
    print(f"adim=20 için rota sayısı: {sonuc}")