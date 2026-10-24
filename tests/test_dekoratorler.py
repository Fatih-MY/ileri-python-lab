import re

from uzay_oyunu.akis import rota_sayisi_onbelleksiz
from uzay_oyunu.dekoratorler import say, sure_olc
from uzay_oyunu.fib_deney import fib_cache_ustte, fib_say_ustte, fib_yalniz_say
from uzay_oyunu.oyun import galaksi_yukle


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