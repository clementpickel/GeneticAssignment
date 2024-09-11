from typing import List, Callable, Tuple
from random import choices, randint, randrange, random, shuffle
from functools import partial

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]

def generate_genome(length: int, queens_number: int) -> Genome:
    genome = [1] * queens_number + [0] * (length - queens_number)
    shuffle(genome)
    return genome

def generate_population(size: int, genome_length: int, queens_number: int) -> Population:
    return [generate_genome(genome_length, queens_number) for _ in range(size)]

# can probably be upgraded
def fitness(genome: Genome, board_size: int) -> int:
    if len(genome) != board_size:
        raise ValueError("genome and board must be of the same length")

    queens_co = []
    score = genome.count(1)
    for i in range(len(genome)):
        if genome[i] == 1:
            queens_co.append((i % board_size, int(i / board_size)))

    for q1 in queens_co:
        for q2 in queens_co:
            if q1[0] == q2[0]:
                score -= 1
            elif q1[1] == q2[1]:
                score -= 1
            elif q2[1] - q1[1] == q2[0] - q1[0]:
                score -= 1
            elif q2[1] - q1[1] == q1[0] - q2[0]:
                score -= 1
    return score
            
def selection_pair(population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )

# need modification, need to remove a queen for every queen added
def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genome a and b must be of same length")
    
    length = len(a)
    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

# need modifications, need to remove a queen for every queen added
def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    return genome

def run_evolution(
      populate_func: PopulateFunc,
      fitness_func: FitnessFunc,
      fitness_limit: int,
      selection_func: SelectionFunc = selection_pair,
      crossover_func: CrossoverFunc = single_point_crossover,
      mutation_func: MutationFunc = mutation,
      generation_limit: int = 100
) -> Tuple[Population, int]:
    population = populate_func()

    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )
        if fitness_func(population[0]) >= fitness_limit: # we calculate 2 time the fitness function of the best, can be improved
            break

        next_generation = population[0, 2] # elitism

        for _ in range(int(len(population) / 2) - 1):
            parent = selection_func(population, fitness_func)
            offsping_a, offspring_b = crossover_func(parent[0], parent[1])
            offsping_a = mutation_func(offsping_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offsping_a, offspring_b]
        
        population = next_generation
    
    population = sorted(
        population,
        key=lambda genome: fitness_func(genome),
        reverse=True
    )

    return population, i


board_width = 4
queens_number = 4
population, generations = run_evolution(
    populate_func=partial(
        generate_population, size = 20, genome_length = board_width**2, queens_number = queens_number
    ),
    fitness_func=partial(
        fitness, board_size = board_width**2
    ),
    fitness_limit=queens_number
)

print(population[0], generations)