
def gcd(a: int, b:int):
    while b != 0:
        a, b = b, a%b
    return a

def extended_gcd(a:int, b:int):
    if b == 0:
        return a, 1, 0
    
    gcd, x1, y1 = extended_gcd(b, a%b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def mod_inverse(a: int, m: int):
    gcd, x, _ = extended_gcd(a, m)

    if gcd != 1:
        raise ValueError("Modular Multiplication Inverse is not exist")
    
    return x % m
