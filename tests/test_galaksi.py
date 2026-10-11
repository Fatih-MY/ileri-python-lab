import json
from pathlib import Path

import pytest

from uzay_oyunu.oyun import galaksi_kur

JSON_YOLU = Path(__file__).parent.parent / "uzay_oyunu" / "galaksi.json"


def veriyi_oku() -> dict:
    with open(JSON_YOLU, encoding="utf-8") as dosya:
        return json.load(dosya)


def test_dosyadan_kurulum():
    g = galaksi_kur(**veriyi_oku())
    assert (g["konum"], g["yakit"]) == ("dünya", 100)


def test_varsayilan_yakit():
    assert galaksi_kur(["mars"], {"mars": []}, "mars")["yakit"] == 50


def test_baslangic_listede_yoksa_hata():
    with pytest.raises(ValueError):
        galaksi_kur(["mars"], {"mars": []}, "venüs")


def test_baglanti_sirasi_korunur():
    g = galaksi_kur(**veriyi_oku())
    assert g["baglantilar"]["dünya"] == ["centauri", "sirius"]
    assert g["baglantilar"]["sirius"] == ["dünya", "centauri", "orion"]