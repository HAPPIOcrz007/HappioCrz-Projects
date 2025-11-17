import json
import os
import random

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 400
pygame.display.set_caption("Infinite Runner Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# COLOR SCHEMES
COLOR_THEMES = [
    ((20, 40, 80), (200, 180, 120)),
    ((50, 20, 70), (230, 140, 90)),
    ((10, 60, 50), (210, 190, 150)),
    ((60, 10, 10), (220, 160, 100)),
]


# SCORE LOADING
def load_score():
    if os.path.exists("scores.json"):
        with open("scores.json", "r") as f:
            return json.load(f).get("best_score", 0)
    return 0


def save_score(best):
    with open("scores.json", "w") as f:
        json.dump({"best_score": best}, f)


best_score = load_score()


# PLAYER SETUP Core
player_s = [
    pygame.transform.smoothscale(
        pygame.image.load(f"assets/player_stay_ground_{i + 1}.png").convert_alpha(),
        (40, 35),
    )
    for i in range(2)
]
# running animation load
run_imgs = [
    pygame.transform.smoothscale(
        pygame.image.load(f"assets/player_run_ground_{i + 1}.png").convert_alpha(),
        (40, 35),
    )
    for i in range(2)
]
# jumping animation load
jump_img = pygame.transform.smoothscale(
    pygame.image.load("assets/player_jump_down_1.png").convert_alpha(), (40, 35)
)
# initial setup
player_img = player_s[0]
player_rect = player_img.get_rect()
player_rect.topleft = (200, 265)
# velocities
player_vel_y = 0
gravity = 1
is_jumping = False
# animation
anim_index = 0
anim_timer = 0
anim_speed = 8

# LAYERS
foreground = []
midground = []
background = []
# game speed
scroll_speed = 6


def create_platform(x, y, w):
    return pygame.Rect(x, y, w, 20)


def push_new_platform(layer, min_y, max_y):
    last = layer[-1]
    gap = random.randint(90, 160)
    w = random.randint(100, 240)
    new_x = last.x + last.width + gap
    new_y = random.randint(min_y, max_y)
    layer.append(create_platform(new_x, new_y, w))


def create_initial_platforms():
    foreground.clear()
    midground.clear()
    background.clear()
    foreground.append(create_platform(120, 330, 200))
    midground.append(create_platform(80, 270, 180))
    background.append(create_platform(0, 210, 160))


create_initial_platforms()

# GAME initial STATE
game_started = False
game_over = False
score = 0
shake_timer = 0


def reset_game():
    global \
        player_rect, \
        player_vel_y, \
        is_jumping, \
        game_started, \
        game_over, \
        score, \
        shake_timer
    create_initial_platforms()

    mid_plat = midground[0]
    player_rect.x = 200
    player_rect.bottom = mid_plat.top

    player_vel_y = 0
    is_jumping = False
    game_started = False
    game_over = False
    score = 0
    shake_timer = 0


reset_game()

# LOOP
current_bg, current_plank = random.choice(COLOR_THEMES)
theme_timer = 0
THEME_SWITCH_INTERVAL = 300

running = True
font = pygame.font.SysFont("Arial", 24)

while running:
    clock.tick(60)
    # Theme changing
    theme_timer += 1
    if theme_timer >= THEME_SWITCH_INTERVAL:
        current_bg, current_plank = random.choice(COLOR_THEMES)
        theme_timer = 0
    # Screen shaking
    shake_x = random.randint(-5, 5) if shake_timer > 0 else 0
    shake_y = random.randint(-4, 4) if shake_timer > 0 else 0
    if shake_timer > 0:
        shake_timer -= 1
    screen.fill(current_bg)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and (event.mod & pygame.KMOD_CTRL):
                running = False

            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                    continue

                game_started = True

                if not is_jumping and not game_over:
                    is_jumping = True
                    player_vel_y = -17

    if game_started and not game_over:
        screen.blit(
            font.render(f"Score: {int(score)}", True, (255, 255, 255)), (10, 10)
        )
        screen.blit(
            font.render(f"Speed: {int(round(scroll_speed))}", True, (255, 255, 255)),
            (10, 38),
        )

        for p in background:
            p.x -= scroll_speed
        for p in midground:
            p.x -= scroll_speed
        for p in foreground:
            p.x -= scroll_speed

        if background[-1].right < WIDTH:
            push_new_platform(background, 180, 230)
        if midground[-1].right < WIDTH:
            push_new_platform(midground, 240, 290)
        if foreground[-1].right < WIDTH:
            push_new_platform(foreground, 300, 340)

        player_vel_y += gravity
        player_rect.y += player_vel_y

        landing_candidates = []

        for layer in (foreground, midground, background):
            for p in layer:
                if player_rect.colliderect(p) and player_vel_y > 0:
                    if player_rect.bottom - player_vel_y <= p.top:
                        landing_candidates.append(p)

        if landing_candidates:
            target = min(landing_candidates, key=lambda plat: plat.top)
            player_rect.bottom = target.top
            player_vel_y = 0
            is_jumping = False

        score += 0.12
        scroll_speed = 6 + score / 60

        if player_rect.y > HEIGHT:
            game_over = True
            score = int(score)

            if score > best_score:
                best_score = score
                save_score(best_score)

            shake_timer = 30

        if player_rect.top <= 0:
            player_rect.top = 0
            player_vel_y = 0

    for p in background:
        pygame.draw.rect(screen, current_plank, p.move(shake_x, shake_y))
    for p in midground:
        pygame.draw.rect(screen, current_plank, p.move(shake_x, shake_y))
    for p in foreground:
        pygame.draw.rect(screen, current_plank, p.move(shake_x, shake_y))

    if is_jumping:
        player_img = jump_img
    else:
        anim_timer += 1
        if anim_timer >= anim_speed:
            anim_timer = 0
            anim_index = (anim_index + 1) % len(run_imgs)
        player_img = run_imgs[anim_index]

    screen.blit(player_img, player_rect.move(shake_x, shake_y))

    if not game_started and not game_over:
        screen.blit(
            font.render("Press SPACE to start", True, (255, 255, 255)), (280, 100)
        )

    if game_over:
        screen.blit(
            font.render(f"Game Over! Score: {score}", True, (255, 100, 100)), (270, 130)
        )
        screen.blit(
            font.render(f"Best Score: {best_score}", True, (255, 255, 255)), (310, 160)
        )
        screen.blit(
            font.render("Press SPACE to restart", True, (255, 255, 255)), (270, 190)
        )

    pygame.display.flip()

pygame.quit()
