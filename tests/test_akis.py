from itertools import islice, takewhile

import pytest

from uzay_oyunu.akis import fibonacci, yakit_gostergesi


def test_next_ile_ilk_uc_deger():
    g = fibonacci()
    assert (next(g), next(g), next(g)) == (0, 1, 1)


def test_islice_ile_ilk_12_deger():
    assert list(islice(fibonacci(), 12)) == [
        0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
    ]


def test_takewhile_ile_100den_kucukler():
    kucukler = list(takewhile(lambda x: x < 100, fibonacci()))
    assert kucukler == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]


def test_uretec_tek_kullanimliktir():
    g = fibonacci()
    ilk = list(islice(g, 5))
    ikinci = list(islice(g, 5))
    assert ilk == [0, 1, 1, 2, 3]
    assert ikinci == [5, 8, 13, 21, 34]
    assert ilk != ikinci

    def test_yakit_gostergesi_listesi():
    assert list(yakit_gostergesi(100, 30)) == [70, 40, 10, 0]


def test_yakit_gostergesi_tam_bolunen():
    assert list(yakit_gostergesi(100, 50)) == [50, 0]


def test_yakit_bitince_stopiteration():
    g = yakit_gostergesi(10, 5)
    assert next(g) == 5
    assert next(g) == 0
    with pytest.raises(StopIteration):
        next(g)


def test_yakit_gostergesi_tek_kullanimlik():
    g = yakit_gostergesi(100, 30)
    assert list(g) == [70, 40, 10, 0]
    assert list(g) == []


def test_tuketim_sifir_olamaz():
    with pytest.raises(ValueError):
        next(yakit_gostergesi(100, 0))