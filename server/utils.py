import hashlib
from db import Option

def hash_file(name):
    with open(name, "rb") as fp:
        s = hashlib.sha256(fp.read())
    return s.hexdigest()

