#!/usr/bin/python3

from typing import List, Callable, Tuple
from random import choices, randint, randrange, random

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]

def generate_genome_1(length: int, min: int, max: int) -> Genome:
    return [randint(min, max-1) for _ in range(length)]

def generate_population(size: int, genome_length: int, min: int, max: int) -> Population:
    return  [generate_genome_1(genome_length, min, max) for _ in range(size)]

def fitness(genome: Genome) -> int:
    score = 0

    for i in range(len(genome)):
        x1, y1 = i, genome[i]
        for j in range(i + 1, len(genome)):
            x2, y2 = j, genome[j]

            if y1 != y2 and y2 - y1 != x2 - x1 and y2 - y1 != x1 - x2: # check vertical and diagonals
                score += 1
    return score

def selection_pair(population) -> Population:
    return get_population(choices(
        population=population,
        weights=[pair[1] for pair in population],
        k=2
    ))

def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genome a and b must be of same length")
    
    length = len(a)
    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

def mutation(genome: Genome, min: int, max: int, num: int = 1, probability: float = 0.10) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        if random() < probability:
            genome[index] = randint(min, max-1)
    return genome

def create_fitness(pop: Population):
    res = []
    for elem in pop:
        res.append([elem, fitness(elem)])
    return res

def sort_fitness(list):
    return sorted(
        list,
        key=lambda elem: elem[1],
        reverse=True
    )

def get_population(list):
    res = []
    for elem in list:
        res.append(elem[0])
    return res

def run_evolution(
      populate_func: PopulateFunc,
      fitness_func: FitnessFunc,
      fitness_limit: int,
      selection_func: SelectionFunc = selection_pair,
      crossover_func: CrossoverFunc = single_point_crossover,
      mutation_func: MutationFunc = mutation,
      generation_limit: int = 100
) -> Tuple[Population, int]:
    breacked = False
    population = populate_func()
    # old_fitness = 0
    # turn_with_same_fitness = 0

    for i in range(generation_limit):
        population = create_fitness(population) # go from [[int]] to [[[int], int]], bad practice
        population = sort_fitness(population)

        if population[0][1] >= fitness_limit:
            population = get_population(population)
            breacked = True
            break
        
        # if old_fitness == population[0][1]:
        #     turn_with_same_fitness += 1
        # else :
        #     old_fitness = population[0][1]
        #     turn_with_same_fitness = 0
        
        # if turn_with_same_fitness >= int(0.15 * generation_limit): # if fitness doens't change for 15% of gen: stop
        #     population = get_population(population)                # greatly decrease success rate for large N so we removed it
        #     breacked = True
        #     break
        
        next_generation = [population[0][0], population[1][0]] # elitism, keep the best 2 for the next generatoin

        if len(population) > 20: 
            next_generation += populate_func(size=2) # immigration, inroduce 2 new random genome

        for _ in range(int(len(population) / 2) - 2 if len(population) > 20 else 1):
            parent = selection_func(population)
            offsping_a, offspring_b = crossover_func(parent[0], parent[1])
            offsping_a = mutation_func(offsping_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offsping_a, offspring_b]

        population = next_generation
    
    if not breacked:
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )

    return population, i

