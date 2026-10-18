# İleri Python Programlama – Uzay Oyunu

Üreteçler, boru hatları ve önbellekli rota hesabı içeren uzay oyunu projesi.

## Hafta 4 Görev 4: Önbellekli rota sayacı

`rota_sayisi("dünya", 20)` için ölçümler (`time.perf_counter()` ile):

| Sürüm | Süre (saniye) | Sonuç |
|---|---|---|
| Önbelleksiz (`rota_sayisi_onbelleksiz`) | 1.269116 | 4315343 |
| `@lru_cache` ile (`rota_sayaci`) | 0.000075 | 4315343 |

`cache_info()` çıktısı:

`CacheInfo(hits=47, misses=51, maxsize=None, currsize=51)`

Önbellekli sürüm bu ölçümde yaklaşık 17 bin kat daha hızlı.

Yorum: Önbelleksiz sürüm aynı (gezegen, adım) çiftlerini defalarca yeniden
hesaplıyor, bu yüzden adım sayısı arttıkça süre katlanarak büyüyor. Önbellekli
sürüm her çifti yalnızca bir kez hesaplıyor (51 kez, `misses`) ve geri kalan
47 çağrıda sonucu önbellekten veriyor (`hits`).

Ölçümü yeniden almak için:

```
uv run python -m uzay_oyunu.olcum
```