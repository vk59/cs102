import random

def is_prime(n: int) -> bool:
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    # CODE:
    delit = 2 # делитель
    flag = True # if the number is prime, then flag == true
    while (delit*delit < n) & (flag):
        if n % delit == 0:
            flag = False
        delit+=1
    return flag

def gcd(a: int, b: int) -> int:
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    # EVKLID :
    if (a<b):
        a, b = b, a
    while (b != 0):
        r = a % b
        a = b
        b = r
    return a

def multiplicative_inverse(e: int, phi: int) -> int:
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    a = phi
    b = e
    c = []
    k = 0
    while (a % b != 0):
        ost = a % b
        c.append(a // b) # целая часть
        a = b
        b = ost
        k += 1
    x = 0
    y = 1
    for i in range (k-1, -1, -1):
        temp = y
        y = x - y * c[i]
        x = temp
    d = y % phi
    return d