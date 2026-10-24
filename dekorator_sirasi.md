# Dekoratör sırası: @say ve @lru_cache

`fib(20)` hesaplanırken `fib` fonksiyonunun kaç kez çağrıldığını `@say`
dekoratörüyle sayıyoruz. Üç dizilimde de sonuç aynı (`fib(20) = 6765`),
çağrı sayısı ise çok farklı:

| Dizilim | Çağrı sayısı |
|---|---|
| Yalnızca `@say` | 21891 |
| `@say` üstte, `@lru_cache` altta | 39 |
| `@lru_cache` üstte, `@say` altta | 21 |

## Sıra nasıl okunur?

Dekoratörler aşağıdan yukarı uygulanır: en alttaki dekoratör fonksiyonu önce
sarar, üsttekiler onu sarar. Fonksiyonu çağırdığımızda ise en dıştaki katman
önce çalışır. Bu yüzden "hangisi dışta?" sorusu, hangi çağrıların hangi
katmana ulaştığını belirler.

## 1. Yalnızca @say: 21891

Önbellek yok. `fib(20)`, `fib(19)` ve `fib(18)` çağırır, onlar da kendi
alt problemlerini çağırır. Aynı değerler (örneğin `fib(10)`) defalarca
baştan hesaplanır ve her çağrı sayılır. Toplam çağrı sayısı 2 x F(21) - 1 =
2 x 10946 - 1 = 21891.

## 2. @say üstte, @lru_cache altta: 39

`@say` en dışta olduğu için fonksiyona yapılan her çağrı önce `@say`'dan
geçer, önbellekten cevap verilenler dahil. Önbellek ise altta ve hesaplamayı
tekrarlamaktan kurtarıyor: her `n` değeri (0'dan 20'ye kadar) yalnızca bir
kez gerçekten hesaplanır. Ama `n >= 2` olan 19 hesaplama, her biri iki
çağrı yapar (`fib(n-1)` ve `fib(n-2)`), bu 38 çağrı eder. Bir de ilk
`fib(20)` çağrısı var: 38 + 1 = 39. Bu çağrıların bir kısmı önbellekten
cevaplanır ama `@say` onları da sayar, çünkü önbelleğin dışında duruyor.

## 3. @lru_cache üstte, @say altta: 21

Şimdi önbellek en dışta. Daha önce hesaplanmış bir değer istendiğinde
cevap doğrudan önbellekten gelir ve `@say`'a hiç ulaşmaz. `@say` yalnızca
önbellekte olmayan (cache miss) çağrılarda çalışır. Her `n` değeri
(0'dan 20'ye kadar, toplam 21 değer) tam bir kez hesaplandığı için sayaç 21
gösterir.

Sayaca `fib.__wrapped__.cagri` ile ulaşırız. `fib` artık `lru_cache`
nesnesidir, `__wrapped__` ise onun sardığı `@say` sarmalayıcısıdır ve
canlı sayaç oradadır. `fib.cagri` de vardır ama `functools.wraps` onu
dekoratör uygulanırken bir kez kopyaladığı için hep 0 kalır.

## Sonuç

Önbelleği dışa koymak çağrıları gerçekten azaltır (21). `@say`'ı dışa
koyarsak önbellek hesaplamayı azaltsa da her çağrı sayılır (39). Hiç
önbellek yoksa çağrı sayısı üstel büyür (21891).