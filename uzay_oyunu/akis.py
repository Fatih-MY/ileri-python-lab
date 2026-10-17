from collections.abc import Iterable, Iterator
from pathlib import Path


def fibonacci() -> Iterator[int]:
    """Sonsuz fibonacci dizisini (0, 1, 1, 2, 3, ...) tembel olarak üretir."""
    onceki, simdiki = 0, 1
    while True:
        yield onceki
        onceki, simdiki = simdiki, onceki + simdiki


def yakit_gostergesi(yakit: int, tuketim: int) -> Iterator[int]:
    """Her next() çağrısında yakıtı tuketim kadar azaltıp kalanı üretir.

    Yakıt 0'a inince durur (StopIteration). tuketim pozitif olmalıdır.
    """
    if tuketim <= 0:
        raise ValueError("tuketim pozitif olmalı")
    while yakit > 0:
        yakit = max(yakit - tuketim, 0)
        yield yakit


def satirlari_oku(yol: str | Path) -> Iterator[str]:
    """Dosyayı satır satır okur, boş ve # ile başlayan satırları atlar."""
    with open(yol, encoding="utf-8") as dosya:
        for satir in dosya:
            satir = satir.strip()
            if not satir or satir.startswith("#"):
                continue
            yield satir


def ayristir(satirlar: Iterable[str]) -> Iterator[tuple[str, str, int]]:
    """'kaynak -> hedef yakit' satırlarından (kaynak, hedef, yakit) üretir."""
    for satir in satirlar:
        kaynak, _, hedef, yakit = satir.split()
        yield kaynak, hedef, int(yakit)


def uzun_yolculuklar(
    kayitlar: Iterable[tuple[str, str, int]], esik: int
) -> Iterator[tuple[str, str, int]]:
    """Yakıtı eşikten büyük olan kayıtları süzer."""
    for kayit in kayitlar:
        if kayit[2] > esik:
            yield kayit