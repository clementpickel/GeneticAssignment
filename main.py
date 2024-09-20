#!/usr/bin/python3

from typing import List, Callable, Tuple
from random import choices, randint, randrange, random, choice
from functools import partial
from sys import argv
from time import time

from help import help, show_result, is_num, input_check

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

            if y1 != y2 and y2 - y1 != x2 - x1 and y2 - y1 != x1 - x2: # check vertical, horizontal and diagonals
                score += 1
    return score
            
def selection_pair(population) -> Population:
    return get_population(choices(
        population=population,
        weights=[genome[1] for genome in population],
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

    for i in range(generation_limit):
        population = create_fitness(population)
        population = sort_fitness(population)
        if population[0][1] >= fitness_limit:
            population = get_population(population)
            breacked = True
            break

        next_generation = [population[0][0], population[1][0]] # elitism

        if len(population) > 20: 
            next_generation += populate_func(size=2) # immigration

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

def main():
    start_time = time()
    if (len(argv) == 2 and argv[1] == "-h" or len(argv) < 4):
        help()
        return
    queens_number = is_num(argv[1])
    size = is_num(argv[2])
    generation_limit = is_num(argv[3])
    mut_chance = 0.1
    if len(argv) >= 6:
        mut_chance = float(argv[4])

    input_check(queens_number, size, generation_limit)

    population, generations = run_evolution(
        populate_func=partial(
            generate_population, size = size, genome_length = queens_number, min = 0, max = queens_number
        ),
        fitness_func=fitness,
        fitness_limit=queens_number * (queens_number - 1) / 2, # summ from 0 to queens_number,
        mutation_func=partial(
            mutation, min = 0, max = queens_number - 1, probability=mut_chance
        ),
        generation_limit=generation_limit
    )
    elapsed_time = time() - start_time
    show_result(population[0], generations, queens_number, queens_number, fitness(population[0]), elapsed_time)
    return

main()
