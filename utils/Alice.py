from random import random as r

class Alice():
    def __init__(self, pub_key:tuple[int], additional_bits:int=4, **kwargs):
        self._pub_key = pub_key
        self._alpha = pub_key[0]
        self._e = pub_key[1]
        self._additional_bits = additional_bits

    def send(self, m:int, code_order:int, **kwargs) -> list[int]:
        def add_additional_bits(m:int, additional_bits:int=4, **kwargs):
            bin_m = bin(m)[2:]
            add_bits = ''.join('1' if r() > 0.5 else '0' for _ in range(additional_bits))
            return int(bin_m + add_bits, 2)
        print(f'A sent {m} to B...')
        bin_m = bin(m)[2:]
        if len(bin_m) > code_order:
            print(f'{m} is too large of a message to send!')
            exit(1)
        m = add_additional_bits(m=m, additional_bits=self.additional_bits)
        m_list = []
        while m > 0:
            m_list.append(min(m, self.alpha - 1))
            m = m - (self.alpha - 1)
        return [m_part**self.e % self.alpha for m_part in m_list]
        
        

    @property
    def alpha(self) -> int:
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if not isinstance(value, int):
            raise ValueError('additional_bits must be an integer')
        self._alpha = value

    @property
    def e(self) -> int:
        return self._e

    @e.setter
    def e(self, value):
        if not isinstance(value, int):
            raise ValueError('e must be an integer')
        self._e = value

    @property
    def additional_bits(self):
        return self._additional_bits

    @additional_bits.setter
    def additional_bits(self, value):
        if not isinstance(value, int):
            raise ValueError('additional_bits must be an integer')
        self._additional_bits = value