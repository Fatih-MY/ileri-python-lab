from collections.abc import Callable
from typing import Any

Durum = dict[str, Any]
Komut = Callable[[Durum], str]

KOMUTLAR: dict[str, tuple[Komut, str]] = {}


def komut(ad: str, aciklama: str = "") -> Callable[[Komut], Komut]:
    """Fonksiyonu KOMUTLAR sözlüğüne (fonksiyon, aciklama) olarak kaydeder.

    Fonksiyonu değiştirmeden aynen döndürür. Aynı ad ikinci kez
    kullanılırsa tanım anında ValueError fırlatır.
    """

    def kaydet(fonksiyon: Komut) -> Komut:
        if ad in KOMUTLAR:
            raise ValueError(f"'{ad}' komutu zaten kayıtlı")
        KOMUTLAR[ad] = (fonksiyon, aciklama)
        return fonksiyon

    return kaydet


@komut("yardim", "komutları listeler")
def yardim(durum: Durum) -> str:
    """Kayıtlı komutları ve açıklamalarını alfabetik sırayla listeler."""
    satirlar = [f"{ad} {KOMUTLAR[ad][1]}" for ad in sorted(KOMUTLAR)]
    return "\n".join(satirlar)


@komut("envanter", "eşyalarını gösterir")
def envanter(durum: Durum) -> str:
    """Oyuncunun eşyalarını gösterir."""
    # Döngüsel içe aktarmayı önlemek için burada içe aktarılır.
    from uzay_oyunu.oyun import envanter_metni

    metin = envanter_metni(durum["credits"], durum["engines"], durum["copilot"])
    return metin or "Envanterin boş."


@komut("harita", "gidebileceğin gezegenleri gösterir")
def harita(durum: Durum) -> str:
    """Bulunulan gezegenden gidilebilecek gezegenleri gösterir."""
    return ", ".join(durum["baglantilar"][durum["konum"]])