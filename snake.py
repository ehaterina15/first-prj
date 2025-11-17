"""
Игра «Изгиб Питона».
Реализация классической игры «Змейка» на Pygame.
"""

import random
import pygame


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20

GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BOARD_BACKGROUND_COLOR = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """
    Базовый игровой объект.

    Содержит позицию и цвет. Дочерние классы должны реализовать draw().
    """

    def __init__(self, position=None, body_color=(255, 255, 255)):
        """
        Инициализирует объект.

        :param position: tuple[int, int], координаты объекта
        :param body_color: tuple[int, int, int], RGB-цвет
        """
        if position is None:
            position = (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2
            )

        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Абстрактный метод отрисовки.

        Должен быть переопределён в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко на поле."""

    def __init__(self):
        """Создаёт яблоко и помещает его в случайное место."""
        super().__init__(body_color=(255, 0, 0))
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает новую случайную позицию яблока."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовывает яблоко."""
        size = (GRID_SIZE, GRID_SIZE)
        rect = pygame.Rect(self.position, size)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс, управляющий логикой змейки."""

    def __init__(self):
        """Создаёт змейку в центре экрана."""
        super().__init__(body_color=(0, 255, 0))
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление, запрещая разворот на 180°."""
        if self.next_direction is not None:
            new_dx, new_dy = self.next_direction
            curr_dx, curr_dy = self.direction
            opposite = (-curr_dx, -curr_dy)

            if (new_dx, new_dy) != opposite:
                self.direction = (new_dx, new_dy)

        self.next_direction = None

    def reset(self):
        """Сбрасывает состояние змейки после столкновения."""
        self.length = 1
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        self.positions = [self.position]
        self.direction = random.choice(
            [UP, DOWN, LEFT, RIGHT]
        )
        self.next_direction = None
        self.last = None

    def move(self):
        """
        Двигает змейку на одну клетку.

        1. Создаёт новую голову.
        2. Проверяет столкновение с собой.
        3. Добавляет голову в список.
        4. Удаляет хвост, если змейка не выросла.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        if new_head in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface):
        """
        Отрисовывает змейку.

        Стирает хвост, затем рисует все сегменты.
        """
        if self.last is not None:
            erase_rect = pygame.Rect(
                self.last,
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                surface,
                BOARD_BACKGROUND_COLOR,
                erase_rect
            )

        for pos in self.positions:
            rect = pygame.Rect(
                pos,
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш пользователя.

    Изменяет направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    """Главная функция, запускающая игру."""
    pygame.init()
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    pygame.display.set_caption("Изгиб Питона")

    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(20)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
