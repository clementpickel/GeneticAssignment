from time import time
from main import run_evolution, generate_population, fitness, mutation 
from functools import partial

test_arg = [
    # [1, 1, 100, 100, 0.1],
    # [1, 2, 300, 2000, 0.1],
    [5, 5, 300, 2000, 0.1],
    [5, 5, 300, 2000, 0.1],
    [6, 6, 300, 2000, 0.1],
    [6, 6, 300, 2000, 0.1],
    [8, 8, 300, 2000, 0.1],
    [8, 8, 300, 2000, 0.1],
    [9, 9, 300, 2000, 0.1],
    [9, 9, 300, 2000, 0.1],
    [10, 10, 300, 2000, 0.1],
    [10, 10, 300, 2000, 0.1],
    [12, 12, 300, 2000, 0.1],
    [12, 12, 300, 2000, 0.1],
]

def test(board_width, queens_number, size, generation_limit, mut_chance):
    start_time = time()
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
    elapsed_time = time() - start_time
    score = fitness(population[0])
    success = score == queens_number * (queens_number -1) / 2
    
    return success, generations, elapsed_time, population[0]

def show_res(res):
    for elem in res:
        print(elem)

def run_test():
    res = []
    for elem in test_arg:
        success, generations, elapsed__time, genome = test(elem[0], elem[1], elem[2], elem[3], elem[4])
        print(success, generations, elapsed__time, genome)
        # res.append[success, generations, elapsed__time, genome]
    show_res(res)

run_test()