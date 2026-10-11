from uzay_oyunu.tuzaklar import yakit_ekle


def test_depo_cagrilar_arasinda_paylasilmaz():
    ilk = yakit_ekle(10)
    ikinci = yakit_ekle(5)
    assert ilk == [10]
    assert ikinci == [5]


def test_verilen_depo_kullanilir():
    depo = [1]
    assert yakit_ekle(2, depo) == [1, 2]
    assert depo == [1, 2]