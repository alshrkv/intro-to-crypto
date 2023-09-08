from typing import Iterable


class PolyGF2:
    """Constructs a new polynomial whose coefficients are in GF2.
    The binary form of the given integer is interpreted as a vector of coefficients.

    Implements usual polynomial arithmetic.

    >>> a = PolyGF2(0b1100_1100)
    >>> b = PolyGF2(0b0001_0101)

    >>> print(a + b)
    x⁷ + x⁶ + x⁴ + x³ + 1

    >>> print(a * b)
    x¹¹ + x¹⁰ + x⁹ + x⁸ + x⁵ + x⁴ + x³ + x²
    """

    def __init__(self, __x=0):
        self.__x = int(__x)

    def __int__(self):
        return int(self.__x)

    def __index__(self):
        return int(self)

    def __eq__(self, other):
        return int(self) == int(other)

    def __hash__(self):
        return hash(int(self))

    def __bool__(self):
        return self != 0

    @property
    def degree(self):
        # https://en.wikipedia.org/wiki/Degree_of_a_polynomial
        return int(self).bit_length() - 1

    @classmethod
    def from_vector(cls, vector: Iterable[int]) -> "PolyGF2":
        return cls(sum(2**i * c for i, c in enumerate(vector)))

    def __repr__(self):
        cls_name = type(self).__name__
        # format spec #_b : binary form with '0b' prefix and '_' separator between every 4 bits
        return f"{cls_name}({int(self):#_b})"

    def __iter__(self):
        """Yield coefficients of the polynomial, starting from the smallest term."""
        x = int(self)
        while x:
            yield x % 2
            x //= 2

    def __str__(self):
        if not self:
            return "0"

        terms = []
        for degree, coef in enumerate(self):
            match coef, degree:
                case [1, 0]:
                    terms.append("1")
                case [1, 1]:
                    terms.append("x")
                case [1, _]:
                    terms.append(f"x{str(degree).translate(superscript)}")
        return " + ".join(reversed(terms))

    def __add__(self, other):
        return PolyGF2(int(self) ^ int(other))

    def __mul__(self, other):
        p = PolyGF2()
        for i, a in enumerate(self):
            for j, b in enumerate(PolyGF2(other)):
                p += (a & b) << (i + j)
        return p

    def __divmod__(self, other):
        # https://en.wikipedia.org/wiki/Polynomial_long_division

        q, r, d = PolyGF2(), self, PolyGF2(other)

        if not d:
            raise ZeroDivisionError("polynomial division or modulo by zero")

        while r and r.degree >= d.degree:
            t = 2 ** (r.degree - d.degree)
            q += t
            r += t * d
        return q, r

    def __truediv__(self, other):
        return divmod(self, other)[0]

    def __mod__(self, other):
        return divmod(self, other)[1]

    __sub__ = __add__
    __radd__ = __add__
    __rsub__ = __add__
    __rmul__ = __mul__
    __floordiv__ = __truediv__
    __rtruediv__ = __truediv__
    __rfloordiv__ = __truediv__
    __rmod__ = __mod__
    __rdivmod__ = __divmod__


superscript = str.maketrans(
    {
        "0": "\N{Superscript Zero}",
        "1": "\N{Superscript One}",
        "2": "\N{Superscript Two}",
        "3": "\N{Superscript Three}",
        "4": "\N{Superscript Four}",
        "5": "\N{Superscript Five}",
        "6": "\N{Superscript Six}",
        "7": "\N{Superscript Seven}",
        "8": "\N{Superscript Eight}",
        "9": "\N{Superscript Nine}",
    }
)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
