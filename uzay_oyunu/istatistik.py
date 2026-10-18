from collections.abc import Callable
from functools import partial, reduce


def adlari_buyut_mfr(galaksi: dict) -> list[str]:
    """Gezegen adlarının büyük harfli listesi (map ile)."""
    return list(map(str.upper, galaksi["gezegenler"]))


def adlari_buyut(galaksi: dict) -> list[str]:
    """Gezegen adlarının büyük harfli listesi (liste üreteci ile)."""
    return [ad.upper() for ad in galaksi["gezegenler"]]


def cok_baglantilar_mfr(galaksi: dict, en_az: int = 2) -> list[str]:
    """En az en_az bağlantısı olan gezegenler (filter ile)."""
    baglantilar = galaksi["baglantilar"]
    return list(
        filter(
            lambda gezegen: len(baglantilar[gezegen]) >= en_az,
            galaksi["gezegenler"],
        )
    )


def cok_baglantilar(galaksi: dict, en_az: int = 2) -> list[str]:
    """En az en_az bağlantısı olan gezegenler (liste üreteci ile)."""
    baglantilar = galaksi["baglantilar"]
    return [g for g in galaksi["gezegenler"] if len(baglantilar[g]) >= en_az]


def toplam_baglanti_mfr(galaksi: dict) -> int:
    """Toplam bağlantı sayısı (reduce ile)."""
    return reduce(
        lambda toplam, hedefler: toplam + len(hedefler),
        galaksi["baglantilar"].values(),
        0,
    )


def toplam_baglanti(galaksi: dict) -> int:
    """Toplam bağlantı sayısı (sum ile)."""
    return sum(len(hedefler) for hedefler in galaksi["baglantilar"].values())


def yolculuk(mesafe: int, hiz: int = 1) -> float:
    """Verilen mesafeyi verilen hızla gitmek için gereken süreyi döndürür."""
    if hiz <= 0:
        raise ValueError("hiz pozitif olmalı")
    return mesafe / hiz


hizli_yolculuk: Callable[..., float] = partial(yolculuk, hiz=3)

# Okunaklılık yorumu: [BURAYA KENDİ GÖRÜŞÜNÜ YAZ, aşağıdaki taslak sadece örnek]
# Bence liste üreteci ve sum daha okunaklı, çünkü cümle gibi soldan sağa
# okunuyor ve ek bir lambda ya da list() sarmalayıcısı gerektirmiyor.
# map/filter'da lambda'yı ve list() dönüşümünü, reduce'ta ise iki parametreli
# lambda ile başlangıç değerini (0) ayrıca takip etmem gerekiyor.