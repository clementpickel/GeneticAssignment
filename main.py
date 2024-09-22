from time import time
from sys import argv
from functools import partial
from help import is_num, input_check, show_result
from genetic import run_evolution, generate_population, fitness, mutation 

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