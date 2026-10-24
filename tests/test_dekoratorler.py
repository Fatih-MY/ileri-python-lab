import re

import pytest

from uzay_oyunu.akis import rota_sayisi_onbelleksiz
from uzay_oyunu.dekoratorler import log_cagri, say, sinirla, sure_olc
from uzay_oyunu.fib_deney import fib_cache_ustte, fib_say_ustte, fib_yalniz_say
from uzay_oyunu.oyun import galaksi_kur, galaksi_yukle, hedef_menusu
from uzay_oyunu.yakit import yakit_harca


def test_sonuc_degismeden_doner():
    @sure_olc
    def topla(a, b):
        return a + b

    assert topla(2, 3) == 5


def test_adli_argumanlarla_cagri_calisir():
    @sure_olc
    def selamla(ad, selam="Merhaba"):
        return f"{selam} {ad}"

    assert selamla(ad="Ayşe", selam="Selam") == "Selam Ayşe"
    assert selamla("Ali") == "Merhaba Ali"


def test_ad_ve_belge_korunur():
    @sure_olc
    def ornek():
        """Örnek belge."""
        return 1

    assert ornek.__name__ == "ornek"
    assert ornek.__doc__ == "Örnek belge."


def test_sure_belirtilen_bicimde_yazdirilir(capsys):
    @sure_olc
    def bos():
        return None

    bos()
    cikti = capsys.readouterr().out
    assert re.fullmatch(r"bos: \d+\.\d{4} sn\n", cikti)


def test_onbelleksiz_rota_sayacina_uygulanir(capsys):
    olculen = sure_olc(rota_sayisi_onbelleksiz)
    baglantilar = galaksi_yukle()["baglantilar"]
    capsys.readouterr()
    assert olculen(baglantilar, "dünya", 10) == 2185
    cikti = capsys.readouterr().out
    assert cikti.startswith("rota_sayisi_onbelleksiz: ")
    assert cikti.count("\n") == 1


def test_say_cagrilari_sayar():
    @say
    def topla(a, b):
        return a + b

    assert topla.cagri == 0
    assert topla(1, 2) == 3
    assert topla(a=3, b=4) == 7
    assert topla.cagri == 2


def test_say_ad_ve_belgeyi_korur():
    @say
    def ornek():
        """Örnek belge."""
        return 1

    assert ornek.__name__ == "ornek"
    assert ornek.__doc__ == "Örnek belge."


def test_her_fonksiyonun_kendi_sayaci_var():
    @say
    def bir():
        return 1

    @say
    def iki():
        return 2

    bir()
    bir()
    iki()
    assert (bir.cagri, iki.cagri) == (2, 1)


def test_fib_yalnizca_say():
    fib = fib_yalniz_say()
    assert fib(20) == 6765
    assert fib.cagri == 21891


def test_fib_say_ustte_lru_cache_altta():
    fib = fib_say_ustte()
    assert fib(20) == 6765
    assert fib.cagri == 39


def test_fib_lru_cache_ustte_say_altta():
    fib = fib_cache_ustte()
    assert fib(20) == 6765
    assert fib.__wrapped__.cagri == 21
    # wraps, sayacın yalnızca bir kopyasını taşır, canlı sayaç alttadır.
    assert fib.cagri == 0


def test_log_cagri_oncesi_ve_sonrasi_yazdirir(capsys):
    @log_cagri
    def yolculuk(hedef, hiz=1):
        return f"{hedef} hiz={hiz}"

    sonuc = yolculuk("orion", hiz=3)
    assert sonuc == "orion hiz=3"
    assert capsys.readouterr().out == (
        "-> yolculuk('orion', hiz=3)\n"
        "<- yolculuk = 'orion hiz=3'\n"
    )


def test_log_cagri_konumsal_ve_adli_argumanlar(capsys):
    @log_cagri
    def topla(a, b, c=0):
        return a + b + c

    assert topla(1, 2, c=3) == 6
    assert capsys.readouterr().out == "-> topla(1, 2, c=3)\n<- topla = 6\n"


def test_log_cagri_ad_ve_belgeyi_korur():
    @log_cagri
    def ornek():
        """Örnek belge."""
        return 1

    assert ornek.__name__ == "ornek"
    assert ornek.__doc__ == "Örnek belge."


def test_hedef_menusu_loglanir(capsys):
    menu = hedef_menusu(["a", "b"])
    assert menu == "Nereye gitmek istersin?\n[1] a\n[2] b"
    assert capsys.readouterr().out.startswith("-> hedef_menusu(['a', 'b'])\n")
    assert hedef_menusu.__name__ == "hedef_menusu"


def test_galaksi_kur_loglanir(capsys):
    g = galaksi_kur(["mars"], {"mars": []}, "mars")
    assert g["yakit"] == 50
    log = capsys.readouterr().out
    assert log.startswith("-> galaksi_kur(['mars'], {'mars': []}, 'mars')\n")
    assert galaksi_kur.__name__ == "galaksi_kur"


def test_aralik_icindeki_deger_gecer():
    @sinirla(0, 10)
    def ikiyle_carp(x):
        return x * 2

    assert ikiyle_carp(5) == 10


def test_yakit_harca_sinir_degerleri_gecerlidir():
    assert yakit_harca(0) == 100
    assert yakit_harca(100) == 0


def test_yakit_harca_aralik_disi_degerler_hata_verir():
    with pytest.raises(
        ValueError, match="yakit_harca: 150 değeri 0-100 aralığında değil"
    ):
        yakit_harca(150)
    with pytest.raises(ValueError, match="yakit_harca: -1 değeri"):
        yakit_harca(-1)


def test_yakit_harca_sinirin_hemen_disi_hata_verir():
    with pytest.raises(ValueError):
        yakit_harca(101)
    with pytest.raises(ValueError):
        yakit_harca(-1)


def test_sinirla_adli_argumanla_da_kontrol_eder():
    assert yakit_harca(miktar=30) == 70
    with pytest.raises(ValueError, match="yakit_harca: 150"):
        yakit_harca(miktar=150)


def test_sinirla_yalnizca_ilk_argumani_kontrol_eder():
    @sinirla(0, 10)
    def topla(a, b):
        return a + b

    assert topla(5, 1000) == 1005
    with pytest.raises(ValueError):
        topla(11, 1)


def test_sinirla_ad_ve_belgeyi_korur():
    @sinirla(0, 10)
    def ornek(x):
        """Örnek belge."""
        return x

    assert ornek.__name__ == "ornek"
    assert ornek.__doc__ == "Örnek belge."
    assert yakit_harca.__name__ == "yakit_harca"