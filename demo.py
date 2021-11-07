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
