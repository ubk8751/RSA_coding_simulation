import math

class Bob():
    def __init__(self, p:int, q:int, additional_bits:int=4, **kwargs):
        self._alpha = p * q
        self._beta = (p - 1) * (q - 1)
        self._e = self.find_coprime(beta=self.beta)
        self._d = self.mod_inverse(e=self.e, beta=self.beta)
        self._additional_bits = additional_bits

    
    def find_coprime(self, beta:int, **kwargs) -> int:
        e = 65537
        while math.gcd(e, beta) != 1:
            e += 2  
        return e

    def mod_inverse(self, e, beta) -> int|None:
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        gcd, x, _ = extended_gcd(e, beta)
        if gcd == 1:
            return x % beta  # Ensure d is positive
        else:
            return None

    def receive(self, c:list[int], **kwargs):
        print(f'B received {sum(c)} from A')
        message = 0
        for m in c:
            message += m**self.d % self.alpha
        bin_message = bin(message)[2:][:-self.additional_bits]
        message = int(bin_message, 2)
        print(f'After decryption the message received was {message}')

    @property
    def alpha(self) -> int:
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if not isinstance(value, int):
            raise ValueError('alpha must be an integer')
        self._alpha = value

    @property
    def beta(self) -> int:
        return self._beta

    @beta.setter
    def beta(self, value):
        if not isinstance(value, int):
            raise ValueError('beta must be an integer')
        self._beta = value

    @property
    def e(self) -> int:
        return self._e

    @e.setter
    def e(self, value):
        if not isinstance(value, int):
            raise ValueError('e must be an integer')
        self._e = value
        self._d = self.mod_inverse(self._e, self._beta)

    @property
    def d(self) -> int:
        return self._d
    
    @property
    def pub_key(self) -> tuple[int]:
        return (self.alpha, self.e)
    
    @property
    def additional_bits(self):
        return self._additional_bits

    @additional_bits.setter
    def additional_bits(self, value):
        if not isinstance(value, int):
            raise ValueError('additional_bits must be an integer')
        self._additional_bits = value