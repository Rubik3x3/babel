"""
Biblioteca de Babel: dado un texto devuelve su direccion dentro de la
biblioteca, y dada una direccion devuelve el texto. No se guarda nada, todo
se calcula.

Una pagina son 3200 caracteres sobre un alfabeto de 29 simbolos, asi que hay
29**3200 paginas posibles. Cada pagina se lee como un numero en base 29 y se
mezcla con un cifrado afin modulo N: y = (MULT * n + OFFSET) % N. Como MULT es
coprimo con N la operacion es invertible (inverso modular), asi que de cualquier
direccion se puede volver al texto original sin perder nada. Ese y se reparte
en pagina, volumen, estante, pared y hexagono.
"""

from math import gcd

ALPHABET = "abcdefghijklmnopqrstuvwxyz ,."
BASE = len(ALPHABET)
PAGE_LEN = 3200 # 40 renglones de 80 caracteres cada uno
N = BASE ** PAGE_LEN
WALLS, SHELVES, VOLUMES, PAGES = 4, 5, 32, 410

# Constantes del cifrado afin. MULT tiene que ser coprimo con N (o sea, no
# multiplo de 29) para poder invertirlo; OFFSET puede ser cualquier numero.
MULT = 982451653
OFFSET = 472882049
assert gcd(MULT, N) == 1
_MULT_INV = pow(MULT, -1, N)
_B36 = "0123456789abcdefghijklmnopqrstuvwxyz"

def _text_to_int(text: str) -> int:
    text = text.lower()[:PAGE_LEN].ljust(PAGE_LEN)
    n = 0
    for ch in text:
        n = n * BASE + ALPHABET.index(ch if ch in ALPHABET else " ")
    return n

def _int_to_text(n: int) -> str:
    chars = []
    for _ in range(PAGE_LEN):
        n, d = divmod(n, BASE)
        chars.append(ALPHABET[d])
    return "".join(reversed(chars))

def _to_base36(n: int) -> str:
    if n == 0:
        return "0"
    s = []
    while n:
        n, d = divmod(n, 36)
        s.append(_B36[d])
    return "".join(reversed(s))

def _from_base36(s: str) -> int:
    n = 0
    for ch in s:
        n = n * 36 + _B36.index(ch)
    return n

def encode(text: str) -> str:
    # Texto a direccion 'hexagono-pared-estante-volumen:pagina'.
    n = _text_to_int(text)
    y = (MULT * n + OFFSET) % N

    y, page = divmod(y, PAGES)
    y, volume = divmod(y, VOLUMES)
    y, shelf = divmod(y, SHELVES)
    hexagon, wall = divmod(y, WALLS)
    return f"{_to_base36(hexagon)}-{wall}-{shelf}-{volume}:{page + 1}"

def decode(address: str) -> str:
    # Direccion a texto.
    hexagon, wall, shelf, rest = address.split("-")
    volume, page = rest.split(":")
    wall, shelf, volume, page = int(wall), int(shelf), int(volume), int(page) - 1

    y = _from_base36(hexagon)
    y = ((y * WALLS + wall) * SHELVES + shelf) * VOLUMES + volume
    y = y * PAGES + page

    n = (_MULT_INV * (y - OFFSET)) % N
    return _int_to_text(n)

if __name__ == "__main__":
    frase = "el universo, que otros llaman la biblioteca."
    direccion = encode(frase)
    pagina = decode(direccion)

    print("Frase     :", repr(frase))
    print("Coordenada:", direccion[:70] + "...")
    print("Recuperada:", repr(pagina.rstrip()))
    print("Reversible:", pagina.rstrip() == frase)
