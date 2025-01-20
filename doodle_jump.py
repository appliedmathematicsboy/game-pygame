import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (255, 0, 0)

# Создаем игрока
player_width, player_height = 50, 50
player_color = (0, 255, 0)
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 60
player_speed = 5
player_jump = -12  # Уменьшенная сила прыжка
gravity = 0.5

# Смещение камеры по оси Y
camera_y_offset = 0
camera_border_up = WIDTH // 2
camera_border_down = WIDTH // 2 + 100

#счет
score = 0

#создаем платформы
platform_width, platform_height = 100, 20
platform_color = (255, 0, 0)
platforms = [[WIDTH // 2 - platform_width // 2, HEIGHT - 40]]
oldplatforms = []

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("doodle jump")

# проверка столкновения
def check_collision(platforms, player_x, player_y, player_width, player_height, y_velocity):
    for platform in platforms:
        if (platform[1] - 5 <= player_y + player_height <= platform[1]) and \
           (platform[0] <= player_x + player_width) and \
           (platform[0] + platform_width >= player_x) and \
           y_velocity > 0:
            return True
    return False

# Цикл игры
running = True
y_velocity = 0
clock = pygame.time.Clock()

while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Гравитация
    y_velocity += gravity
    player_y += y_velocity

    # Текущая высота
    current_hight = player_y + camera_y_offset

    # Смещение камеры
    if current_hight < HEIGHT // 2 + 50:
        camera_y_offset += (HEIGHT // 2 + 50 - current_hight) * 0.2

    if current_hight > HEIGHT - 50:
        camera_y_offset -= (current_hight - HEIGHT + 50) * 0.7

    # Добавили к списку старых платформ, если ниже ушла
    if platforms[0][1] > HEIGHT - camera_y_offset:
        oldplatforms += [platforms.pop(0)]

    # Проверяем, сколько платформ осталось и добавляем новые, если их меньше 10
    if len(platforms) > 0 and platforms[-1][1] > 90 - camera_y_offset:
        new_platform_x = random.randint(0, WIDTH - platform_width)
        new_platform_y = platforms[-1][1] - random.randint(100, 140)  # Разное расстояние между платформами
        platforms.append([new_platform_x, new_platform_y])

    # Вставляем старые платформы обратно, если они ниже определенной высоты
    if len(oldplatforms) > 0:
        if oldplatforms[-1][1] < HEIGHT - camera_y_offset:
            platforms.insert(0, oldplatforms.pop(-1))



    # Столкновения с новыми и старыми платформами
    all_platforms = platforms + oldplatforms[-6:]  # Объединяем новые и последние 6 старых платформ
    if check_collision(all_platforms, player_x, player_y, player_width, player_height, y_velocity):
        y_velocity = player_jump
        score += 1

    # Выход из программы
    if camera_y_offset + player_y > HEIGHT + camera_y_offset:
        running = False

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        player_x -= 8
    if keystate[pygame.K_RIGHT]:
        player_x += 8
    if player_x > WIDTH:
        player_x = -player_width
    if player_x + player_width < 0:
        player_x = WIDTH

    # Рендеринг
    screen.fill(BLACK)

    # Рисуем игрока с учетом смещения камеры
    pygame.draw.rect(screen, player_color, (player_x, player_y + camera_y_offset, player_width, player_height))

    # Рисуем платформ с учетом смещения камеры
    for platform in platforms + oldplatforms[-6:]:
        pygame.draw.rect(screen, platform_color, (platform[0], platform[1] + camera_y_offset, platform_width, platform_height))

    f1 = pygame.font.Font(None, 46)
    text1 = f1.render(str(f'score : {score}'), True, (180, 0, 0))
    screen.blit(text1, (WIDTH - 150, 30))

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()