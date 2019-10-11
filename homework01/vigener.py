def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # MY CODE:
    ciphertext = ""
    keys = []
    # transform keyword to list
    for i in range(0, len(keyword)):
        if (keyword[i] <= 'Z'):
            keys.append(ord(keyword[i]) - ord('A'))
        else:
            keys.append(ord(keyword[i]) - ord('a'))
    for i in range(0, len(plaintext)):
        num_letter = ord(plaintext[i])
        # checking the symbol
        if (num_letter >= ord('A')) & (num_letter <= ord('Z')):
            num_letter = (num_letter + keys[i % len(keys)] - ord('A')) % 26 + ord('A')
        elif (num_letter >= ord('a')) & (num_letter <= ord('z')):
            num_letter = (num_letter + keys[i % len(keys)] - ord('a')) % 26 + ord('a')
        ciphertext += chr(num_letter)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # MY CODE :
    plaintext = ""
    keys = []
    for i in range(0, len(keyword)):
        if (keyword[i] <= 'Z'):
            keys.append(ord(keyword[i]) - ord('A'))
        else:
            keys.append(ord(keyword[i]) - ord('a'))
    for i in range(0, len(ciphertext)):
        letter = ord(ciphertext[i])
        if (letter >= ord('A')) & (letter <= ord('Z')):
            letter = letter - ord('A') - keys[i % len(keys)]
            if letter < 0:
                letter = 26 + letter
            letter += ord('A')
        elif (letter >= ord('a')) & (letter <= ord('z')):
            letter = letter - ord('a') - keys[i % len(keys)]
            if letter < 0:
                letter = 26 + letter
            letter += ord('a')
        plaintext += chr(letter)
    return plaintext
