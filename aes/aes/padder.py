from abc import ABC, abstractmethod


class Padder(ABC):
    @abstractmethod
    def pad(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def unpad(self, data: bytes) -> bytes:
        pass


class SimplePadder(Padder):
    def __init__(self, block_size: int = 16, sentinel: bytes = b"\x80") -> None:
        self.block_size = block_size
        self.sentinel = sentinel

    def pad(self, data: bytes) -> bytes:
        padding_length = self.block_size - len(data) % self.block_size
        return data + self.sentinel + bytes(padding_length - 1)

    def unpad(self, data: bytes) -> bytes:
        return data[: data.rfind(self.sentinel)]
