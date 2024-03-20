import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego con Menú")

# Definir colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE=(0, 0, 255)

# Cargar música de fondo
pygame.mixer.music.load('stranger-things-124008.mp3')
pygame.mixer.music.set_volume(0.5)  # Ajustar volumen (0.0 - 1.0)

# Cargar sonido para cuando el jugador pierde
game_over_sound = pygame.mixer.Sound('stranger-things-124008.mp3')

# Definir variables del jugador
player_size = 50
player_x = (WIDTH - player_size) // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

# Definir variables de los enemigos
enemy_size = 50
enemy_speed = 3
enemies = []

# Definir marcador de puntos
score = 0
font = pygame.font.Font(None, 36)

# Función para crear un nuevo enemigo
def create_enemy():
    enemy_x = random.randint(0, WIDTH - enemy_size)
    enemy_y = 0
    enemies.append([enemy_x, enemy_y])

# Función para mover los enemigos
def move_enemies():
    for enemy in enemies:
        enemy[1] += enemy_speed

# Función para dibujar al jugador y a los enemigos en la pantalla
def draw_objects():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

    # Mostrar marcador de puntos en pantalla
    text = font.render("Puntos: " + str(score), True, RED)
    screen.blit(text, (10, 10))

# Función para mostrar el menú de inicio
def show_menu():
    screen.fill(BLACK)
    font_menu = pygame.font.Font(None, 50)
    text_start = font_menu.render("Presiona cualquier tecla para comenzar", True, WHITE)
    text_rect_start = text_start.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text_start, text_rect_start)
    text_controls = font_menu.render("P: Pausa / C: Continuar / Q: Salir", True, WHITE)
    text_rect_controls = text_controls.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(text_controls, text_rect_controls)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Función para mostrar el menú de pausa
def show_pause_menu():
    screen.fill(BLACK)
    font_pause = pygame.font.Font(None, 50)
    text_pause = font_pause.render("PAUSA", True, WHITE)
    text_rect_pause = text_pause.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text_pause, text_rect_pause)

    text_resume = font_pause.render("Presiona C para continuar", True, WHITE)
    text_rect_resume = text_resume.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(text_resume, text_rect_resume)

    text_quit = font_pause.render("Presiona Q para salir", True, WHITE)
    text_rect_quit = text_quit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(text_quit, text_rect_quit)

    pygame.display.update()

# Mostrar el menú de inicio
show_menu()

# Reproducir música de fondo
pygame.mixer.music.play(-1)  # -1 significa que se repetirá continuamente

# Bucle principal del juego
running = True
clock = pygame.time.Clock()
paused = False

while running:
    clock.tick(60)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                    show_pause_menu()
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_c:
                paused = False
                pygame.mixer.music.unpause()
            elif event.key == pygame.K_q:
                running = False

    if paused:
        continue  # No actualices ni manejes la lógica del juego si está pausado

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # Crear un nuevo enemigo aleatorio
    if random.random() < 0.02:
        create_enemy()

    # Mover y dibujar enemigos
    move_enemies()

    # Dibujar objetos en pantalla
    draw_objects()
    pygame.display.update()

    # Verificar colisiones entre el jugador y los enemigos
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            game_over_sound.play()
            running = False
            break
        elif enemy[1] > HEIGHT:
            enemies.remove(enemy)
            score += 1

# Mostrar pantalla de fin de juego
screen.fill(WHITE)
text = font.render("¡Game Over! Puntos: " + str(score), True, RED)
screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2))
pygame.display.update()

# Esperar unos segundos antes de salir del juego
pygame.time.wait(2000)

# Salir de Pygame
pygame.quit()
sys.exit()
