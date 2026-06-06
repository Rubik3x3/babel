# Biblioteca de Babel

La Biblioteca de Babel de Jorge Luis Borges, en Python. Le das un texto y te
dice en qué coordenada de la biblioteca está. Le das una coordenada y te
devuelve el texto. Funciona en ambos sentidos.

No guarda nada. La biblioteca ya contiene todas las páginas posibles, así que
cualquier texto que se te ocurra ya está ahí dentro. El programa solo calcula
dónde.

```python
from babel import encode, decode

direccion = encode("el universo, que otros llaman la biblioteca.")
# '1yxb81oh2ve7dt0s5ldieu1buitug9r2...-3-1-9:118'

decode(direccion).rstrip()
# 'el universo, que otros llaman la biblioteca.'
```

## Cómo funciona

Una página son 3200 caracteres de un alfabeto de 29 símbolos. Si a cada símbolo
le das un valor (a=0, b=1... y así), el texto entero se convierte en un número
escrito en base 29. O sea: cada página posible es un número, y cada número es una
página.

Si usáramos ese número tal cual como coordenada, dos textos parecidos quedarían
en estantes pegados. Para evitarlo, el número `n` pasa por una cuenta que lo
manda a otra parte de la biblioteca:

```
y = (MULT * n + OFFSET) mod N
```

Lo importante es que la cuenta se puede deshacer: como `MULT` no comparte
factores con N, podés hacerla al revés y recuperar el texto original sin perder
nada. Por eso encode y decode funcionan en los dos sentidos.

Al final, ese número `y` se corta en pedazos —hexágono, pared, estante, volumen
y página—, que es lo que arma la dirección.

## Uso

```bash
python3 babel.py   # demo de ida y vuelta
```

Necesitas Python 3.8 o superior sin dependencias.

## Alfabeto

Las 26 letras de la `a` a la `z`, más espacio, coma y punto: 29 símbolos. Todo
se pasa a minúsculas y cualquier otro carácter cuenta como espacio.

Este es el algoritmo que usa [Library of Babel](https://play.google.com/store/apps/details?id=com.rubik3x3.libraryofbabel.library_of_babel),
una app en Flutter que publiqué en Google Play.

Basado en [libraryofbabel.info](https://libraryofbabel.info) de Jonathan Basile.
