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


def hedef_menusu(hedefler: list[str]) -> str:
    """Hedef listesini numaralı menü metnine çevirir."""
    satirlar = ["Nereye gitmek istersin?"]
    for sira, hedef in enumerate(hedefler, start=1):
        satirlar.append(f"[{sira}] {hedef}")
    return "\n".join(satirlar) 