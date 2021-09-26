# -*- coding: utf-8 -*-
"""
@author: shouk
"""

def gcd(a, b):
    '''Euclid's Algorithm to find greatest common divisor'''
  assert a >= 0 and b >= 0 and a + b > 0
  while a > 0 and b > 0:
    if a >= b:
      a = a % b
    else:
      b = b % a
  return max(a, b)

def extended_gcd(a, b):
    '''extended Euclid's Algorithm to find greatest common divisor d, factor a and b such that d == a * x + b * y'''
  assert a >= b and b >= 0 and a + b > 0

  if b == 0:
    d, x, y = a, 1, 0
  else:
    (d, p, q) = extended_gcd(b, a % b)
    x = q
    y = p - q * (a // b)

  assert a % d == 0 and b % d == 0
  assert d == a * x + b * y
  return (d, x, y)

def divide(a, b, n):
    '''return the number x s.t. x = b / a (mod n) and 0 <= x <= n-1.'''
  assert n > 1 and a > 0 and gcd(a, n) == 1
  if n > a:
    return b * extended_gcd(n, a)[2] % n
  return b * extended_gcd(a, n)[1] % n
