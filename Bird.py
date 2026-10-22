import pygame
import random

pygame.init()
W, H = 480, 640          # Ширина, высота
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Птичка")
clock = pygame.time.Clock()


SKY_COLOR = (135, 206, 250) # небо
PIPE_COLOR = (0, 150, 0)   # трубы
GRAVITY = 0.5      # сила притяжения
JUMP = -8          # сила прыжка
GAP = 160          # просвет между трубами
PIPE_SPEED = 4     # скорость труб
BIRD_SIZE = 40     # размер птички на экране

try:
    bird_img = pygame.image.load("bird.png").convert_alpha()
    bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE, BIRD_SIZE))
except:
    bird_img = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
    bird_img.fill((255, 200, 0))

def reset_game():
    global bird_x, bird_y, bird_vy, pipe_x, pipe_gap_y, score
    global game_over, started
    bird_x = 100
    bird_y = H // 2
    bird_vy = 0
    pipe_x = W
    pipe_gap_y = random.randint(80, H - 80 - GAP)
    score = 0
    game_over = False
    started = False

reset_game()

font = pygame.font.SysFont("Arial", 32)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not started:
                    started = True
                elif not game_over:
                    bird_vy = JUMP
            if event.key == pygame.K_RETURN and game_over:
                reset_game()

    if started and not game_over:
        bird_vy += GRAVITY
        bird_y += bird_vy

        pipe_x -= PIPE_SPEED

        if pipe_x < -70:
            pipe_x = W
            pipe_gap_y = random.randint(80, H - 80 - GAP)
            score += 1

        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_SIZE, BIRD_SIZE)
        top_pipe = pygame.Rect(pipe_x, 0, 70, pipe_gap_y)
        bot_pipe = pygame.Rect(pipe_x, pipe_gap_y + GAP, 70, H)
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bot_pipe):
            game_over = True
        if bird_y < 0 or bird_y > H:
            game_over = True

    screen.fill(SKY_COLOR)
    pygame.draw.rect(screen, PIPE_COLOR, (pipe_x, 0, 70, pipe_gap_y))
    pygame.draw.rect(screen, PIPE_COLOR, (pipe_x, pipe_gap_y + GAP, 70, H))
    screen.blit(bird_img, (bird_x, bird_y))

    text = font.render(str(score), True, (255, 255, 255))
    screen.blit(text, (W // 2 - 10, 30))

    if not started:
        hint1 = font.render("Нажми пробел", True, (255, 255, 255))
        screen.blit(hint1, (W // 2 - 130, H // 2 - 100))
        hint2 = font.render("чтобы начать", True, (255, 255, 255))
        screen.blit(hint2, (W // 2 - 110, H // 2 - 60))

    if game_over:
        over = font.render("Игра окончена", True, (255, 0, 0))
        screen.blit(over, (W // 2 - 110, H // 2 - 20))
        again = font.render("ENTER — сыграть ещё", True, (255, 255, 255))
        screen.blit(again, (W // 2 - 170, H // 2 + 30))

    pygame.display.update()
    clock.tick(60)

pygame.quit()