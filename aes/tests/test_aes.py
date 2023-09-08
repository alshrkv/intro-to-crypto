import pytest
from hypothesis import given
from hypothesis.strategies import SearchStrategy, binary, one_of

from aes import aes


def aes_key() -> SearchStrategy[bytes]:
    return one_of(
        [binary(min_size=size, max_size=size) for size in aes.AES_KEY_LENGTHS]
    )


@given(binary(min_size=16, max_size=16), aes_key())
def test_decrypt_inverts_encrypt(plaintext: bytes, key: bytes):
    assert aes.decrypt(aes.encrypt(plaintext, key), key) == plaintext


FIPS_examples = (
    (
        "00112233445566778899aabbccddeeff",  # plaintext
        "000102030405060708090a0b0c0d0e0f",  # key
        "69c4e0d86a7b0430d8cdb78070b4c55a",  # ciphertext
    ),
    (
        "00112233445566778899aabbccddeeff",
        "000102030405060708090a0b0c0d0e0f1011121314151617",
        "dda97ca4864cdfe06eaf70a0ec0d7191",
    ),
    (
        "00112233445566778899aabbccddeeff",
        "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
        "8ea2b7ca516745bfeafc49904b496089",
    ),
)


@pytest.mark.parametrize("plaintext, key, ciphertext", FIPS_examples)
def test_FIPS_examples(plaintext: str, key: str, ciphertext: str):
    encrypted = aes.encrypt(bytes.fromhex(plaintext), bytes.fromhex(key))
    decrypted = aes.decrypt(bytes.fromhex(ciphertext), bytes.fromhex(key))
    assert encrypted.hex() == ciphertext
    assert decrypted.hex() == plaintext
