def yakit_ekle(miktar: int, depo: list[int] | None = None) -> list[int]:
    """Miktarı depoya ekler ve depoyu döndürür.

    depo verilmezse her çağrıda yeni bir liste açılır. Varsayılan değer
    olarak [] kullanmak tuzaktır, çünkü o liste çağrılar arasında paylaşılır.
    """
    if depo is None:
        depo = []
    depo.append(miktar)
    return depo