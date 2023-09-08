import pytest
from hypothesis import given
from hypothesis.strategies import SearchStrategy, binary

from aes import modes
from aes.counter import Counter, SimpleCounter
from aes.padder import Padder, SimplePadder

from .test_aes import aes_key


def iv(size: int) -> SearchStrategy[bytes]:
    return binary(min_size=size, max_size=size)


@given(binary(), aes_key())
def test_ECB_decrypt_inverts_encrypt(plaintext: bytes, key: bytes):
    mode = modes.ECB(key, SimplePadder())
    assert mode.decrypt(mode.encrypt(plaintext)) == plaintext


@given(binary(), iv(16), aes_key())
def test_CBC_decrypt_inverts_encrypt(plaintext: bytes, iv: bytes, key: bytes):
    mode = modes.CBC(key, iv, SimplePadder())
    assert mode.decrypt(mode.encrypt(plaintext)) == plaintext


@given(binary(), iv(16), aes_key())
def test_OFB_decrypt_inverts_encrypt(plaintext: bytes, iv: bytes, key: bytes):
    mode = modes.OFB(key, iv)
    assert mode.decrypt(mode.encrypt(plaintext)) == plaintext


@given(binary(), iv(16), aes_key())
def test_CFB128_decrypt_inverts_encrypt(plaintext: bytes, iv: bytes, key: bytes):
    mode = modes.CFB(key, iv)
    assert mode.decrypt(mode.encrypt(plaintext)) == plaintext


@given(binary(), iv(16), aes_key())
def test_CFB8_decrypt_inverts_encrypt(plaintext: bytes, iv: bytes, key: bytes):
    mode = modes.CFB8(key, iv)
    assert mode.decrypt(mode.encrypt(plaintext)) == plaintext


@given(binary(), iv(12), aes_key())
def test_CTR_decrypt_inverts_encrypt(plaintext: bytes, iv: bytes, key: bytes):
    mode = modes.CTR(key, SimpleCounter(iv))
    assert mode.decrypt(mode.encrypt(plaintext)) == plaintext


@pytest.fixture
def NIST_plaintext():
    return bytes.fromhex(
        "6bc1bee22e409f96e93d7e117393172a"
        "ae2d8a571e03ac9c9eb76fac45af8e51"
        "30c81c46a35ce411e5fbc1191a0a52ef"
        "f69f2445df4f9b17ad2b417be66c3710"
    )


@pytest.fixture
def NIST_key():
    return bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")


@pytest.fixture
def NIST_iv():
    return bytes.fromhex("000102030405060708090a0b0c0d0e0f")


class NoPadding(Padder):
    def pad(self, data: bytes) -> bytes:
        return data

    unpad = pad


def test_ECB_NIST_example(NIST_plaintext: bytes, NIST_key: bytes):
    mode = modes.ECB(NIST_key, NoPadding())
    assert mode.encrypt(NIST_plaintext).hex() == (
        "3ad77bb40d7a3660a89ecaf32466ef97"
        "f5d3d58503b9699de785895a96fdbaaf"
        "43b1cd7f598ece23881b00e3ed030688"
        "7b0c785e27e8ad3f8223207104725dd4"
    )


def test_CBC_NIST_example(NIST_plaintext: bytes, NIST_key: bytes, NIST_iv: bytes):
    mode = modes.CBC(NIST_key, NIST_iv, NoPadding())
    assert mode.encrypt(NIST_plaintext).hex() == (
        "7649abac8119b246cee98e9b12e9197d"
        "5086cb9b507219ee95db113a917678b2"
        "73bed6b8e3c1743b7116e69e22229516"
        "3ff1caa1681fac09120eca307586e1a7"
    )


def test_OFB_NIST_example(NIST_plaintext: bytes, NIST_key: bytes, NIST_iv: bytes):
    mode = modes.OFB(NIST_key, NIST_iv)
    assert mode.encrypt(NIST_plaintext).hex() == (
        "3b3fd92eb72dad20333449f8e83cfb4a"
        "7789508d16918f03f53c52dac54ed825"
        "9740051e9c5fecf64344f7a82260edcc"
        "304c6528f659c77866a510d9c1d6ae5e"
    )


def test_CFB128_NIST_example(NIST_plaintext: bytes, NIST_key: bytes, NIST_iv: bytes):
    mode = modes.CFB(NIST_key, NIST_iv)
    assert mode.encrypt(NIST_plaintext).hex() == (
        "3b3fd92eb72dad20333449f8e83cfb4a"
        "c8a64537a0b3a93fcde3cdad9f1ce58b"
        "26751f67a3cbb140b1808cf187a4f4df"
        "c04b05357c5d1c0eeac4c66f9ff7f2e6"
    )


def test_CFB8_NIST_example(NIST_plaintext: bytes, NIST_key: bytes, NIST_iv: bytes):
    mode = modes.CFB8(NIST_key, NIST_iv)
    assert mode.encrypt(NIST_plaintext[:18]).hex() == (
        "3b79424c9c0dd436bace9e0ed4586a4f32b9"
    )


class NISTCounter(Counter):
    def __iter__(self):
        return (
            bytes.fromhex(block)
            for block in (
                "f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff",
                "f0f1f2f3f4f5f6f7f8f9fafbfcfdff00",
                "f0f1f2f3f4f5f6f7f8f9fafbfcfdff01",
                "f0f1f2f3f4f5f6f7f8f9fafbfcfdff02",
            )
        )


def test_CTR_NIST_example(NIST_plaintext: bytes, NIST_key: bytes):
    mode = modes.CTR(NIST_key, NISTCounter())
    assert mode.encrypt(NIST_plaintext).hex() == (
        "874d6191b620e3261bef6864990db6ce"
        "9806f66b7970fdff8617187bb9fffdff"
        "5ae4df3edbd5d35e5b4f09020db03eab"
        "1e031dda2fbe03d1792170a0f3009cee"
    )
