"""Модуль игры 'Змейка' на Pygame."""

import random
import pygame

# Константы размеров:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20

GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BORDER_COLOR = (120, 120, 120)

# Настройки окна:
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()
SPEED = 20


def handle_keys(snake):
    """Обрабатывает события Pygame и меняет направление движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


class GameObject:
    """Базовый класс игрового объекта с позицией и цветом."""

    def __init__(self, position=None, body_color=(255, 255, 255)):
        """
        Инициализирует игровой объект.

        :param position: начальная позиция (x, y)
        :param body_color: цвет объекта (R, G, B)
        """
        default = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position if position is not None else default
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на поверхности (переопределяется в наследниках)."""
        pass


class Apple(GameObject):
    """Игровое яблоко, которое появляется в случайной клетке поля."""

    def __init__(self):
        """Создаёт яблоко и сразу задаёт ему случайную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Перемещает яблоко в случайную клетку сетки."""
        x_coord = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y_coord = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x_coord, y_coord)

    def draw(self, surface):
        """Рисует яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка: хранит сегменты тела и реализует логику движения."""

    def __init__(self):
        """Создаёт змейку длины 1 в центре экрана."""
        start_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(position=start_pos, body_color=SNAKE_COLOR)

        self.length = 1
        self.positions = [start_pos]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Применяет отложенное изменение направления движения."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Перемещает змейку на одну клетку.

        Добавляет новую голову, проверяет столкновение с собой
        и при необходимости удаляет хвост.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        # Проверка на столкновение с собственным телом (кроме головы и шеи).
        if new_head in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface):
        """Отрисовывает все сегменты змейки на поверхности."""
        if self.last is not None:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сбрасывает змейку в исходное состояние в центре поля."""
        start_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [start_pos]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def main():
    """Запускает игру: создаёт объекты и главный игровой цикл."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()