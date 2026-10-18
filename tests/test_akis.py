from itertools import islice, takewhile
from pathlib import Path

import pytest

from uzay_oyunu.akis import (
    ayristir,
    fibonacci,
    rota_sayaci,
    rota_sayisi_onbelleksiz,
    satirlari_oku,
    uzun_yolculuklar,
    yakit_gostergesi,
)
from uzay_oyunu.istatistik import (
    adlari_buyut,
    adlari_buyut_mfr,
    cok_baglantilar,
    cok_baglantilar_mfr,
    hizli_yolculuk,
    toplam_baglanti,
    toplam_baglanti_mfr,
    yolculuk,
)
from uzay_oyunu.oyun import galaksi_kur, galaksi_yukle

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


def test_rota_sayilari():
    say = rota_sayaci(galaksi_yukle()["baglantilar"])
    assert say("dünya", 3) == 9
    assert say("dünya", 10) == 2185
    assert say("dünya", 40) == 16832258606399


def test_onbelleksiz_surum_ayni_sonucu_verir():
    baglantilar = galaksi_yukle()["baglantilar"]
    assert rota_sayisi_onbelleksiz(baglantilar, "dünya", 10) == 2185


def test_onbellek_gercekten_kullaniliyor():
    say = rota_sayaci(galaksi_yukle()["baglantilar"])
    say("dünya", 10)
    bilgi = say.cache_info()
    assert bilgi.hits > 0
    assert bilgi.misses == bilgi.currsize


def test_her_sayacin_kendi_onbellegi_var():
    baglantilar = galaksi_yukle()["baglantilar"]
    ilk = rota_sayaci(baglantilar)
    ilk("dünya", 5)
    ikinci = rota_sayaci(baglantilar)
    assert ikinci.cache_info().currsize == 0


def test_kucuk_haritalar():
    assert rota_sayaci({"a": ["b"], "b": ["a"]})("a", 5) == 1
    dallanan = rota_sayaci({"a": ["b", "c"], "b": [], "c": []})
    assert dallanan("a", 1) == 2
    assert dallanan("a", 2) == 0


def test_buyuk_harfli_adlar_iki_yolla():
    galaksi = galaksi_yukle()
    beklenen = ["DÜNYA", "CENTAURI", "SIRIUS", "ORION", "KARA_DELIK"]
    assert adlari_buyut_mfr(galaksi) == beklenen
    assert adlari_buyut(galaksi) == beklenen


def test_cok_baglantili_gezegenler_iki_yolla():
    galaksi = galaksi_yukle()
    beklenen = ["dünya", "centauri", "sirius", "orion"]
    assert cok_baglantilar_mfr(galaksi) == beklenen
    assert cok_baglantilar(galaksi) == beklenen


def test_toplam_baglanti_iki_yolla():
    galaksi = galaksi_yukle()
    assert toplam_baglanti_mfr(galaksi) == 10
    assert toplam_baglanti(galaksi) == 10


def test_istatistik_kucuk_galaksi():
    galaksi = galaksi_kur(
        ["a", "b", "c"], {"a": ["b", "c"], "b": ["a"], "c": []}, "a"
    )
    assert adlari_buyut(galaksi) == adlari_buyut_mfr(galaksi) == ["A", "B", "C"]
    assert cok_baglantilar(galaksi) == cok_baglantilar_mfr(galaksi) == ["a"]
    assert toplam_baglanti(galaksi) == toplam_baglanti_mfr(galaksi) == 3


def test_hizli_yolculuk_hizi_sabit():
    assert yolculuk(12) == 12.0
    assert hizli_yolculuk(12) == 4.0
    assert hizli_yolculuk.func is yolculuk
    assert hizli_yolculuk.keywords == {"hiz": 3}


def test_hizli_yolculuk_hiz_ezilebilir():
    assert hizli_yolculuk(12, hiz=6) == 2.0


def test_yolculuk_hizi_pozitif_olmali():
    with pytest.raises(ValueError):
        yolculuk(12, hiz=0)