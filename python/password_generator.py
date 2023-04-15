import string
import random


def generate_password(m):
    sym = list(set((string.ascii_letters + string.digits)) - {'I', 'l', '1', 'o', 'O', '0'})
    result = ''
    for j in range(m):
        result += random.choice(sym)
        sym.remove(result[-1])
    if any(x.isdigit() for x in result) and any(x.isalpha() for x in result) \
            and any(x.istitle() for x in result) and \
            any(x == x.lower() and x.isalpha() for x in result):
        return result
    return generate_password(m)