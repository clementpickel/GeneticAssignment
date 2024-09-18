#!/usr/bin/python3

from typing import List, Callable, Tuple
from random import choices, randint, randrange, random, choice
from functools import partial
from sys import argv, stderr

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]

# def generate_genome(length: int, min: int, max: int) -> Genome:
#     return [randint(min, max-1) for _ in range(length)]

# add constraint based initialisation but it kinda defeat the point so idk if i should use it
def generate_genome(length: int, min: int, max: int) -> Genome:
    res = []
    already_used_x = []
    already_used_y = []
    for _ in range(int(length / 2)):
        allowed_numbers_x = [i for i in range(min, max) if i not in already_used_x]
        allowed_numbers_y = [i for i in range(min, max) if i not in already_used_y]
        x = choice(allowed_numbers_x)
        y = choice(allowed_numbers_y)

        already_used_x.append(x)
        already_used_y.append(y)
        res.append(x)
        res.append(y)
        
    return res

def generate_population(size: int, genome_length: int, min: int, max: int) -> Population:
    return  [generate_genome(genome_length, min, max) for _ in range(size)]

def fitness(genome: Genome) -> int:
    if len(genome)%2 != 0:
        raise ValueError("genome must be [X,Y, ...]")
    
    score = 0

    for i in range(0, len(genome), 2):
        for j in range(i + 2, len(genome), 2):
            q1 = (genome[i], genome[i+1])
            q2 = (genome[j], genome[j+1])

            if q1[0] == q2[0] and q1[1] == q2[1]: # decrease score if 2 queens have the same coordinates
                score -= 2

            if q1[0] != q2[0] and q1[1] != q2[1] and q2[1] - q1[1] != q2[0] - q1[0] and q2[1] - q1[1] != q1[0] - q2[0]: # check vertical, horizontal and diagonals
                score += 1
    return score
            
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

def mutation(genome: Genome, min: int, max: int, num: int = 1, probability: float = 0.10) -> Genome:
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
    if fitness(genome) != queens_number * (queens_number - 1) / 2:
        print("Not a solution, generation limit reached, fitness =", fitness(genome), "/", queens_number * (queens_number - 1) / 2)

def is_num(str):
    try:
        int(str)
    except ValueError:
        exit(84)
    return int(str)

def help():
    print("""python3 main.py B Q P L (M)
          B = board width
          Q = number of queens
          P = size of the population
          L = generation limit
          M = mutation chance, 0.1 by default""")
    
def input_check(board_width: int, queens_number: int, population: int, gen_lim: int):
    if board_width < 1:
        print("Board too small", file=stderr)
        exit(84)
    if queens_number < 1:
        print("Not enough queens", file=stderr)
        exit(84)
    if population < 2:
        print("Population too small", file=stderr)
        exit(84)
    if gen_lim < 1:
        print("Not enough generations", file=stderr)
        exit(84)
    if queens_number > board_width:
        print("I mean.. you can try...")

def main():
    if (len(argv) == 2 and argv[1] == "-h" or len(argv) < 5):
        help()
        return
    board_width = is_num(argv[1])
    queens_number = is_num(argv[2])
    size = is_num(argv[3])
    generation_limit = is_num(argv[4])
    mut_chance = 0.1
    if len(argv) >= 6:
        mut_chance = float(argv[5])

    input_check(board_width, queens_number, size, generation_limit)

    population, generations = run_evolution(
        populate_func=partial(
            generate_population, size = size, genome_length = queens_number * 2, min = 0, max = board_width
        ),
        fitness_func=fitness,
        fitness_limit=queens_number * (queens_number - 1) / 2, # summ from 0 to queens_number,
        mutation_func=partial(
            mutation, min = 0, max = board_width - 1, probability=mut_chance
        ),
        generation_limit=generation_limit
    )
    show_result(population[0], generations, board_width, queens_number)
    return

main()