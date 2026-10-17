from itertools import islice, takewhile
from pathlib import Path

import pytest

from uzay_oyunu.akis import (
    ayristir,
    fibonacci,
    satirlari_oku,
    uzun_yolculuklar,
    yakit_gostergesi,
)

SEYIR = Path(__file__).parent.parent / "veri" / "seyir.txt"


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


def test_satirlari_oku_bos_ve_yorum_satirlarini_atlar(tmp_path):
    dosya = tmp_path / "deneme.txt"
    dosya.write_text("a -> b 1\n\n# yorum\nb -> c 2\n", encoding="utf-8")
    assert list(satirlari_oku(dosya)) == ["a -> b 1", "b -> c 2"]


def test_ayristir_demet_uretir():
    kayitlar = list(ayristir(["dünya -> sirius 12"]))
    assert kayitlar == [("dünya", "sirius", 12)]


def test_toplam_yakit():
    kayitlar = ayristir(satirlari_oku(SEYIR))
    assert sum(y for _, _, y in kayitlar) == 88


def test_uzun_yolculuklar():
    kayitlar = ayristir(satirlari_oku(SEYIR))
    hedefler = [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)]
    assert hedefler == ["sirius", "centauri", "orion", "kara_delik"]


def test_boru_hatti_tembel_calisir():
    okunan = []

    def kaynak():
        for satir in ["a -> b 1", "b -> c 2", "c -> d 3"]:
            okunan.append(satir)
            yield satir

    hat = ayristir(kaynak())
    assert next(hat) == ("a", "b", 1)
    assert okunan == ["a -> b 1"]


def test_boru_hatti_tek_kullanimlik():
    kayitlar = ayristir(satirlari_oku(SEYIR))
    assert sum(y for _, _, y in kayitlar) == 88
    assert list(kayitlar) == []