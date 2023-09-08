from collections import deque
from functools import reduce
from itertools import compress
from operator import xor
from typing import Iterable, Iterator

from more_itertools import take


class LFSR:
    def __init__(self, coefficients: Iterable[int], iv: Iterable[int]) -> None:
        """LFSR-based PRNG.

        coefficients: (p0, p1, ..., pm-1)
                  iv: (s0, s1, ..., sm-1)
        """
        self.coefficients = list(coefficients)
        self._registers = deque(iv)

        assert len(self.coefficients) == len(self._registers)

    @property
    def registers(self) -> list[int]:
        return list(self._registers)

    def __iter__(self) -> Iterator[int]:
        """Yield s0, s1, ..., si."""
        while True:
            feedback = reduce(xor, compress(self._registers, self.coefficients))
            self._registers.append(feedback)
            yield self._registers.popleft()


if __name__ == "__main__":
    # cf. table 2.2 from the book
    bit_stream = LFSR([1, 1, 0], [0, 0, 1])
    assert take(9, bit_stream) == [0, 0, 1, 0, 1, 1, 1, 0, 0]
