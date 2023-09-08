import itertools
from functools import reduce
from operator import xor
from typing import TypeVar
from collections.abc import Iterable, Iterator

T = TypeVar("T")


def grouper(items: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    # grouper([1, 2, 3, 4, 5], 2) --> (1, 2) (3, 4) (5, )
    it = iter(items)
    while block := tuple(itertools.islice(it, n)):
        yield block


def bitwise_xor(a: Iterable[int], b: Iterable[int]) -> bytes:
    return bytes(map(xor, a, b))


def vector_by_matrix(v: Iterable[int], m: Iterable[Iterable[int]]) -> Iterator[int]:
    return (gdot(row, v) for row in m)


def gdot(a: Iterable[int], b: Iterable[int]) -> int:
    return gsum(map(gmul, a, b))


# GF256 arithmetic:
# https://en.wikipedia.org/wiki/Finite_field_arithmetic#Program_examples


def gsum(nums: Iterable[int]) -> int:
    return reduce(xor, nums, 0)


def gmul(a: int, b: int) -> int:
    p = 0
    while a and b:
        if b & 1:
            p ^= a
        if a >= 128:
            a = (a << 1) ^ 0b1_0001_1011
        else:
            a <<= 1
        b >>= 1
    return p
