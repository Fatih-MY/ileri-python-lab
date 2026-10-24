from collections.abc import Callable
from functools import lru_cache

from uzay_oyunu.dekoratorler import say


def fib_yalniz_say() -> Callable[[int], int]:
    """Yalnızca @say ile süslenmiş özyinelemeli fibonacci üretir."""

    @say
    def fib(n: int) -> int:
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    return fib


def fib_say_ustte() -> Callable[[int], int]:
    """@say üstte, @lru_cache altta olan fibonacci üretir."""

    @say
    @lru_cache(maxsize=None)
    def fib(n: int) -> int:
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    return fib


def fib_cache_ustte() -> Callable[[int], int]:
    """@lru_cache üstte, @say altta olan fibonacci üretir.

    Canlı sayaç, fib.__wrapped__.cagri ile okunur.
    """

    @lru_cache(maxsize=None)
    @say
    def fib(n: int) -> int:
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    return fib


if __name__ == "__main__":
    ilk = fib_yalniz_say()
    ilk(20)
    print(f"Yalnızca @say : {ilk.cagri}")

    ikinci = fib_say_ustte()
    ikinci(20)
    print(f"@say üstte, @lru_cache altta: {ikinci.cagri}")

    ucuncu = fib_cache_ustte()
    ucuncu(20)
    print(f"@lru_cache üstte, @say altta: {ucuncu.__wrapped__.cagri}")