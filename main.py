#!/usr/bin/python3

from typing import List, Callable, Tuple
from random import choices, randint, randrange, random
from functools import partial
from sys import argv

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]

def generate_genome(length: int, min: int, max: int) -> Genome:
    return [randint(min, max-1) for _ in range(length)]
    
def generate_population(size: int, genome_length: int, min: int, max: int) -> Population:
    return  [generate_genome(genome_length, min, max) for _ in range(size)]

def fitness(genome: Genome) -> int:
    if len(genome)%2 != 0:
        raise ValueError("genome must be [X,Y, ...]")
    
    queens_co = []
    score = len(genome)
    for i in range(0, len(genome), 2):
        queens_co.append([genome[i], genome[i+1]])

    for i in range(len(queens_co)):
        for j in range(len(queens_co)):
            if i != j:
                q1 = queens_co[i]
                q2 = queens_co[j]
                if q1[0] == q2[0] and q2[0] == q1[0]:
                    score -= 2

                if q1[0] != q2[0] and q1[1] != q2[1] and q2[1] - q1[1] != q2[0] - q1[0] and q2[1] - q1[1] != q1[0] - q2[0]:
                    score += 1
    return score / 2
            
def selection_pair(population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )

def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genome a and b must be of same length")
    
    length = len(a)
    p = randint(2, length - 2)
    if p % 2 != 0: # only cut so to leave X,Y together
        p -= 1
    return a[0:p] + b[p:], b[0:p] + a[p:]

def mutation(genome: Genome, min: int, max: int, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        if random() < probability:
            genome[index] = randint(min, max-1)
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
        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = [population[0], population[1]] # elitism

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

def show_board(genome: Genome, board_size: int):
    board = [['_' for _ in range(board_size)]for _ in range(board_size)]
    for i in range(0, len(genome), 2):
        board[genome[i+1]][genome[i]] = 'Q'
    for line in board:
        for char in line:
            print(char, end=" ")
        print("")

def show_result(genome: Genome, generation: int, board_width: int, queens_number: int):
    print("result =", genome)
    print("generation =", generation)
    show_board(genome, board_width)
    if fitness(genome) != queens_number * (queens_number + 1) / 2:
        print("Not a solution, limit reached")

def is_num(str):
    try:
        int(str)
    except ValueError:
        exit(84)
    return int(str)

def help():
    print("""python3 main.py B Q S L
          B = board width
          Q = number of queens
          S = size of the population
          L = generation limit
""")

def main():
    if (len(argv) == 2 and argv[1] == "-h" or len(argv) != 5):
        help()
        return
    board_width = is_num(argv[1])
    queens_number = is_num(argv[2])
    size = is_num(argv[3])
    generation_limit = is_num(argv[4])

    population, generations = run_evolution(
        populate_func=partial(
            generate_population, size = size, genome_length = queens_number * 2, min = 0, max = board_width
        ),
        fitness_func=fitness,
        fitness_limit=queens_number * (queens_number + 1) / 2, # summ from 0 to queens_number,
        mutation_func=partial(
            mutation, min = 0, max = board_width - 1
        ),
        generation_limit=generation_limit
    )
    show_result(population[0], generations, board_width, queens_number)
    return

main()