from uzay_oyunu.akis import yakit_gostergesi
from uzay_oyunu.araclar import hamle_sayaci
from uzay_oyunu.dekoratorler import log_cagri
from uzay_oyunu.komutlar import KOMUTLAR 
import json
from pathlib import Path 
from uzay_oyunu.araclar import hamle_sayaci

def envanter_metni(credits: bool, engines: bool, copilot: bool) -> str:
    """Eldeki eşyaları 'Sende: ...' metnine çevirir.

    Hiç eşya yoksa boş metin döndürür. Ekrana yazmaz.
    """
    esyalar = []
    if credits:
        esyalar.append("bol kredi")
    if engines:
        esyalar.append("hiperdrive motoru")
    if copilot:
        esyalar.append("yetenekli bir pilot")

    if not esyalar:
        return ""
    return "Sende: " + ", ".join(esyalar)


@log_cagri
def hedef_menusu(hedefler: list[str]) -> str:
    """Hedef listesini numaralı menü metnine çevirir."""
    satirlar = ["Nereye gitmek istersin?"]
    for sira, hedef in enumerate(hedefler, start=1):
        satirlar.append(f"[{sira}] {hedef}")
    return "\n".join(satirlar) 

@log_cagri
def galaksi_kur(
    gezegenler: list[str],
    baglantilar: dict[str, list[str]],
    baslangic: str,
    **kwargs: int,
) -> dict:
    """Galaksi verisinden oyunun başlangıç durumunu kurar.

    baslangic gezegenler listesinde yoksa ValueError fırlatır.
    Yakıt verilmezse (yakit=...) varsayılan 50 olur.
    """
    if baslangic not in gezegenler:
        raise ValueError(f"Başlangıç gezegeni listede yok: {baslangic}")
    return {
        "gezegenler": gezegenler,
        "baglantilar": baglantilar,
        "konum": baslangic,
        "yakit": kwargs.get("yakit", 50),
    }


def galaksi_yukle() -> dict:
    """galaksi.json dosyasını okuyup galaksi_kur ile galaksiyi kurar."""
    yol = Path(__file__).with_name("galaksi.json")
    with open(yol, encoding="utf-8") as dosya:
        veri = json.load(dosya)
    return galaksi_kur(**veri)


def travel() -> None:
    """Oyunun ana döngüsü."""
    galaksi = galaksi_yukle()
    planet = galaksi["konum"]
    fuel = galaksi["yakit"]
    gosterge = yakit_gostergesi(galaksi["yakit"], 5)
    credits = engines = copilot = False
    hamle = hamle_sayaci()
    hamle_sayisi = 0
    print("Uzay yolculuğuna hoş geldin!")

    while True:
        # Gezegene varınca eşyayı al
        if planet == "centauri":
            credits = True
        elif planet == "sirius":
            copilot = True
        elif planet == "orion":
            engines = True

        print(f"\nŞu an {planet} gezegenindesin. Yakıt: {fuel}")
        envanter = envanter_metni(credits, engines, copilot)
        if envanter:
            print(envanter)

        if planet == "kara_delik":
            if credits and engines and copilot:
                print("Kara deliği geçtin, oyunu kazandın!")
            else:
                print("Eksik donanımla kara deliğe girdin. Oyun bitti.")
            break

        destinations = galaksi["baglantilar"][planet]
        durum = {
            "konum": planet,
            "baglantilar": galaksi["baglantilar"],
            "credits": credits,
            "engines": engines,
            "copilot": copilot,
        }
        print(hedef_menusu(destinations))
        secim = input("> ").strip()
        while secim in KOMUTLAR:
            komut_fonksiyonu, _ = KOMUTLAR[secim]
            print(komut_fonksiyonu(durum))
            print(hedef_menusu(destinations))
            secim = input("> ").strip()

        if secim.isdigit() and 1 <= int(secim) <= len(destinations):
            try:
                fuel = next(gosterge)
            except StopIteration:
                print("Yakıtın bitti, uzayda sürükleniyorsun…")
                break
            planet = destinations[int(secim) - 1]
            hamle_sayisi = hamle()
        else:
            print("Geçersiz seçim.")

    print(f"\nOyunu {hamle_sayisi} hamlede bitirdin!")


if __name__ == "__main__":
    travel()