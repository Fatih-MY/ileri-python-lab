from uzay_oyunu.kayit import gorev_kaydi

BEKLENEN = (
    "[YÜKSEK] Kara deliğe atla\n"
    " 1. Kredi kazan\n"
    " 2. Pilot bul\n"
    " 3. Hiperdrive al\n"
    " sorumlu: Ayşe"
)


def test_dogrudan_cagri():
    sonuc = gorev_kaydi(
        "Kara deliğe atla",
        "Kredi kazan", "Pilot bul", "Hiperdrive al",
        oncelik="yüksek", sorumlu="Ayşe",
    )
    assert sonuc == BEKLENEN


def test_acarak_cagri():
    adimlar = ["Kredi kazan", "Pilot bul", "Hiperdrive al"]
    ekler = {"oncelik": "yüksek", "sorumlu": "Ayşe"}
    assert gorev_kaydi("Kara deliğe atla", *adimlar, **ekler) == BEKLENEN


def test_varsayilan_oncelik():
    assert gorev_kaydi("Yakıt al") == "[NORMAL] Yakıt al"


def test_oncelik_yalnizca_adla_verilir():
    sonuc = gorev_kaydi("Başlık", "adım", "yüksek")
    assert sonuc.startswith("[NORMAL]")
    assert " 2. yüksek" in sonuc