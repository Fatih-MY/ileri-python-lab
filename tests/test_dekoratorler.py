import re

from uzay_oyunu.akis import rota_sayisi_onbelleksiz
from uzay_oyunu.dekoratorler import sure_olc
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