from time import time
from sys import argv
from functools import partial
from help import is_num, input_check, show_result
from genetic import run_evolution, generate_population, fitness, mutation 
from PIL import Image

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
    # plot_maze(population[0], queens_number)
    return

def plot_maze(genome, board_size: int):
  board = [['0' for _ in range(board_size)]for _ in range(board_size)]
  for i in range(len(genome)):
    board[i][genome[i]] = 'Q'
  colors = {
    '0': (144, 238, 144),  # Light Green for empty slots
    'Q': (0, 0, 0),        # Black for Queens
    '2': (0, 255, 0),      # Green for start
    '3': (255, 0, 0)       # Red for end
  }
  cell_size = 50  # Each cell will be 50x50 pixels

  # Create a new image with the size based on the matrix dimensions
  img_width = len(board[0]) * cell_size
  img_height = len(board) * cell_size
  image = Image.new("RGB", (img_width, img_height))

  # Function to draw each block
  def draw_block(x, y, color):
    for i in range(cell_size):
      for j in range(cell_size):
        image.putpixel((x + i, y + j), color)

  # Loop through the matrix and draw the corresponding color for each cell
  for row in range(len(board)):
    for col in range(len(board[0])):
      # Calculate the top-left corner of the current cell
      x = col * cell_size
      y = row * cell_size

      # Get the color for the current cell
      color = colors[board[row][col]]

      # Draw the block
      draw_block(x, y, color)
  # Save the image
  fileName = "Queen Placement.png"
  image.save(fileName)

#   img = mpimg.imread(fileName)
#   plt.imshow(img)
#   plt.axis('off')
#   plt.show()

main()