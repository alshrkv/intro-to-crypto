from hypothesis import given
from hypothesis.strategies import builds, integers

from polynomial import PolyGF2


def polynomials():
    return builds(PolyGF2, integers(0, 256))


@given(polynomials(), polynomials(), polynomials())
def test_addition_properties(x, y, z):
    assert x + y == y + x
    assert (x + y) + z == x + (y + z)
    assert x + 0 == 0 + x == x


@given(polynomials(), polynomials(), polynomials())
def test_multiplication_properties(x, y, z):
    assert x * y == y * x
    assert (x * y) * z == x * (y * z)
    assert x * (y + z) == x * y + x * z
    assert x * 1 == x
    assert x * 0 == 0


@given(polynomials(), polynomials().filter(bool))
def test_division_properties(x, y):
    q, r = divmod(x, y)
    assert x == q * y + r


@given(polynomials())
def test_can_rebuild_itself_from_coefficients(x):
    assert PolyGF2.from_vector(list(x)) == x
