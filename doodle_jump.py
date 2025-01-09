import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 400, 600
FPS = 60
WHITE = (255, 255, 255)

# Настройки игрока
player_width, player_height = 50, 50
player_color = (0, 255, 0)
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 200
player_speed = 5
player_jump = -12  # Уменьшенная сила прыжка
gravity = 0.5

# Настройки платформ
platform_width, platform_height = 100, 20
platform_color = (255, 0, 0)
platforms = [[WIDTH // 2 - platform_width // 2, HEIGHT - 40]]  # Начальная платформа

# Смещение камеры по оси Y
camera_y_offset = 0

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump на Pygame")

# Игровой цикл
clock = pygame.time.Clock()
running = True
y_velocity = 0

while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Гравитация
    y_velocity += gravity
    player_y += y_velocity

    # Смещение камеры: если игрок поднимается выше середины экрана, смещаем камеру
    if player_y < HEIGHT // 2:
        camera_y_offset += (HEIGHT // 2 - player_y) * 0.01  # Плавное смещение камеры
        player_y = HEIGHT // 2

    # Ограничение падения игрока (для простоты)
    if player_y > HEIGHT:
        running = False

    # Платформы и прыжки
    for platform in platforms:
        # Проверка, если игрок падает на платформу
        if (player_x + player_width > platform[0] and player_x < platform[0] + platform_width) and \
           (player_y + player_height >= platform[1] and player_y + player_height <= platform[1] + platform_height) and \
           y_velocity > 0:
            y_velocity = player_jump  # Сброс вертикальной скорости при прыжке

    # Удаление платформ ниже экрана и создание новых выше
    platforms = [[x, y + camera_y_offset] for x, y in platforms if y + camera_y_offset < HEIGHT]
    while len(platforms) < 5:
        new_platform_x = random.randint(0, WIDTH - platform_width)
        new_platform_y = platforms[-1][1] - random.randint(100, 150)  # Разное расстояние между платформами
        platforms.append([new_platform_x, new_platform_y])

    # Рисование игрока с учетом смещения камеры
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))

    # Рисование платформ с учетом смещения камеры
    for platform in platforms:
        pygame.draw.rect(screen, platform_color, (platform[0], platform[1] + camera_y_offset, platform_width, platform_height))

    # Обновление экрана
    pygame.display.flip()

pygame.quit()

