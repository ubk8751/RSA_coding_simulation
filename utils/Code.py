import itertools
import pickle

class Code():
    def __init__(self, code_order):
        self._code_order = code_order
        self._code = []
    
    def gen_code(self, code_order:int, min_distance:int, **kwargs):
        def distance(word1, word2):
            """Calculate the Hamming distance between two bit strings."""
            return sum(c1 != c2 for c1, c2 in zip(word1, word2))

        def filter_code(code:list[tuple[int]], min_distance:int):
            """
            Filter a list of code words to ensure that each has at least a `min_distance`
            Hamming distance from each other.

            :param code: List of bit strings (tuples of 0s and 1s).
            :param min_distance: The minimum required Hamming distance.
            :return: A list of bit strings that satisfy the minimum distance requirement.
            """
            filtered = []

            for bit_string in code:
                if all(distance(bit_string, selected) >= min_distance for selected in filtered):
                    filtered.append(''.join(str(num) for num in bit_string))
            return filtered
        
        print("Generating new code...")
        self.code_order = code_order
        unfiltered_code = list(itertools.product([0, 1], repeat=code_order))
        self.code = filter_code(code=unfiltered_code, min_distance=min_distance)


    def save(self):
        file = open(f'{self.__class__.__name__ }.pkl', 'wb')
        file.write(pickle.dumps(self.__dict__))
        file.close()
    
    def load(self):
        file = open(f'{self.__class__.__name__ }.pkl', 'rb')
        data_pickle = file.read()
        self.__dict__ = pickle.loads(data_pickle)
        file.close()

    def check_value(self, value:str, **kwargs):
        if value in self.code:
            return True
        return False

    @property
    def code(self):
        return self._code

    @property
    def code_order(self):
        return self._code_order
    
    @code_order.setter
    def code_order(self, value):
        if not isinstance(value, int):
            raise ValueError("code_order must be an integer")
        self._code_order = value
    
    @code.setter
    def code(self, value):
        if (not isinstance(value, list) or
            not isinstance(value[0], str)):
            raise ValueError("code must be of type list[tuple[int]]!")
        self._code = value
