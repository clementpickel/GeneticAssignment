from time import time
from genetic import run_evolution, generate_population, fitness, mutation 
from functools import partial
from typing import List
import matplotlib.pyplot as plt
import concurrent.futures

test_start = 4
test_end = 9
test_iteration = 10

test_arg = []

time_chart_n = []
time_chart_n_time = []

success_rate_chart_x = []
success_rate_chart_y = []

for i in range(test_start, test_end):
    success_rate_chart_x.append(i)
    success_rate_chart_y.append(0)
    for _ in range(test_iteration):
        test_arg.append([i, i * 10, i*2000, 0.1])

def test(queens_number, size, generation_limit, mut_chance):
    start_time = time()
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
    score = fitness(population[0])
    success = score == queens_number * (queens_number -1) / 2
    if success:
        time_chart_n.append(queens_number)
        time_chart_n_time.append(elapsed_time)

        success_rate_chart_y[queens_number - test_start] += 1

    return success, generations, elapsed_time, population[0]

def show_res(res):
    for elem in res:
        print(elem)

def plot_chart(x: List[int], y: List[int], title: str, xlabel: str, ylabel: str, ShortFileName: str):
    plt.clf()
    plt.plot(x, y, color='b', marker='o', linestyle='None')  # 'b' for blue, 'o' for markers

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.grid(True)

    #   plt.legend()

    fileName = ShortFileName + str(int(time())) +".png"
    plt.savefig(fileName, format='png')


    # plt.show()

# def run_test(): # old run_test with no multithreading
#     total_success = 0
#     for elem in test_arg:
#         success, generations, elapsed__time, genome = test(elem[0], elem[1], elem[2], elem[3], elem[4])
#         total_success += 1 if success else 0
#         print(success, generations, elapsed__time, genome)
#     print(f"{total_success / len(test_arg) * 100:.1f}% of success")
#     plot_progress_chart()

def compute_success_rate() -> List[int]:
    res = []
    for elem in success_rate_chart_y:
        res.append(elem / test_iteration * 100)
    return res

def run_test():
    total_success = 0

    def run_single_test(elem):
        success, generations, elapsed__time, genome = test(elem[0], elem[1], elem[2], elem[3])
        print("python3 main.py", elem[0], elem[1], elem[2], "=", success, generations, elapsed__time, genome)
        return success

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(run_single_test, test_arg))

    total_success = sum(1 for result in results if result)

    print(f"{total_success / len(test_arg) * 100:.1f}% of success")
    plot_chart(success_rate_chart_x , compute_success_rate(), "N-queens success rate", "Number of queens", "success rate(in %)", "SuccessRate")
    plot_chart(time_chart_n , time_chart_n_time, "Time to solve the N-queens problem", "Number of queens", "Time to solve", "TimeChart")
    print(compute_success_rate())

run_test()
