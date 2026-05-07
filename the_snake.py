from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
# Цвет яблока
APPLE_COLOR = (255, 0, 0)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
# Скорость движения змейки:
SPEED = 20

# Настройка нашего игрового окна:

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок игрового окна:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализирует базовый игровой объект."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод отрисовки."""
        pass


class Apple(GameObject):
    """Класс яблока, наследуется от GameObject."""

    def __init__(self):
        """Инициализирует яблоко со случайной позицией."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Задаёт яблоку случайные координаты в пределах игровой сетки."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко (красный квадрат с рамкой)."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки наследует GameObject: управляет движением, ростом и отрисовкой."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None
    
    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        if hasattr(self, 'positions'):
            for position in self.positions:
                rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
                
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        center_x = (center_x // GRID_SIZE) * GRID_SIZE
        center_y = (center_y // GRID_SIZE) * GRID_SIZE
        self.positions = [(center_x, center_y)]
        self.length = 1
        self.last = None

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]
    
    def move(self):
        """Передвигает змейку на одну клетку, проходя сквозь стены."""
        head = self.get_head_position()
        x, y = self.direction

        new_head = ((head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                    (head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface):
        """Отрисовывает змейку и затирает след."""
        # Рисуем все сегменты, кроме последнего
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш, чтобы изменить направление движения."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    pygame.init()
    
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

        if snake.get_head_position() in snake.positions[1:]:
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR,
                             (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            snake.reset()
            apple.randomize_position()

            while apple.position in snake.positions:
                apple.randomize_position()

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
