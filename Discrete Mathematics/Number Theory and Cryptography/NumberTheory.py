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

def lcm(a, b):
  '''least common multiple'''
  assert a > 0 and b > 0
  m, n = a, b
  while m > 0 and n > 0:
    if m < n:
      m, n = n, m
    m = m % n
  return a * b // max(m, n)

def diophantine(a, b, c):
  '''Given three numbers a>0, b>0, and c, return some x and y such that ax+by=c'''
  assert c % gcd(a, b) == 0
  # return (x, y) such that a * x + b * y = c
  d, x, y = extended_gcd(a, b)
  if b > a:
    x, y = y, x
  return (x * c // d, y * c // d)

def divide(a, b, n):
    '''return the number x s.t. x = b / a (mod n) and 0 <= x <= n-1.'''
  assert n > 1 and a > 0 and gcd(a, n) == 1
  if n > a:
    return b * extended_gcd(n, a)[2] % n
  return b * extended_gcd(a, n)[1] % n

def FastModularExponentiation(b, k, m):
  '''return b^(2^k) mod m'''
  val = b % m
  for i in range(k):
    val = val ** 2 % m
  return val

def FastModularExponentiation(b, e, m):
  '''return b^e mod m'''
  if m == 1:
    return 0
  if e == 0:
    return 1
  bit = e
  vals = [b % m]
  digits = []
  ans = 1
  while bit > 0:
    digits.append(bit % 2)
    bit //= 2
    vals.append(vals[-1] ** 2 % m)
  for i in range(len(digits)):
    if digits[i] == 1:
      ans = ans * vals[i] % m
  return ans

def ChineseRemainderTheorem(n1, r1, n2, r2):
  (x, y) = extended_gcd(n1, n2)
  return (x * n1 * r2 + y * n2 * r1) % (n1 * n2)
