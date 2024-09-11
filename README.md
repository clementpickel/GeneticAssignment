# GeneticAssignment

Create a genetic algorithm to solve the n-queens / TSP / any problem we want.
genome representation = [X,Y x the number of queens]

github:
https://github.com/clementpickel/GeneticAssignment

sources:
https://www.youtube.com/watch?v=uQj5UNhCPuo
https://www.youtube.com/watch?v=nhT56blfRpE
https://stackoverflow.com/questions/41432956/checking-for-horizontal-vertical-and-diagonal-pairs-given-coordinates
https://www.educative.io/answers/solving-the-8-queen-problem-using-genetic-algorithm

steps:
change genome from position in the board in binary to position X, Y
the genetic algorithm converge to a solution with 2 pieces or more at the same place to remove a queen
we change the fitness function from counting the number of non attacking queen to non attacking pair
we change the mutation from +/- 1 to a random between 0 and board_size
