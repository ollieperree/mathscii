# mathscii: Mathematical diagrams and typesetting in ASCII art

Allows rendering of mathematics stuff in ASCII for maximum portability.

Functions which generate ASCII representations of symbols/diagrams return numpy arrays of characters. Use `mathscii.display` to print them. Hopefully I'll add more symbols, and ways of combining them nicely with operators (think fractions, exponentiation etc.)

## Examples

```python
from mathscii import *

display(matrix([[1, 2, dots(), "n"],
                [2, 3, dots(), "n + 1"],
                [vdots(), vdots(), ddots(), vdots()],
                ["n", "n + 1", dots(), "2n - 1"]]))
```

![Matrix](https://i.postimg.cc/T1k8S0jv/matrix.png)

```python
from mathscii import *

fig1 = Diagram()

fig1.polygon(0, 3, 5, 2, 2, 7)
fig1.circle(10, 10, 3)
fig1.label(10, 10, "O")
fig1.label(5.5, 2, "A")
fig1.label(2, 7.7, "B")
fig1.label(-0.5, 3, "C")

display(fig1.draw())
```

![Geometry diagram](https://i.postimg.cc/Hsx15GHY/geometry.png)

## Requirements

- numpy

For diagrams:

- matplotlib
- PIL
- A TTF font: pass the path to `mathscii.diagram` or `mathscii.Diagram.__init__`. By default the path is `/usr/share/fonts/droid/DroidSansMono.ttf`.
