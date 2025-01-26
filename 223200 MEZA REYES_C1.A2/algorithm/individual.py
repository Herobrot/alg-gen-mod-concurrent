import random


class Individual:
    def __init__(self, bits, n_points):
        self.bits = bits
        self.binary = self._generate_random_binary(n_points)

    @classmethod
    def from_binary(cls, binary, bits):
        instance = cls(bits, 2**bits)
        instance.binary = binary
        return instance

    def _generate_random_binary(self, n_points):
        decimal = random.randint(0, n_points - 1)
        return f"{decimal:0{self.bits}b}"

    def mutate(self, bit_mutation_rate):
        mutated = list(self.binary)
        for bit in range(len(mutated)):
            if random.random() < bit_mutation_rate:
                mutated[bit] = "1" if mutated[bit] == "0" else "0"
        self.binary = "".join(mutated)
