from Crypto.Random.random import getrandbits
from Crypto.Cipher import AES

SAMPLE_LENGTH = 16

def gen_key(l):
    """Generate a SAMPLE_LENGTH-char key"""
    s = ''
    for i in range(l):
        b = getrandbits(8)
        s += chr(b)
    return s


def prepare_val(v):
    """Append spaces to value so that it is divisible by SAMPLE_LENGTH"""
    r = len(v)%SAMPLE_LENGTH
    if r % SAMPLE_LENGTH == 0:
        return v
    v = v + ' '*(SAMPLE_LENGTH - r)
    return v


def encrypt_token(token):
    key = gen_key(SAMPLE_LENGTH)
    tok = prepare_val(token)
    aes = AES.new(key, AES.MODE_ECB)
    encrypted = aes.encrypt(tok)
    return (key, encrypted)


def restore_val(v):
    return v.strip()


def decrypt_token(key, encrypted):
    aes = AES.new(key, AES.MODE_ECB)
    tok = aes.decrypt(encrypted)
    token = restore_val(tok)
    return token


