from collections.abc import Iterator


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