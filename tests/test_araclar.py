import json
from pathlib import Path

from uzay_oyunu.araclar import en_bagli_gezegenler, hamle_sayaci
from uzay_oyunu.oyun import galaksi_kur

JSON_YOLU = Path(__file__).parent.parent / "uzay_oyunu" / "galaksi.json"


def galaksiyi_kur():
    with open(JSON_YOLU, encoding="utf-8") as dosya:
        return galaksi_kur(**json.load(dosya))


def test_sayac_her_cagrida_artar():
    sayac = hamle_sayaci()
    assert [sayac(), sayac(), sayac()] == [1, 2, 3]


def test_sayaclar_birbirinden_bagimsiz():
    a = hamle_sayaci()
    b = hamle_sayaci()
    a()
    a()
    assert b() == 1
    assert a() == 3


def test_en_bagli_gezegenler():
    g = galaksiyi_kur()
    assert en_bagli_gezegenler(g) == [
        "sirius", "centauri", "dünya", "orion", "kara_delik"
    ]


def test_esitlikte_alfabetik_sira():
    g = galaksi_kur(["b", "a", "c"], {"a": ["b"], "b": ["a"], "c": []}, "a")
    assert en_bagli_gezegenler(g) == ["a", "b", "c"]