import json
import os
import random

import pygame

# Initialize pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 400
pygame.display.set_caption("Infinite Runner Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Different color themes for the game [background_color, platform_color]
COLOR_THEMES = [
    ((20, 40, 80), (200, 180, 120)),  # Blue background with tan platforms
    ((50, 20, 70), (230, 140, 90)),  # Purple background with orange platforms
    ((10, 60, 50), (210, 190, 150)),  # Green background with beige platforms
    ((60, 10, 10), (220, 160, 100)),  # Red background with gold platforms
]


# Load the best score from file if it exists
def load_score():
    if os.path.exists("scores.json"):
        with open("scores.json", "r") as file:
            return json.load(file).get("best_score", 0)
    return 0


# Save the best score to file
def save_score(best_score):
    with open("scores.json", "w") as file:
        json.dump({"best_score": best_score}, file)


# Load the previous best score
best_score = load_score()

# Load player standing animation frames
player_standing_frames = [
    pygame.transform.smoothscale(
        pygame.image.load(f"assets/player_stay_ground_{i + 1}.png").convert_alpha(),
        (40, 35),
    )
    for i in range(2)
]

# Load player running animation frames
player_running_frames = [
    pygame.transform.smoothscale(
        pygame.image.load(f"assets/player_run_ground_{i + 1}.png").convert_alpha(),
        (40, 35),
    )
    for i in range(2)
]

# Load player jumping image
player_jumping_frame = pygame.transform.smoothscale(
    pygame.image.load("assets/player_jump_down_1.png").convert_alpha(), (40, 35)
)

# Set up player initial state
player_image = player_standing_frames[0]
player_rect = player_image.get_rect()
player_rect.topleft = (200, 265)

# Player physics variables
player_vertical_velocity = 0
gravity_strength = 1
is_player_jumping = False
can_player_jump = True  # Prevents jumping in mid-air

# Animation control variables
current_animation_frame = 0
animation_timer = 0
animation_speed = 8  # Frames per second for animations

# Game layers for platforms (background, midground, foreground)
foreground_platforms = []
midground_platforms = []
background_platforms = []

# Initial game scroll speed
scroll_speed = 6


# Create a platform rectangle at specified position and width
def create_platform(x_position, y_position, width):
    return pygame.Rect(x_position, y_position, width, 20)


# Add a new platform to a layer with random positioning
def add_new_platform_to_layer(layer, min_height, max_height):
    last_platform = layer[-1]
    gap_between_platforms = random.randint(90, 160)
    platform_width = random.randint(100, 240)
    new_x_position = last_platform.x + last_platform.width + gap_between_platforms
    new_y_position = random.randint(min_height, max_height)
    layer.append(create_platform(new_x_position, new_y_position, platform_width))


# Create the initial platforms for all layers when game starts
def create_initial_platforms():
    foreground_platforms.clear()
    midground_platforms.clear()
    background_platforms.clear()

    # Create starting platforms for each layer
    foreground_platforms.append(create_platform(120, 330, 200))
    midground_platforms.append(create_platform(80, 270, 180))
    background_platforms.append(create_platform(0, 210, 160))


# Initialize the platforms
create_initial_platforms()

# Game state variables
game_has_started = False
game_is_over = False
current_score = 0
screen_shake_timer = 0


# Reset the game to its initial state
def reset_game():
    global player_rect, player_vertical_velocity, is_player_jumping, can_player_jump
    global game_has_started, game_is_over, current_score, screen_shake_timer

    # Recreate all platforms
    create_initial_platforms()

    # Reset player position to the first midground platform
    first_midground_platform = midground_platforms[0]
    player_rect.x = 200
    player_rect.bottom = first_midground_platform.top

    # Reset player state
    player_vertical_velocity = 0
    is_player_jumping = False
    can_player_jump = True
    game_has_started = False
    game_is_over = False
    current_score = 0
    screen_shake_timer = 0


# Initialize game state
reset_game()

# Set up theme switching
current_background_color, current_platform_color = random.choice(COLOR_THEMES)
theme_switch_timer = 0
THEME_SWITCH_TIME = 300  # How often to switch themes (in frames)

# Game loop control
game_is_running = True

# Set up fonts for UI
ui_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 72, bold=True)

