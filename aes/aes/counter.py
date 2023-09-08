from abc import ABC, abstractmethod
from typing import Iterator


class Counter(ABC):
    @abstractmethod
    def __iter__(self) -> Iterator[bytes]:
        pass


class SimpleCounter(Counter):
    def __init__(self, iv: bytes, size: int = 4):
        self.iv = iv
        self.size = size

    def __iter__(self) -> Iterator[bytes]:
        for i in range(2 ** (self.size * 8)):
            yield self.iv + i.to_bytes(self.size, byteorder="big")
