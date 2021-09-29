# -*- coding: utf-8 -*-
"""
Some functions are provided in the quiz
@author: shouk
"""

# ===============================================
# provided functions
# ===============================================
def ConvertToInt(message_str):
  res = 0
  for i in range(len(message_str)):
    res = res * 256 + ord(message_str[i])
  return res

def ConvertToStr(n):
    res = ""
    while n > 0:
        res += chr(n % 256)
        n //= 256
    return res[::-1]

def PowMod(a, n, mod):
    if n == 0:
        return 1 % mod
    elif n == 1:
        return a % mod
    else:
        b = PowMod(a, n // 2, mod)
        b = b * b % mod
        if n % 2 == 0:
          return b
        else:
          return b * a % mod

def ExtendedEuclid(a, b):
    if b == 0:
        return (1, 0)
    (x, y) = ExtendedEuclid(b, a % b)
    k = a // b
    return (y, x - k * y)

def InvertModulo(a, n):
    (b, x) = ExtendedEuclid(a, n)
    if b < 0:
        b = (b % n + n) % n
    return b

def IntSqrt(n):
  low = 1
  high = n
  iterations = 0
  while low < high and iterations < 5000:
    iterations += 1
    mid = (low + high + 1) // 2
    if mid * mid <= n:
      low = mid
    else:
      high = mid - 1
  return low

def GCD(a, b):
  if b == 0:
    return a
  return GCD(b, a % b)

def ChineseRemainderTheorem(n1, r1, n2, r2):
  (x, y) = ExtendedEuclid(n1, n2)
  return ((r2 * x * n1 + r1 * y * n2) % (n1 * n2) + (n1 * n2)) % (n1 * n2)

# ======================================================
# my functions
# ======================================================

def Encrypt(message, modulo, exponent):
  '''message^exponent % modulo'''
  return PowMod(ConvertToInt(message), exponent, modulo)

def Decrypt(ciphertext, p, q, exponent):
  return ConvertToStr(PowMod(ciphertext, InvertModulo(exponent, (p-1) * (q-1)), p * q))

def DecipherSimple(ciphertext, modulo, exponent, potential_messages):
  '''given several potential messages, decipher'''
  for message in potential_messages:
    if ciphertext == Encrypt(message, modulo, exponent):
      return message
  return "don't know"

def DecipherSmallPrime(ciphertext, modulo, exponent):
  '''one prime is smaller than 1000000, decipher'''
  for i in range(3, 1000000, 2):
    if modulo % i == 0:
      small_prime = i
      big_prime = modulo // small_prime
      return Decrypt(ciphertext, small_prime, big_prime, exponent)
  return "don't know"

def DecipherSmallDiff(ciphertext, modulo, exponent):
  '''when the difference of p and q is small, decipher'''
  mid = IntSqrt(modulo)
  for small_prime in range(mid, mid-5000, -1):
    if modulo % small_prime == 0:
      big_prime = modulo // small_prime
      return Decrypt(ciphertext, small_prime, big_prime, exponent)

def DecipherCommonDivisor(first_ciphertext, first_modulo, first_exponent, second_ciphertext, second_modulo, second_exponent):
  '''
  Fix this implementation to correctly decipher both messages in case first_modulo and second_modulo share a prime factor,
  and return (first_message, second_message).
  '''
  if common_prime > 1:
    q1 = first_modulo // common_prime
    q2 = second_modulo // common_prime
    return (Decrypt(first_ciphertext, common_prime, q1, first_exponent), Decrypt(second_ciphertext, common_prime, q2, second_exponent))
  return ("unknown message 1", "unknown message 2")

def DecipherHastad(first_ciphertext, first_modulo, second_ciphertext, second_modulo):
  '''Bob has sent the same messagemessage to Alice and Angelina using two different public keys (n1, e=2) and (n2, e=2), decipher'''
  r = ChineseRemainderTheorem(first_modulo, first_ciphertext, second_modulo, second_ciphertext)
  return ConvertToStr(IntSqrt(r))