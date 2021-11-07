
Smart Matrix
===========================
This document is the description of work for Smart Matrix

****
 
| Project Name | Author |
| ---- | ---- |
| Smart Matrix | Enze Xu |

| Version | Date |
| ---- | ---- |
| v1.0 | 11/06/2021 |

****
# Catalog

* [1 Purpose](#1-purpose)
* [2 Format](#2-format)
* [3 Demo](#3-demo)

****

# 1 Purpose

1. Matrix multiplication in algebraic form

****

# 2 Format

A `matrix` has m×n `cell`s in list format, and each cell(a string, e.g., `3*x12-y1^2+3`) includes several `part`s (e.g., `3*x12^2*y22`, `-y1^2`, `+3`).

A `part` has a sig, a coefficient and a unit:
1. sig: a char, `+` or `-`. Default value is `+`.
2. coefficient: a float, e.g., `1*`, `3.2001*`. Default value is `1`. Not that if coefficient is not default, here must be a `*` before the unit.
3. unit: hard to explain, just give examples: `x32^2*y1*x2`, `y1*y1^2*y1^3`

There can be spaces in the input format, though they will just be ignored after all.

****

# 3 Demo
```python
# demo.py
# Created by ENZE XU on 2021/11/6.

from smart_matrix import SmartMatrix, times_smart_matrix

sm1 = SmartMatrix([["x1+x2+x2", "x2+x3", "x3+x1"], ["1*x1", "2*x2", "3*x3"]])
sm2 = SmartMatrix([["1", "y1^1"], ["2", "y2^2"], ["3", "y3^3"]])
sm3 = times_smart_matrix(sm1, sm2)
print(sm1)
print(sm2)
print(sm3)
print("sm3[0][1]:", sm3[0][1])
```

```shell
$ python demo.py
shape = (2, 3)
[ +x1 +2*x2,    +x2 +x3,    +x1 +x3 ]
[       +x1,      +2*x2,      +3*x3 ]

shape = (3, 2)
[    +1,    +y1 ]
[    +2,  +y2^2 ]
[    +3,  +y3^3 ]

shape = (2, 2)
[                                   +4*x1 +4*x2 +5*x3,  +x1*y1 +x1*y3^3 +2*x2*y1 +x2*y2^2 +x3*y2^2 +x3*y3^3 ]
[                                     +x1 +4*x2 +9*x3,                         +x1*y1 +2*x2*y2^2 +3*x3*y3^3 ]

sm3[0][1]:  +x1*y1 +x1*y3^3 +2*x2*y1 +x2*y2^2 +x3*y2^2 +x3*y3^3
```