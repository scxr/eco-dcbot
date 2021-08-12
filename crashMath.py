import time
import hmac
import hashlib
import random
hash_rand = "%032x" % random.getrandbits(256)
salt = "0000000000000000000fa3b65e43e4240d71762a5bf397d5304b2596d116859c"

def get_res(hash):
    hm = hmac.new(str.encode(hash), str.encode(str(time.time())), hashlib.sha256)
    hm.update(salt.encode("utf-8"))
    h = hm.hexdigest()
    if (int(h, 16) % 33 == 0):
        return 1
    h = int(h[:13], 16)
    e = 2**52
    return (((100 * e - h) / (e-h)) // 1) / 100.0

print(get_res(hash_rand))