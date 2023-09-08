from abc import ABC, abstractmethod
from collections import deque
from itertools import accumulate, chain, pairwise
from collections.abc import Iterator

from . import aes
from .counter import Counter
from .padder import Padder
from .utils import bitwise_xor, grouper


class Mode(ABC):
    block_size = 16

    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        pass


class ECB(Mode):
    def __init__(self, key: bytes, padder: Padder):
        self.key = key
        self.padder = padder

    def encrypt(self, data: bytes) -> bytes:
        blocks = map(bytes, grouper(self.padder.pad(data), self.block_size))
        return b"".join(aes.encrypt(x, self.key) for x in blocks)

    def decrypt(self, data: bytes) -> bytes:
        blocks = map(bytes, grouper(data, self.block_size))
        return self.padder.unpad(b"".join(aes.decrypt(y, self.key) for y in blocks))


class CBC(Mode):
    def __init__(self, key, iv: bytes, padder: Padder):
        self.key = key
        self.iv = iv
        self.padder = padder

    def encrypt(self, data: bytes) -> bytes:
        process_block = lambda x, y: aes.encrypt(bitwise_xor(x, y), self.key)
        blocks = map(bytes, grouper(self.padder.pad(data), self.block_size))
        first_block = process_block(self.iv, next(blocks))
        return b"".join(
            accumulate(
                blocks,
                process_block,
                initial=first_block,
            )
        )

    def decrypt(self, data: bytes) -> bytes:
        process_block = lambda y1, y2: bitwise_xor(aes.decrypt(y2, self.key), y1)
        blocks = map(bytes, grouper(data, self.block_size))
        return self.padder.unpad(
            b"".join(
                process_block(y1, y2) for y1, y2 in pairwise(chain([self.iv], blocks))
            )
        )


class OFB(Mode):
    def __init__(self, key: bytes, iv: bytes):
        self.key = key
        self.iv = iv

    def _key_stream_gen(self) -> Iterator[bytes]:
        s = self.iv
        while True:
            s = aes.encrypt(s, self.key)
            yield s

    def encrypt(self, data: bytes) -> bytes:
        blocks = map(bytes, grouper(data, self.block_size))
        return b"".join(map(bitwise_xor, self._key_stream_gen(), blocks))

    decrypt = encrypt


class CFB(Mode):
    segment_size = 16

    def __init__(self, key: bytes, iv: bytes):
        self.key = key
        self.iv = iv

    def encrypt(self, data: bytes) -> bytes:
        ciphertext = b""
        input_block = deque(self.iv, maxlen=self.block_size)

        for x in map(bytes, grouper(data, self.segment_size)):
            output_block = aes.encrypt(bytes(input_block), self.key)
            y = bitwise_xor(x, output_block[: self.segment_size])
            ciphertext += y
            input_block += y

        return ciphertext

    def decrypt(self, data: bytes) -> bytes:
        plaintext = b""
        input_block = deque(self.iv, maxlen=self.block_size)

        for y in map(bytes, grouper(data, self.segment_size)):
            output_block = aes.encrypt(bytes(input_block), self.key)
            x = bitwise_xor(y, output_block[: self.segment_size])
            plaintext += x
            input_block += y

        return plaintext


class CFB8(CFB):
    segment_size = 1


class CTR(OFB):
    def __init__(self, key: bytes, counter: Counter):
        self.key = key
        self.counter = counter

    def _key_stream_gen(self) -> Iterator[bytes]:
        return (aes.encrypt(i, self.key) for i in self.counter)


# TODO: GCM
