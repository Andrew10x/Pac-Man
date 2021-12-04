from math import inf
from minimax import GameState, genTree, minimax

maze = [
    [1, 1, 5, 1, 0],
    [1, 0, 0, 1, 1],
    [1, 0, 0, 2, 0],
    [1, 1, 6, 0, 0],
    [0, 0, 0, 1, 0]]

state = GameState(maze)
tree = genTree(state, (3, 2))
bestScore = minimax(tree, -inf, inf, 2)
print(tree)
print(bestScore)