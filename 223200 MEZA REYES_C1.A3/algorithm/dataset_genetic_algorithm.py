import numpy as np
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

class GeneticAlgorithm:
    def __init__(self, dataset, iterations, population_size, crossover_rate, mutation_rate, 
                 min_interval_mutation_rate, max_interval_mutation_rate, num_workers=4):
        self.dataset = dataset
        self.iterations = iterations
        self.population_size = int(population_size)
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.min_interval_mutation_rate = min_interval_mutation_rate
        self.max_interval_mutation_rate = max_interval_mutation_rate
        self.num_workers = num_workers
                
        self.yd = dataset[:, -1]
        self.X = dataset[:, 1:-1]
                
        self.best_solutions = []
        self.yc_per_generation = []
        self.population = self.initialize_population()
                
        self.evolution_lock = threading.Lock()
        self.results_lock = threading.Lock()
        self.generation_complete = threading.Event()
        self.fitness_queue = Queue()

    def initialize_population(self):
        rng = np.random.default_rng(int(time.time()))
        num_features = self.X.shape[1]
        return rng.uniform(-1, 1, size=(self.population_size, num_features + 1))

    def fitness_function(self, individual):
        yc = np.dot(self.X, individual[1:]) + individual[0]
        error_vector = self.yd - yc
        return np.abs(error_vector).mean()

    def calculate_fitness_batch(self, individuals):
        return [(self.fitness_function(ind), ind) for ind in individuals]

    def mutate(self, individual):
        mutated_individual = individual.copy()
        num_genes = len(individual)
        num_mutations = int(self.mutation_rate * num_genes)
        
        if num_mutations > 0:
            genes_to_mutate = random.sample(range(num_genes), num_mutations)
            for gene in genes_to_mutate:
                mutation_value = random.uniform(self.min_interval_mutation_rate, 
                                             self.max_interval_mutation_rate)
                gene_transform = random.choice([-1, 1])
                mutated_individual[gene] += gene_transform * mutation_value
        
        return mutated_individual

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(1, len(parent1) - 1)
            offspring = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        else:
            offspring = parent1.copy()
        return offspring

    def parallel_fitness_calculation(self, population):
        batch_size = max(1, len(population) // self.num_workers)
        population_batches = [
            population[i:i + batch_size] 
            for i in range(0, len(population), batch_size)
        ]
        
        fitness_scores = []
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            future_to_batch = {
                executor.submit(self.calculate_fitness_batch, batch): batch 
                for batch in population_batches
            }
            
            for future in as_completed(future_to_batch):
                fitness_scores.extend(future.result())
        
        return sorted(fitness_scores, key=lambda x: x[0])

    def evolve_population(self):
        with self.evolution_lock:            
            fitness_scores = self.parallel_fitness_calculation(self.population)
                        
            selected_population = [ind for _, ind in fitness_scores[:self.population_size // 2]]
                        
            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(selected_population, 2)
                                
                offspring = self.crossover(parent1, parent2)
                offspring = self.mutate(offspring)
                new_population.append(offspring)
            
            self.population = np.array(new_population)
                        
            with self.results_lock:
                self.best_solutions.append(fitness_scores[0])
                best_individual = fitness_scores[0][1]
                yc = np.dot(self.X, best_individual[1:]) + best_individual[0]
                self.yc_per_generation.append(yc)

    def run(self):
        progress_queue = Queue()
        
        def evolution_worker():
            for gen in range(self.iterations):
                self.evolve_population()
                progress_queue.put((gen, self.best_solutions[-1][0]))
        
        evolution_thread = threading.Thread(target=evolution_worker)
        evolution_thread.start()
        
        completed_generations = 0
        while completed_generations < self.iterations:
            gen, fitness = progress_queue.get()
            completed_generations += 1
            print(f"Generación {gen + 1}: Mejor Fitness = {fitness}")
        
        evolution_thread.join()
        return self.best_solutions[-1][1]

    def get_yd(self):
        return self.yd

    def get_yc(self, generation=None):
        with self.results_lock:
            if generation is None:
                generation = len(self.yc_per_generation) - 1
            return self.yc_per_generation[generation]

    def get_best_solutions(self):
        with self.results_lock:
            return self.best_solutions.copy()