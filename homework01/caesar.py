def encrypt_caesar(plaintext: str) -> str:
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # MY CODE encrypt:
    shift = 3 
    ciphertext = ""
    for i in range (0, len(plaintext)):
        letter = ord(plaintext[i]) # spell the word
        if (letter >= ord("A") & letter <= ord("Z") | letter >= ord("a") & letter <= ord("z")): 
            # check the letter and form new 'ord' of letter
            letter = letter + shift
        ciphertext += chr(letter) # add the new letter to encrypt word
    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # MY CODE decrypt:


    return plaintext