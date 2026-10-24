from uzay_oyunu.dekoratorler import sinirla


@sinirla(0, 100)
def yakit_harca(miktar: int) -> int:
    """Dolu depodan (100 birim) miktar kadar yakıt harcar, kalanı döndürür."""
    return 100 - miktar


if __name__ == "__main__":
    print(yakit_harca(30))
    try:
        yakit_harca(150)
    except ValueError as hata:
        print(f"ValueError: {hata}")