# Main game loop
while game_is_running:
    # Control game speed to 60 frames per second
    clock.tick(60)

    # Handle theme switching
    theme_switch_timer += 1
    if theme_switch_timer >= THEME_SWITCH_TIME:
        current_background_color, current_platform_color = random.choice(COLOR_THEMES)
        theme_switch_timer = 0

    # Handle screen shake effect (for game over)
    shake_offset_x = random.randint(-5, 5) if screen_shake_timer > 0 else 0
    shake_offset_y = random.randint(-4, 4) if screen_shake_timer > 0 else 0
    if screen_shake_timer > 0:
        screen_shake_timer -= 1

    # Fill the screen with current background color
    screen.fill(current_background_color)

    # Process game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False

        if event.type == pygame.KEYDOWN:
            # Quit game with Ctrl+Q
            if event.key == pygame.K_q and (event.mod & pygame.KMOD_CTRL):
                game_is_running = False

            # Handle space bar input
            if event.key == pygame.K_SPACE:
                if game_is_over:
                    # Restart game if game over
                    reset_game()
                    continue

                # Start the game if not already started
                game_has_started = True

                # Jump if player is on ground and allowed to jump
                if not is_player_jumping and can_player_jump and not game_is_over:
                    is_player_jumping = True
                    can_player_jump = False  # Prevent jumping again until landing
                    player_vertical_velocity = (
                        -17
                    )  # Negative velocity makes player jump up

    # Gameplay logic (only when game is active)
    if game_has_started and not game_is_over:
        # Display current score and speed
        screen.blit(
            ui_font.render(f"Score: {int(current_score)}", True, (255, 255, 255)),
            (10, 10),
        )
        screen.blit(
            ui_font.render(f"Speed: {int(round(scroll_speed))}", True, (255, 255, 255)),
            (10, 38),
        )

        # Move all platforms to create scrolling effect
        for platform in background_platforms:
            platform.x -= scroll_speed
        for platform in midground_platforms:
            platform.x -= scroll_speed
        for platform in foreground_platforms:
            platform.x -= scroll_speed

        # Add new platforms when existing ones scroll off screen
        if background_platforms[-1].right < WIDTH:
            add_new_platform_to_layer(background_platforms, 180, 230)
        if midground_platforms[-1].right < WIDTH:
            add_new_platform_to_layer(midground_platforms, 240, 290)
        if foreground_platforms[-1].right < WIDTH:
            add_new_platform_to_layer(foreground_platforms, 300, 340)

        # Apply gravity to player
        player_vertical_velocity += gravity_strength
        player_rect.y += player_vertical_velocity

        # Check for platform collisions (landing)
        platforms_player_can_land_on = []

        for layer in (foreground_platforms, midground_platforms, background_platforms):
            for platform in layer:
                # Check if player is colliding with platform and moving downward
                if player_rect.colliderect(platform) and player_vertical_velocity > 0:
                    # Make sure player was above the platform before moving down
                    if player_rect.bottom - player_vertical_velocity <= platform.top:
                        platforms_player_can_land_on.append(platform)

        # Land on the highest platform if multiple collisions
        if platforms_player_can_land_on:
            highest_platform = min(
                platforms_player_can_land_on, key=lambda platform: platform.top
            )
            player_rect.bottom = highest_platform.top
            player_vertical_velocity = 0
            is_player_jumping = False
            can_player_jump = True  # Allow jumping again after landing

        # Increase score and speed over time
        current_score += 0.12
        scroll_speed = 6 + current_score / 60

        # Check if player fell off the bottom of the screen (game over)
        if player_rect.y > HEIGHT:
            game_is_over = True
            current_score = int(current_score)

            # Update best score if current score is higher
            if current_score > best_score:
                best_score = current_score
                save_score(best_score)

            # Trigger screen shake effect
            screen_shake_timer = 30

        # Prevent player from going above the top of the screen
        if player_rect.top <= 0:
            player_rect.top = 0
            player_vertical_velocity = 0

    # Draw all platforms with current platform color
    for platform in background_platforms:
        pygame.draw.rect(
            screen,
            current_platform_color,
            platform.move(shake_offset_x, shake_offset_y),
        )
    for platform in midground_platforms:
        pygame.draw.rect(
            screen,
            current_platform_color,
            platform.move(shake_offset_x, shake_offset_y),
        )
    for platform in foreground_platforms:
        pygame.draw.rect(
            screen,
            current_platform_color,
            platform.move(shake_offset_x, shake_offset_y),
        )

    # Update player animation based on state
    if is_player_jumping:
        player_image = player_jumping_frame
    else:
        # Cycle through running animation frames
        animation_timer += 1
        if animation_timer >= animation_speed:
            animation_timer = 0
            current_animation_frame = (current_animation_frame + 1) % len(
                player_running_frames
            )
        player_image = player_running_frames[current_animation_frame]

    # Draw the player character
    screen.blit(player_image, player_rect.move(shake_offset_x, shake_offset_y))

    # Show title screen before game starts
    if not game_has_started and not game_is_over:
        # Game title with border effect
        title_text_color = (173, 216, 230)  # Light sky blue
        title_border_color = (100, 149, 237)  # Darker blue for border

        # Render the main title text
        title_text = title_font.render("GRAVITY JUMP", True, title_text_color)
        title_position = title_text.get_rect(center=(WIDTH // 2, 120))

        # Create border effect by drawing the text multiple times with offsets
        for offset_x, offset_y in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            border_text = title_font.render("GRAVITY JUMP", True, title_border_color)
            screen.blit(border_text, title_position.move(offset_x, offset_y))

        # Draw the main title text on top of the border
        screen.blit(title_text, title_position)

        # Display game instructions
        screen.blit(
            ui_font.render("Press SPACE to jump", True, (255, 255, 255)), (300, 200)
        )

    # Show game over screen
    if game_is_over:
        screen.blit(
            ui_font.render(f"Game Over! Score: {current_score}", True, (255, 100, 100)),
            (270, 130),
        )
        screen.blit(
            ui_font.render(f"Best Score: {best_score}", True, (255, 255, 255)),
            (310, 160),
        )
        screen.blit(
            ui_font.render("Press SPACE to restart", True, (255, 255, 255)), (270, 190)
        )

    # Update the display
    pygame.display.flip()

# Clean up pygame when game ends
pygame.quit()
