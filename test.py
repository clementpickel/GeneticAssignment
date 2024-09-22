from time import time
from genetic import run_evolution, generate_population, fitness, mutation 
from functools import partial

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

test_arg = [
    # [1, 1, 100, 100, 0.1],
    # [1, 2, 50, 2000, 0.1],
    [5, 5, 50, 2000, 0.1],
    [5, 5, 50, 2000, 0.1],
    [5, 5, 50, 2000, 0.1],
    [5, 5, 50, 2000, 0.1],
    [5, 5, 50, 2000, 0.1],
    [6, 6, 50, 2000, 0.1],
    [6, 6, 50, 2000, 0.1],
    [6, 6, 50, 2000, 0.1],
    [6, 6, 50, 2000, 0.1],
    [6, 6, 50, 2000, 0.1],
    [7, 7, 50, 2000, 0.1],
    [7, 7, 50, 2000, 0.1],
    [7, 7, 50, 2000, 0.1],
    [7, 7, 50, 2000, 0.1],
    [7, 7, 50, 2000, 0.1],
    [8, 8, 50, 2000, 0.1],
    [8, 8, 50, 2000, 0.1],
    [8, 8, 50, 2000, 0.1],
    [8, 8, 50, 2000, 0.1],
    [8, 8, 50, 2000, 0.1],
    [9, 9, 50, 5000, 0.1],
    [9, 9, 50, 5000, 0.1],
    [9, 9, 50, 5000, 0.1],
    [9, 9, 50, 5000, 0.1],
    [9, 9, 50, 5000, 0.1],
    [10, 10, 50, 10000, 0.1],
    [10, 10, 50, 10000, 0.1],
    [10, 10, 50, 10000, 0.1],
    [10, 10, 50, 10000, 0.1],
    [10, 10, 50, 10000, 0.1],
]
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
  rand_dict = {}

  # plot graph
  plt.plot(n, n_time, label='Time to solve', color='b', marker='o')  # 'b' for blue, 'o' for markers

  # Adding labels and title
  plt.xlabel('Number of queens')
  plt.ylabel('Time to solve')
  plt.title('Average Distance between Two Points')

  # Adding a grid for better readability
  plt.grid(True)

  # Displaying the legend
  plt.legend()

  # Save the plot as a PNG image
  fileName = "TimeChart"+ str(time()) +".png"
  plt.savefig(fileName, format='png')

  # Display the graph
  # plt.show()

def run_test():
    res = []
    for elem in test_arg:
        success, generations, elapsed__time, genome = test(elem[0], elem[1], elem[2], elem[3], elem[4])
        print(success, generations, elapsed__time, genome)
        # res.append[success, generations, elapsed__time, genome]
    show_res(res)
    plot_progress_chart()

run_test()