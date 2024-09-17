import random

import pygame as p

FPS = 60
GRIDSIZE = 10
SCREEN_SIZE = 600
CELL_SIZE = SCREEN_SIZE / GRIDSIZE


class Ball:
    def __init__(self, x: float, y: float, color: str, player: str) -> None:
        self.position = [x, y]
        self.color = color
        self.player = player
        self.size = CELL_SIZE / 10
        self.vector = [5, 4]
        self.last_xy = self.xy()

    def move(self, reverse=False) -> None:
        if reverse:
            self.position[0] -= self.vector[0]
            self.position[1] -= self.vector[1]
        else:
            self.position[0] += self.vector[0]
            self.position[1] += self.vector[1]

    def xy(self) -> list[int]:
        return [
            max(0, min((GRIDSIZE - 1, int((self.position[0]) / CELL_SIZE)))),
            max(0, min(GRIDSIZE - 1, int((self.position[1]) / CELL_SIZE))),
        ]

    def update_vector(self, grid) -> tuple | None:
        x, y = self.xy()

        if (
            self.position[0] - self.size <= 0
            or self.position[0] + self.size >= SCREEN_SIZE
        ):
            self.move(True)
            self.vector[0] *= -1
            return
        if (
            self.position[1] - self.size <= 0
            or self.position[1] + self.size >= SCREEN_SIZE
        ):
            self.move(True)
            self.vector[1] *= -1
            return

        cell_color = grid[y][x]
        if self.color == cell_color:
            self.last_xy = x, y
            return

        if x != self.last_xy[0]:
            self.move(True)
            self.vector[0] *= -1
        if y != self.last_xy[1]:
            self.vector[1] *= -1
            self.move(True)
        self.last_xy = x, y
        return x, y


def init_grid() -> list[list]:
    cells = [random.choice(["white", "black"]) for _ in range(GRIDSIZE * GRIDSIZE)]
    grid = [cells[i * GRIDSIZE : (i + 1) * GRIDSIZE] for i in range(GRIDSIZE)]
    return grid


def draw_grid(screen: p.Surface, grid: list[list[int]]) -> None:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            p.draw.rect(
                screen,
                grid[y][x],
                p.Rect(
                    int(x * CELL_SIZE),
                    int(y * CELL_SIZE),
                    CELL_SIZE,
                    CELL_SIZE,
                ),
            )


def main() -> None:
    balls = [
        Ball(CELL_SIZE / 2, CELL_SIZE / 2, "white", "black"),
        Ball(
            SCREEN_SIZE - CELL_SIZE / 2, SCREEN_SIZE - CELL_SIZE / 2, "black", "white"
        ),
    ]

    grid = init_grid()

    p.init()
    screen = p.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    clock = p.time.Clock()

    running = True
    while running:
        draw_grid(screen, grid)
        for ball in balls:
            ball.move()
            ball_xy = ball.update_vector(grid)
            if ball_xy:
                grid[ball_xy[1]][ball_xy[0]] = ball.color
            p.draw.circle(screen, ball.player, ball.position, ball.size)

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        p.display.flip()
        clock.tick(FPS)
    p.quit()


if __name__ == "__main__":
    main()
