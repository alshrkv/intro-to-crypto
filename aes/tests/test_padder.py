from hypothesis import given
from hypothesis.strategies import binary

from aes.padder import SimplePadder


@given(binary())
def test_unpad_inverts_pad(data: bytes):
    padder = SimplePadder(16)
    assert padder.unpad(padder.pad(data)) == data


@given(binary())
def test_length_of_padded_data_is_a_multiple_of_block_size(data: bytes):
    block_size = 16
    assert len(SimplePadder(block_size).pad(data)) % block_size == 0
