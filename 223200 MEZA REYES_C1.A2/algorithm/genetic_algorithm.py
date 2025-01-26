import random
import math
import threading
from concurrent.futures import ThreadPoolExecutor
from .individual import Individual
from .fitness_function import FitnessFunction
from enum import Enum

class PairingStrategy(Enum):
    RANDOM = "random"
    QUARTER_ALL = "quarter_all"

class CrossoverStrategy(Enum):
    SINGLE_POINT = "single_point"
    COMPLETE_HYBRID = "complete_hybrid"

class MutationStrategy(Enum):
    RANDOM_BIT = "random_bit"
    COMPLEMENT = "complement"

class PruningStrategy(Enum):
    PROPORTIONAL = "proportional"
    BEST_ONLY = "best_only"

class GeneticAlgorithm:
    def __init__(
        self,
        delta,
        min_val,
        max_val,
        iteration,
        pop_max,
        pop_min,
        crossover_rate,
        mutation_rate,
        bit_mutation_rate,
        pairing_strategy=PairingStrategy.QUARTER_ALL,
        crossover_strategy=CrossoverStrategy.COMPLETE_HYBRID,
        mutation_strategy=MutationStrategy.COMPLEMENT,
        pruning_strategy=PruningStrategy.BEST_ONLY
    ):
        self.delta = delta
        self.interval = [min_val, max_val]
        self.iteration = iteration
        self.population = []
        self.pop_max = pop_max
        self.pop_min = pop_min
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.bit_mutation_rate = bit_mutation_rate
        self.fitness = []
        self.n_points = math.ceil((max_val - min_val) / delta) + 1
        self.bits = math.ceil(math.log2(self.n_points))
        self.lock = threading.Lock()
        self.delta_system = (self.interval[1] - self.interval[0]) / (2**self.bits - 1)
        self.fitness_function = FitnessFunction()
        self.best_solution = None
        self.best_fitness = float("-inf")
        self.best_x = None
        self.worse_solution = None
        self.worse_fitness = float("inf")
        self.worse_x = None

        self.pairing_strategy = pairing_strategy
        self.crossover_strategy = crossover_strategy
        self.mutation_strategy = mutation_strategy
        self.pruning_strategy = pruning_strategy

    def initialize_population(self):
        with ThreadPoolExecutor() as executor:
            individuals = [
                Individual(self.bits, self.n_points) for _ in range(int(self.pop_max))
            ]

            self.population = individuals
            self.fitness = list(
                executor.map(
                    lambda ind: self.fitness_function.calculate(
                        self._decode_individual(ind.binary)
                    ),
                    self.population,
                )
            )

    def _decode_individual(self, binary):
        index = int(binary, 2)
        return self.interval[0] + index * self.delta_system

    def adjust_population_size(self, iteration):
        target_size = int(
            self.pop_min
            + (self.pop_max - self.pop_min)
            * ((self.iteration - iteration) / self.iteration)
        )

        with self.lock:
            if len(self.population) > target_size:
                if self.pruning_strategy == PruningStrategy.PROPORTIONAL:
                    self._proportional_pruning(target_size)
                elif self.pruning_strategy == PruningStrategy.BEST_ONLY:
                    self._best_only_pruning(target_size)

    def evolve(self, current_iteration):
        with ThreadPoolExecutor() as executor:
            new_population = []
            for _ in range(len(self.population) // 2):
                parent1, parent2 = self._select_parents()
                child1, child2 = self._crossover(parent1, parent2)
                new_population.extend([child1, child2])

            new_fitness = list(
                executor.map(
                    lambda ind: self.fitness_function.calculate(
                        self._decode_individual(ind.binary)
                    ),
                    new_population,
                )
            )

        with self.lock:
            self._update_population(
                new_population[: len(self.population)],
                new_fitness[: len(self.population)],
            )
            self._update_best_and_worst()

        self.adjust_population_size(current_iteration)

    def _select_parents(self):
        if self.pairing_strategy == PairingStrategy.RANDOM:
            return self._select_parents_random()
        elif self.pairing_strategy == PairingStrategy.QUARTER_ALL:
            return self._select_parents_quarter_all()

    def _select_parents_random(self):
        total_fitness = sum(self.fitness)
        probabilities = [fit / total_fitness for fit in self.fitness]
        parents = random.choices(self.population, weights=probabilities, k=2)
        return parents
    
    def _select_parents_quarter_all(self):
        quarter_size = len(self.population) // 4
        selected_quarter = random.sample(self.population, quarter_size)

        all_combinations = [
            (ind1, ind2) 
            for i, ind1 in enumerate(selected_quarter) 
            for ind2 in selected_quarter[i + 1:]
        ]
        
        selected_pairs = [
            pair for pair in all_combinations if random.random() < self.crossover_rate
        ]
        
        if not selected_pairs:
            raise ValueError("No se encontraron pares válidos para la cruza.")

        return random.choice(selected_pairs)



    def _crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            if self.crossover_strategy == CrossoverStrategy.SINGLE_POINT:
                return self._single_point_crossover(parent1, parent2)
            elif self.crossover_strategy == CrossoverStrategy.COMPLETE_HYBRID:
                return self._complete_hybrid_crossover(parent1, parent2)
        return parent1, parent2

    def _single_point_crossover(self, parent1, parent2):
        point = random.randint(1, self.bits - 1)
        child1_binary = parent1.binary[:point] + parent2.binary[point:]
        child2_binary = parent2.binary[:point] + parent1.binary[point:]
        child1 = Individual.from_binary(child1_binary, self.bits)
        child2 = Individual.from_binary(child2_binary, self.bits)

        self._apply_mutation(child1)
        self._apply_mutation(child2)

        return child1, child2
    
    def _complete_hybrid_crossover(self, parent1, parent2):
        child1_binary = ""
        child2_binary = ""

        for i in range(self.bits):
            if i % 2 == 0: 
                child1_binary += parent2.binary[i]
                child2_binary += parent1.binary[i]
            else:
                child1_binary += parent1.binary[i]
                child2_binary += parent2.binary[i]
        
        child1 = Individual.from_binary(child1_binary, self.bits)
        child2 = Individual.from_binary(child2_binary, self.bits)
        
        self._apply_mutation(child1)
        self._apply_mutation(child2)

        return child1, child2

    
    def _apply_mutation(self, individual):
        if random.random() < self.mutation_rate:
            if self.mutation_strategy == MutationStrategy.RANDOM_BIT:
                individual.mutate(self.bit_mutation_rate)
            elif self.mutation_strategy == MutationStrategy.COMPLEMENT:
                self._complement_mutation(individual)

    def _complement_mutation(self, individual):
        if random.random() < self.mutation_rate:
            binary_list = list(individual.binary)
            for i in range(len(binary_list)):
                if random.random() < self.bit_mutation_rate:
                    binary_list[i] = '1' if binary_list[i] == '0' else '0'
            individual.binary = ''.join(binary_list)

    def _proportional_pruning(self, target_size):
        total_fitness = sum(self.fitness)
        probabilities = [fit / total_fitness for fit in self.fitness]
                
        selected_indices = random.choices(
            range(len(self.population)),
            weights=probabilities,
            k=target_size
        )
                
        new_population = [self.population[i] for i in selected_indices]
        new_fitness = [self.fitness[i] for i in selected_indices]
        
        self.population = new_population
        self.fitness = new_fitness

    def _best_only_pruning(self, target_size):
        unique_pairs = {}
        for ind, fit in zip(self.population, self.fitness):
            unique_pairs[str(ind)] = (ind, fit)

        sorted_pairs = sorted(
            unique_pairs.values(), 
            key=lambda x: x[1], 
            reverse=True
        )[:target_size]

        self.population, self.fitness = zip(*sorted_pairs)
        self.population = list(self.population)
        self.fitness = list(self.fitness)

    def _update_population(self, new_population, new_fitness):
        self.population = new_population
        self.fitness = new_fitness

    def _update_best_and_worst(self):
        current_best_idx = max(range(len(self.fitness)), key=lambda i: self.fitness[i])
        current_best_fitness = self.fitness[current_best_idx]
        current_best_x = self._decode_individual(
            self.population[current_best_idx].binary
        )

        current_worse_idx = min(range(len(self.fitness)), key=lambda i: self.fitness[i])
        current_worse_fitness = self.fitness[current_worse_idx]
        current_worse_x = self._decode_individual(
            self.population[current_worse_idx].binary
        )

        if current_best_fitness > self.best_fitness:
            self.best_fitness = current_best_fitness
            self.best_solution = self.population[current_best_idx]
            self.best_x = current_best_x

        if current_worse_fitness < self.worse_fitness:
            self.worse_fitness = current_worse_fitness
            self.worse_solution = self.population[current_worse_idx]
            self.worse_x = current_worse_x

    def get_decoded_population(self):
        return [
            (self._decode_individual(ind.binary), fit)
            for ind, fit in zip(self.population, self.fitness)
        ]
