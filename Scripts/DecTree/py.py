import numpy as py
from math import sin, exp, pi, sqrt
from scipy.integrate import quad

# function we want to integrate
a = 0.383777778
def f(x):
    a = 0.383777778
    return exp(1/sqrt((sin(a)**2-sin(x)**2)))

res, err = quad(f, 0, 0.383777778)

print("The numerical result is {:f} (+-{:g})"
    .format(res, err))

# A=[0.383777778,
# 0.366333333,
# 0.383777778,
# 0.331444444,
# 0.366333333]
# for a in A:
#     a = 0.383777778
#     def f(x):
#         f = exp(1/sqrt((sin(a)^2-sin(x)))
#     inter = quad(f,0,a)
#     print(inter)