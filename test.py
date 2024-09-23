from time import time
from genetic import run_evolution, generate_population, fitness, mutation 
from functools import partial

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import concurrent.futures

test_arg = []

for i in range(5, 15):
    for _ in range(10):
        test_arg.append([i, i, 50, i*2000, 0.1])

n = []
n_time = []

def test(board_width, queens_number, size, generation_limit, mut_chance):
    start_time = time()
    population, generations = run_evolution(
        populate_func=partial(
            generate_population, size = size, genome_length = queens_number, min = 0, max = board_width
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
    if success:
        n.append(queens_number)
        n_time.append(elapsed_time)
    return success, generations, elapsed_time, population[0]

def show_res(res):
    for elem in res:
        print(elem)

def plot_progress_chart():
  plt.plot(n, n_time, label='Time to solve', color='b', marker='o', linestyle='None')  # 'b' for blue, 'o' for markers

  plt.xlabel('Number of queens')
  plt.ylabel('Time to solve')
  plt.title('Time to solve the N-queens problem')

  plt.grid(True)

  plt.legend()

  fileName = "TimeChart"+ str(int(time())) +".png"
  plt.savefig(fileName, format='png')

  # plt.show()

# def run_test():
#     total_success = 0
#     for elem in test_arg:
#         success, generations, elapsed__time, genome = test(elem[0], elem[1], elem[2], elem[3], elem[4])
#         total_success += 1 if success else 0
#         print(success, generations, elapsed__time, genome)
#     print(f"{total_success / len(test_arg) * 100:.1f}% of success")
#     plot_progress_chart()


def run_test():
    total_success = 0

    def run_single_test(elem):
        success, generations, elapsed__time, genome = test(elem[0], elem[1], elem[2], elem[3], elem[4])
        print(success, generations, elapsed__time, genome)
        return success

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(run_single_test, test_arg))

    total_success = sum(1 for result in results if result)

    print(f"{total_success / len(test_arg) * 100:.1f}% of success")
    plot_progress_chart()

run_test()
