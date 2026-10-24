import inspect
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


def say(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Fonksiyonun kaç kez çağrıldığını 'cagri' niteliğinde sayar."""

    @wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        sarmalayici.cagri += 1
        return fonksiyon(*args, **kwargs)

    sarmalayici.cagri = 0
    return sarmalayici


def log_cagri(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Her çağrıdan önce ad ve argümanları, sonra dönüş değerini yazdırır."""

    @wraps(fonksiyon)
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        parcalar = [repr(arg) for arg in args]
        parcalar += [f"{ad}={deger!r}" for ad, deger in kwargs.items()]
        print(f"-> {fonksiyon.__name__}({', '.join(parcalar)})")
        sonuc = fonksiyon(*args, **kwargs)
        print(f"<- {fonksiyon.__name__} = {sonuc!r}")
        return sonuc

    return sarmalayici


def sinirla(
    alt: float, ust: float
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Dekore edilen fonksiyonun ilk argümanını [alt, ust] aralığıyla sınırlar.

    İlk argüman aralık dışındaysa anlamlı bir ValueError fırlatır.
    """

    def dekorator(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
        imza = inspect.signature(fonksiyon)

        @wraps(fonksiyon)
        def sarmalayici(*args: Any, **kwargs: Any) -> Any:
            bagli = imza.bind(*args, **kwargs)
            bagli.apply_defaults()
            deger = next(iter(bagli.arguments.values()))
            if not alt <= deger <= ust:
                raise ValueError(
                    f"{fonksiyon.__name__}: {deger} değeri "
                    f"{alt}-{ust} aralığında değil"
                )
            return fonksiyon(*args, **kwargs)

        return sarmalayici

    return dekorator


if __name__ == "__main__":
    from uzay_oyunu.akis import rota_sayisi_onbelleksiz
    from uzay_oyunu.oyun import galaksi_yukle

    @log_cagri
    def yolculuk(hedef, hiz=1):
        return f"{hedef} hiz={hiz}"

    yolculuk("orion", hiz=3)

    olculen = sure_olc(rota_sayisi_onbelleksiz)
    sonuc = olculen(galaksi_yukle()["baglantilar"], "dünya", 20)
    print(f"adim=20 için rota sayısı: {sonuc}")