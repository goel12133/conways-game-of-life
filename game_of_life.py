from collections import Counter

import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 5
GENERATIONS_PER_SECOND = 5

GLIDER = [
    (1, 0),
    (2, 1),
    (0, 2),
    (1, 2),
    (2, 2),
]

BLINKER = [
    (1, 0),
    (1, 1),
    (1, 2),
]

TOAD = [
    (2, 1),
    (3, 1),
    (4, 1),
    (1, 2),
    (2, 2),
    (3, 2),
]

PULSAR = [
    (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
    (0, 2), (5, 2), (7, 2), (12, 2),
    (0, 3), (5, 3), (7, 3), (12, 3),
    (0, 4), (5, 4), (7, 4), (12, 4),
    (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
    (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7),
    (0, 8), (5, 8), (7, 8), (12, 8),
    (0, 9), (5, 9), (7, 9), (12, 9),
    (0, 10), (5, 10), (7, 10), (12, 10),
    (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12),
]

GOSPER = [
    (1, 5), (1, 6), (2, 5), (2, 6),
    (11, 5), (11, 6), (11, 7),
    (12, 4), (12, 8),
    (13, 3), (13, 9),
    (14, 3), (14, 9),
    (15, 6),
    (16, 4), (16, 8),
    (17, 5), (17, 6), (17, 7),
    (18, 6),
    (21, 3), (21, 4), (21, 5),
    (22, 3), (22, 4), (22, 5),
    (23, 2), (23, 6),
    (25, 1), (25, 2), (25, 6), (25, 7),
    (35, 3), (35, 4),
    (36, 3), (36, 4),
]

ARRANGEMENTS = {
    pygame.K_1: GLIDER,
    pygame.K_2: BLINKER,
    pygame.K_3: TOAD,
    pygame.K_4: PULSAR,
    pygame.K_5: GOSPER,
}


def moore(cell):
    x, y = cell
    result = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            result.append((x + dx, y + dy))

    return result


def next_generation(alive_cells):
    neighbour_counts = Counter()

    for cell in alive_cells:
        for neighbour in moore(cell):
            neighbour_counts[neighbour] += 1

    new_alive_cells = set()

    for cell, count in neighbour_counts.items():
        if cell in alive_cells:
            if count == 2 or count == 3:
                new_alive_cells.add(cell)
        else:
            if count == 3:
                new_alive_cells.add(cell)

    return new_alive_cells


def center(arrangement):
    grid_width = SCREEN_WIDTH // CELL_SIZE
    grid_height = SCREEN_HEIGHT // CELL_SIZE

    pattern_width = max(x for x, y in arrangement)
    pattern_height = max(y for x, y in arrangement)

    dx = grid_width // 2 - pattern_width // 2
    dy = grid_height // 2 - pattern_height // 2

    return {(x + dx, y + dy) for x, y in arrangement}


def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))

    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))


def draw_cells(screen, alive_cells):
    for x, y in alive_cells:
        pygame.draw.rect(
            screen,
            "white",
            (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    paused = True
    generation = 0
    alive_cells = center(GLIDER)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                if event.key == pygame.K_n and paused:
                    alive_cells = next_generation(alive_cells)
                    generation += 1

                if event.key in ARRANGEMENTS:
                    alive_cells = center(ARRANGEMENTS[event.key])
                    generation = 0
                    paused = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                cell = (mx // CELL_SIZE, my // CELL_SIZE)

                if cell in alive_cells:
                    alive_cells.remove(cell)
                else:
                    alive_cells.add(cell)

        if not paused:
            alive_cells = next_generation(alive_cells)
            generation += 1

        screen.fill("black")
        draw_grid(screen)
        draw_cells(screen, alive_cells)

        pygame.display.set_caption(
            f"Game of Life | Generation {generation} | "
            f"Cells {len(alive_cells)} | {'Paused' if paused else 'Running'}"
        )

        pygame.display.flip()
        clock.tick(GENERATIONS_PER_SECOND)

    pygame.quit()


if __name__ == "__main__":
    main()
