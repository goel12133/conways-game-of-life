
import pygame

from collections import Counter

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

cellsize = 5

# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.


# using the example on wikipedia

initial = [
    (6,7),
    (7,7),
    (7,8),
    (7,9),
    (8,9),
    (8,10),
    (9,10),
]

alivecells = set(initial)

# moore neighbours of any cell have their x and y elements always both within a plus minus one range of 
# the cell in question (both cannot be zero however so exclude thiihs case

def moore(cell):
    x, y = cell

    result = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:

            if dx == 0 and dy == 0:
                continue
            result.append((x + dx, y + dy))
    return result

def nextgen(alivecells):
    n_counts = Counter()

    for cell in alivecells:
        for neighbour in moore(cell):
            n_counts[neighbour] += 1  # flip logic since all cells that change state must be next to a living cell
    new_alive = set()

    for cell, count in n_counts.items():   # apply rules
        if cell in alivecells:
            if count == 2 or count == 3:
                new_alive.add(cell)
        else:
            if count == 3:
                new_alive.add(cell)

    return new_alive


# WELL KNOWN INITIAL ALIVE CONFIGs

glider = [
    (1,0),
    (2,1),
    (0,2),
    (1,2),
    (2,2),
]

blinker = [
    (1,0),
    (1,1),
    (1,2),
]

toad = [
    (2,1),
    (3,1),
    (4,1),
    (1,2),
    (2,2),
    (3,2),
]

pulsar = [
    (2,0),(3,0),(4,0),(8,0),(9,0),(10,0),(0,2),(5,2),(7,2),(12,2),
    (0,3),(5,3),(7,3),(12,3),(0,4),(5,4),(7,4),(12,4),
    (2,5),(3,5),(4,5),(8,5),(9,5),(10,5), 
    (2,7),(3,7),(4,7),(8,7),(9,7),(10,7),
    (0,8),(5,8),(7,8),(12,8),
    (0,9),(5,9),(7,9),(12,9),
    (0,10),(5,10),(7,10),(12,10),
    (2,12),(3,12),(4,12),(8,12),(9,12),(10,12),
]

gosper = [
    (1,5),(1,6),(2,5),(2,6),(11,5),(11,6),(11,7),(12,4),(12,8), (13,3),(13,9),(14,3),(14,9),
    (15,6),(16,4),(16,8),(17,5),(17,6),(17,7),(18,6),(21,3),(21,4),(21,5),(22,3),(22,4),(22,5),
    (23,2),(23,6),(25,1),(25,2),(25,6),(25,7),(35,3),(35,4),(36,3),(36,4),
]

arrangements = {
    pygame.K_1: glider,
    pygame.K_2: blinker,
    pygame.K_3: toad,
    pygame.K_4: pulsar,
    pygame.K_5: gosper,
}

paused = True
gen = 0

def center(arrangement):
    grid_width = 1280 // cellsize
    grid_height = 720 // cellsize

    pattern_width = max(x for x, y in arrangement)
    pattern_height = max(y for x, y in arrangement)

    dx = grid_width // 2 - pattern_width // 2
    dy = grid_height // 2 - pattern_height // 2

    return {(x + dx, y + dy) for x, y in arrangement}


# https://www.pygame.org/docs/

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_n and paused: # press N key to go one by one 
                alivecells = nextgen(alivecells)
                gen += 1
            if event.key in arrangements:
                alivecells = center(arrangements[event.key])
                gen = 0
                paused = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            cell = (mx // cellsize, my // cellsize)

            if cell in alivecells:
                alivecells.remove(cell)
            else:
                alivecells.add(cell)

    if not paused:
        alivecells = nextgen(alivecells)
        gen += 1

    screen.fill("black")

    # gridlines
    for x in range(0, 1280, cellsize):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, 720))

    for y in range(0, 720, cellsize):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (1280, y))

    # alive 
    for x, y in alivecells:
        pygame.draw.rect(
            screen,
            "white",
            (x * cellsize, y * cellsize, cellsize, cellsize)
        )

    pygame.display.set_caption(
        f"Game of Life | Generation {gen} | Cells {len(alivecells)} | {'Paused' if paused}"
    )

    pygame.display.flip()

    clock.tick(5) # five gen per sec

pygame.quit()


