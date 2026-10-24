from uzay_oyunu.oyun import travel


def test_travel_komutlari_calistirir(monkeypatch, capsys):
    girdiler = iter(["yardim", "harita", "1", "2", "2", "3"])
    monkeypatch.setattr("builtins.input", lambda _="": next(girdiler))

    travel()

    cikti = capsys.readouterr().out
    assert "envanter eşyalarını gösterir" in cikti
    assert "centauri, sirius" in cikti
    assert "oyunu kazandın!" in cikti
    assert "Oyunu 4 hamlede bitirdin!" in cikti