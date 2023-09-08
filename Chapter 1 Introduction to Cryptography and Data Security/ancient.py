import math
from string import ascii_lowercase


class SubstitutionCipher:
    def __init__(self, key: dict[str, str]) -> None:
        self._table = str.maketrans({x.lower(): y.lower() for x, y in key.items()})
        self._inverse = str.maketrans({y.lower(): x.lower() for x, y in key.items()})

    def encode(self, plaintext: str) -> str:
        return plaintext.lower().translate(self._table)

    def decode(self, ciphertext: str) -> str:
        return ciphertext.lower().translate(self._inverse)


class AffineCipher(SubstitutionCipher):
    def __init__(self, key: tuple[int, int], alphabet=ascii_lowercase) -> None:
        (a, b), m = key, len(alphabet)

        if math.gcd(a, m) != 1:
            raise ValueError(f"{a=} and {m=} must be coprime")

        super().__init__({x: alphabet[(a * i + b) % m] for i, x in enumerate(alphabet)})


class CaesarCipher(AffineCipher):
    def __init__(self, key: int, alphabet=ascii_lowercase) -> None:
        super().__init__((1, key), alphabet)


if __name__ == "__main__":
    ROT13 = CaesarCipher(13).encode
    x = "the quick brown fox jumps over the lazy dog"
    assert ROT13(ROT13(x)) == x
