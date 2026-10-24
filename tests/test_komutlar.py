import pytest

from uzay_oyunu import komutlar as komutlar_modulu
from uzay_oyunu.komutlar import KOMUTLAR, envanter, harita, komut, yardim

DURUM = {
    "konum": "sirius",
    "baglantilar": {"sirius": ["orion", "dünya", "kara_delik"]},
    "credits": True,
    "engines": False,
    "copilot": True,
}


@pytest.fixture
def temiz_komutlar(monkeypatch):
    """Testlerde kaydedilen komutlar gerçek KOMUTLAR sözlüğünü kirletmesin."""
    monkeypatch.setattr(komutlar_modulu, "KOMUTLAR", dict(KOMUTLAR))
    return komutlar_modulu.KOMUTLAR


def test_uc_komut_kayitli():
    assert set(KOMUTLAR) == {"yardim", "envanter", "harita"}


def test_kayit_fonksiyon_ve_aciklama_tutar():
    fonksiyon, aciklama = KOMUTLAR["harita"]
    assert fonksiyon is harita
    assert aciklama == "gidebileceğin gezegenleri gösterir"


def test_komut_fonksiyonu_degistirmez(temiz_komutlar):
    def ornek(durum):
        """Örnek belge."""
        return "x"

    assert komut("ornek_komut", "deneme")(ornek) is ornek
    assert temiz_komutlar["ornek_komut"] == (ornek, "deneme")
    assert ornek.__name__ == "ornek"


def test_ayni_ad_iki_kez_kullanilirsa_hata(temiz_komutlar):
    @komut("tekrar", "ilk")
    def ilk(durum):
        return "bir"

    with pytest.raises(ValueError, match="tekrar"):

        @komut("tekrar", "ikinci")
        def ikinci(durum):
            return "iki"

    assert temiz_komutlar["tekrar"] == (ilk, "ilk")


def test_yardim_komutlari_listeler():
    assert yardim(DURUM) == (
        "envanter eşyalarını gösterir\n"
        "harita gidebileceğin gezegenleri gösterir\n"
        "yardim komutları listeler"
    )


def test_envanter_esyalari_gosterir():
    assert envanter(DURUM) == "Sende: bol kredi, yetenekli bir pilot"


def test_envanter_bos():
    bos = {**DURUM, "credits": False, "copilot": False}
    assert envanter(bos) == "Envanterin boş."


def test_harita_gidilebilecek_gezegenleri_gosterir():
    assert harita(DURUM) == "orion, dünya, kara_delik"