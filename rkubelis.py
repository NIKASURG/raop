import pygame as pg
from veikejas import Player
from rkubelis import GameObject
import sys

# Initialize Pygame
pg.init()

# Constants
info = pg.display.Info()
eplotis = info.current_w  # Ekrano plotis
eaukstis = info.current_h  # Ekrano aukštis
WIDTH = eplotis
HEIGHT = eaukstis
PLAYER_WIDTH, PLAYER_HEIGHT = eplotis / 10, eplotis / 8  # Veikėjo aukštis yra 1/10, o plotis 1/8 ekrano plotio
PLAYER_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 0)
GROUND_COLOR = (100, 100, 100)
JUMP_HEIGHT = -15
GRAVITY = 0.5
PLAYER_X_SPEED = 0.5
ANIMATION_SPEED = 5

# Create the screen
screen = pg.display.set_mode((eplotis, eaukstis))
pg.display.set_caption("D2AN")

# Load background image
background_image = pg.image.load("background.png").convert()
background_image = pg.transform.scale(background_image, (WIDTH, HEIGHT))

# Initialize mixer
pg.mixer.init()

# Load menu music
menu_music = pg.mixer.Sound("Menu.mp3")
menu_music.set_volume(0.3)

# Load game music
game_music = pg.mixer.Sound("Game.mp3")
game_music.set_volume(0.3)

# Start playing menu music
menu_music.play(loops=-1)

# Player attributes
player_x = 100
player_y = HEIGHT - HEIGHT
player_x_speed = PLAYER_X_SPEED
player_y_speed = 0
jumping = False

# Ground attributes
ground_y = HEIGHT - 50

# Game state
MENU = 0
GAME = 1
game_state = MENU

# Fonts
font = pg.font.Font(None, 36)

# Main menu text
menu_text = font.render("Press SPACE to Start", True, (255, 255, 255))

# Load player animation frames
player_frames = []
for i in range(1):
    frame = pg.image.load(f"player_frame{i}.png").convert_alpha()
    frame = pg.transform.scale(frame, (int(PLAYER_WIDTH), int(PLAYER_HEIGHT)))
    player_frames.append(frame)
frame_index = 0
frame_counter = 0

# Initial direction (right)
player_direction = "right"

# Create the player object
player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, player_frames)

# Game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    keys = pg.key.get_pressed()

    if game_state == MENU:
        if keys[pg.K_SPACE]:
            game_state = GAME
            menu_music.stop()
            game_music.play(loops=-1)

    elif game_state == GAME:
        frame_counter += 1

        player.move(keys, ground_y)

        # Fill the background with the background image
        screen.blit(background_image, (0, 0))

        # Draw the ground
        pg.draw.rect(screen, GROUND_COLOR, (0, ground_y, WIDTH, HEIGHT - ground_y))

        # Draw the player with animation
        player.draw(screen)

    if game_state == MENU:
        screen.fill(BG_COLOR)
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - menu_text.get_height() // 2))
    if player.x < -1:
        player.x = eplotis - PLAYER_WIDTH - 1
    if player.x > eplotis - PLAYER_WIDTH:
        player.x = 0

    pg.display.update()

# Stop game music when quitting
game_music.stop()

# Quit Pygame
pg.quit()
sys.exit()
