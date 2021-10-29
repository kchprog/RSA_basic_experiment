"""
Implementation of the RSA algorithm in Python with rudimentary design.
"""


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return the gcd of a and b, and integers p and q such that

    gcd(a, b) == p * a + b * q.

    >>> extended_gcd(10, 3)
    (1, 1, -3)
    """
    x, y = a, b

    # Initialize px, qx, py, and qy
    px, qx = 1, 0
    py, qy = 0, 1

    while y != 0:
        # Loop invariants
        # assert math.gcd(a, b) == math.gcd(x, y)  # L.I. 1
        assert x == px * a + qx * b  # L.I. 2
        assert y == py * a + qy * b  # L.I. 3

        q, r = divmod(x, y)  # quotient and remainder when a is divided by b

        # Update x and y
        x, y = y, r

        # Update px, qx, py, and qy
        px, qx, py, qy = py, qy, px - (q * py), qx - (q * qy)

    return x, px, qx


def modular_inverse(a: int, n: int) -> int:
    """Return the inverse of a modulo n, in the range 0 to n - 1 inclusive.

    Preconditions:

    - a and n are coprime

    >>> modular_inverse(10, 3)  # 10 * 1 is equivalent to 1 modulo 3
    1
    >>> modular_inverse(3, 10)  # 3 * 7 is equivalent to 1 modulo 10
    7
    """

    # Step 1: Use extended_gcd to get the linear combination coefficients
    # Since gcd(a, n) = 1, we know that a * x + n * y = 1

    coefficient_p = extended_gcd(a, n)[1]
    coefficient_q = extended_gcd(a, n)[2]
    # Step 2: Try the examples, and notice that the docstring says the return value must be in
    # the range "0 to n-1". How can we use modulo to fix this?

    return (coefficient_p % n + n) % n

def recursive_euclidean(a: int, b: int) -> int:
    """Return the gcd of a and b using the Euclidean algorithm.
    """
    if b == 0:
        return a
    else:
        return recursive_euclidean(b, a % b)

import math
def get_prime_number(n: int) -> int:
    """Return the nth prime number.

    >>> get_prime_number(1)
    2
    >>> get_prime_number(2)
    3
    >>> get_prime_number(3)
    5
    >>> get_prime_number(4)
    7
    >>> get_prime_number(5)
    11
    """
    prime_number = 2
    count = 1
    while count < n:
        prime_number += 1
        if is_prime(prime_number):
            count += 1
    return prime_number

def is_prime(n: int) -> bool:
    """Return True if n is prime, and False otherwise.

    >>> is_prime(2)
    True
    >>> is_prime(4)
    False
    >>> is_prime(11)
    True
    >>> is_prime(15)
    False
    """
    if n < 2:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        for i in range(3, math.ceil(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

import random


def generate_key_variables() -> tuple[int, int]:
    """Generate two distinct prime numbers p and q, and return them as a tuple.

    >>> generate_key_variables()
    (11, 17)
    """
    random_number = random.randint(60, 150)
    random_number_b = random.randint(60, 150)

    p = get_prime_number(random_number)
    q = get_prime_number(random_number_b)

    return p, q


def compute_totient(p, q) -> int:
    """Return the totient of p and q, given P and Q are prime numbers.

    >>> compute_totient(11, 17)
    12
    """
    return (p - 1) * (q - 1)


def choose_e(p: int, q: int) -> int:
    """Choose an integer e such that e is coprime to p-1 and q-1.

    >>> choose_e(11, 17)
    7
    """
    my_totient = compute_totient(p, q)
    for i in range(2, my_totient - 1):
        if extended_gcd(i, my_totient)[0] == 1:
            return i


def choose_d(e: int, p: int, q: int) -> int:
    """Choose an integer d such that d is coprime to e and totient(p, q).

    >>> choose_d(7, 11, 17)
    3
    """
    my_totient = compute_totient(p, q)
    return modular_inverse(e, my_totient)


class communication_party:
    def __init__(self):
        self.p, self.q = generate_key_variables()

    def encrypt(self, message, e, n):
        return pow(message, e, n)

    def decrypt(self, cipher, d, n):
        return pow(cipher, d, n)

    def get_public_key(self, e, n):
        return (e, n)

    def get_private_key(self, d, n):
        return (d, n)

def main():
    """Run the program.
    """
    p, q = generate_key_variables()
    n = p * q

    e = choose_e(p, q)
    d = choose_d(e, p, q)

    party = communication_party()
    message = int(input("Enter a message: "))
    print("Encrypting message...")
    public_key = party.get_public_key(e, n)
    print("Public key:", public_key)
    private_key = party.get_private_key(d, n)
    print("Private key:", private_key)
    cipher = party.encrypt(message, e, n)
    print("Cipher:", cipher)
    decrypted = party.decrypt(cipher, d, n)
    print("The message is:", decrypted)


    
