# İleri Python Programlama – Uzay Oyunu

## Hafta 4 Görev 4: Önbellekli rota sayacı

`rota_sayisi("dünya", 20)` için ölçümler (`time.perf_counter()` ile):

| Sürüm | Süre (saniye) | Sonuç |
|---|---|---|
| Önbelleksiz | [?] | 4315343 |
| `@lru_cache` ile | [?] | 4315343 |

`cache_info()` çıktısı: `[?]`

Yorum: Önbelleksiz sürüm aynı (gezegen, adım) çiftlerini defalarca yeniden
hesaplıyor, adım sayısı arttıkça süre katlanarak büyüyor. Önbellekli sürüm
her çifti bir kez hesaplayıp hatırlıyor, bu yüzden süre milisaniyenin altında.