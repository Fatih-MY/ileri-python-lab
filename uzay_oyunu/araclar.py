from collections.abc import Callable


def hamle_sayaci() -> Callable[[], int]:
    """Her çağrıldığında bir artan sayı döndüren sayaç fonksiyonu üretir."""
    sayi = 0

    def say() -> int:
        nonlocal sayi
        sayi += 1
        return sayi

    return say


def en_bagli_gezegenler(galaksi: dict) -> list[str]:
    """Gezegenleri bağlantı sayısına göre azalan, eşitlikte alfabetik sıralar."""
    baglantilar = galaksi["baglantilar"]
    return sorted(
        galaksi["gezegenler"],
        key=lambda gezegen: (-len(baglantilar[gezegen]), gezegen),
    )