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
    # делитель
    delit = 2
    # if the number is prime, then flag == true
    flag = True
    while (delit*delit < n) & (flag):
        if n % delit == 0:
            flag = False
        delit += 1
    return flag


def gcd(a: int, b: int) -> int:
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    # EVKLID :
    if (a < b):
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
        # целая часть
        c.append(a // b)
        a = b
        b = ost
        k += 1
    x = 0
    y = 1
    for i in range(k-1, -1, -1):
        temp = y
        y = x - y * c[i]
        x = temp
    d = y % phi
    return d


def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    # n = pq
    n = p * q

    # phi = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))
