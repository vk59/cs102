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