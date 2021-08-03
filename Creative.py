import pygame
import numpy as np
import sys
from typing import Tuple

# ---------------- GAME IS FURTHER EXPLAINED IN [Writeup.md] -----------------------

# Below are colors representing land, plants, chicken, cow, and food, respectively
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
BEIGE = (245, 245, 220)

class grid:
    gridSize: Tuple[int, int] # columns, rows == x,y
    data: np.ndarray
    generations: int

    def __init__(self, size, setup):
        self.gridSize = size
        self.data = setup(size)
        self.generations = 0

# function: probStart
# purpose: initialize game
# returns: an np array of size size, whose values are selected from range(states) with probabilities
# 0.35, 0.3, 0.2, 0.1, 0.05, and 0 for states 0, 1, 2, 3, 4, and 5, respectively.
def probStart(size):
    return np.random.choice(states, size, p=[0.35,0.3,0.2,0.1,0.05,0])

# function: ruleFood
# purpose: applies rules given a current state and tallies over neighbor states to determine how food in produced.
# returns: a new state based on the rules for a food game given in the write up.
# Note: assumes a six-state game, where 0 is "empty land", 1 is "water", 2 is "plant", 3 is "chicken", 4 is "cow",
# and 5 is "food".
def ruleFood(cell, tallies):
    if cell == 4 or cell == 3:
        if tallies[5] == 0 or tallies[1] == 0:
            return 5
        else:
            return cell
    elif cell == 2:
        if tallies[1] == 0:
            return 5
        else:
            return cell
    elif cell == 0:
        if tallies[4] >= 2:
            return 4
        elif tallies[3] >= 2:
            return 3
        elif tallies[2] >= 1:
            return 2
        else:
            return cell
    else:
        return cell

def neighborSquare(x, y):
    return [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]

def tally_neighbors(grid, position, neighborSet):
    tally=[0 for i in range(states)]
    for neighb in neighborSet(position[0],position[1]):
        nx,ny = neighb
        h,w = grid.gridSize
        if nx in range(w) and ny in range(h):
            state = grid.data[ny][nx]
            tally[state] += 1
    return tally

def evolve(gr, apply_rule, neighbors):
    gr.generations += 1
    copy = np.full(gr.gridSize, gr.data)
    for y in range(np.size(gr.data,0)):
        for x in range(np.size(gr.data,1)):
            copy[y][x] = apply_rule(gr.data[y][x], tally_neighbors(gr,(x,y),neighbors))
    gr.data=copy
    return

def draw_block(x, y, acolor):
    pygame.draw.rect(screen, acolor,[x*(sqSize+pad), y*(sqSize+pad), sqSize, sqSize])
    return

def draw(gr):
    colors = [GREY,BLUE,GREEN,ORANGE,BROWN,BEIGE]
    for y in range(np.size(gr.data, 0)):
        for x in range(np.size(gr.data, 1)):
            draw_block(x, y, colors[gr.data[y][x]])
    return

states = 6
pygame.display.set_caption("Food Production")
g = grid((60,60), probStart)
sqSize = 8
pad = sqSize // 8
s = (g.gridSize[0]*(sqSize+pad),g.gridSize[1]*(sqSize+pad))
screen = pygame.display.set_mode(s)
clock = pygame.time.Clock()

def handleInputEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

frameCount = 0
desiredGifLength = 200
frameRate = 5
frames = []

while True:
    handleInputEvents()
    draw(g)
    evolve(g, ruleFood, neighborSquare)
    pygame.display.flip()
    clock.tick(frameRate)

# Close the window and quit.
pygame.quit()