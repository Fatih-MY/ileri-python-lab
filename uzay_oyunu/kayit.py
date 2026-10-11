def gorev_kaydi(
    baslik: str, *adimlar: str, oncelik: str = "normal", **ekler: str
) -> str:
    """Bir görevin kaydını metin olarak döndürür.

    baslik: görevin adı.
    *adimlar: istenen sayıda adım metni.
    oncelik: yalnızca adıyla verilebilir, varsayılanı "normal".
    **ekler: sorumlu="Ayşe" gibi ek bilgiler.
    """
    satirlar = [f"[{oncelik.upper()}] {baslik}"]
    for sira, adim in enumerate(adimlar, start=1):
        satirlar.append(f" {sira}. {adim}")
    for anahtar, deger in ekler.items():
        satirlar.append(f" {anahtar}: {deger}")
    return "\n".join(satirlar)


if __name__ == "__main__":
    # 1) Normal çağrı
    print(gorev_kaydi(
        "Kara deliğe atla",
        "Kredi kazan", "Pilot bul", "Hiperdrive al",
        oncelik="yüksek", sorumlu="Ayşe",
    ))

    print()

    # 2) Liste ve sözlüğü açarak çağrı (* ve **)
    adimlar = ["Kredi kazan", "Pilot bul", "Hiperdrive al"]
    ekler = {"oncelik": "yüksek", "sorumlu": "Ayşe"}
    print(gorev_kaydi("Kara deliğe atla", *adimlar, **ekler))