import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up the display
pygame.display.set_caption('Snake 3003')
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

# Colors and settings
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)  # color for the ASCII '0'
font_color = (255, 0, 0)  # color for the ASCII '3'
snake_size = 20
score = 0

# Fonts for ASCII characters
font = pygame.font.Font(None, 40)
game_over_font = pygame.font.Font(None, 100)

# Snake initial setup
snake_pos = [[100, 40], [80, 40], [60, 40]]
direction = 'RIGHT'

# Fruit setup
def spawn_fruit():
    while True:
        new_position = [random.randrange(0, window_size[0]//snake_size) * snake_size,
                        random.randrange(0, window_size[1]//snake_size) * snake_size]
        if new_position not in snake_pos:
            return new_position

fruit_pos = spawn_fruit()
fruit_image = pygame.image.load('fruit.png')  # Ensure this path is correctly set
fruit_image = pygame.transform.scale(fruit_image, (snake_size, snake_size))

# Change direction function
def change_direction(new_dir):
    global direction
    if new_dir == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if new_dir == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if new_dir == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if new_dir == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

# Function to display game over screen
def game_over():
    screen.fill(black)
    game_over_text = game_over_font.render('Game Over', True, white)
    score_text = font.render('Score: ' + str(score), True, white)
    restart_text = font.render('Press R to Restart', True, white)
    quit_text = font.render('Press Q to Quit', True, white)
    screen.blit(game_over_text, (window_size[0] // 2 - game_over_text.get_width() // 2, window_size[1] // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (window_size[0] // 2 - score_text.get_width() // 2, window_size[1] // 2 + 60))
    screen.blit(restart_text, (window_size[0] // 2 - restart_text.get_width() // 2, window_size[1] // 2 + 120))
    screen.blit(quit_text, (window_size[0] // 2 - quit_text.get_width() // 2, window_size[1] // 2 + 180))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False
            if event.type == pygame.QUIT:
                return False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_direction('UP')
            if event.key == pygame.K_DOWN:
                change_direction('DOWN')
            if event.key == pygame.K_LEFT:
                change_direction('LEFT')
            if event.key == pygame.K_RIGHT:
                change_direction('RIGHT')

    # Move the snake
    new_head = [snake_pos[0][0] + (snake_size if direction == 'RIGHT' else -snake_size if direction == 'LEFT' else 0),
                snake_pos[0][1] + (snake_size if direction == 'DOWN' else -snake_size if direction == 'UP' else 0)]
    snake_pos.insert(0, new_head)

    # Check fruit collision
    if snake_pos[0] == fruit_pos:
        score += 1
        fruit_pos = spawn_fruit()  # Re-position the fruit
        snake_pos.append(snake_pos[-1])  # Grow the snake by adding another segment at the tail
    else:
        snake_pos.pop()

    # Check self-collision
    if snake_pos[0] in snake_pos[1:]:
        if game_over():
            snake_pos = [[100, 40], [80, 40], [60, 40]]  # Reset snake position
            direction = 'RIGHT'  # Reset direction
            score = 0  # Reset score
            fruit_pos = spawn_fruit()  # Respawn fruit
        else:
            pygame.quit()
            sys.exit()

    # Game over conditions
    if snake_pos[0][0] >= window_size[0] or snake_pos[0][0] < 0 or snake_pos[0][1] >= window_size[1] or snake_pos[0][1] < 0:
        if game_over():
            snake_pos = [[100, 40], [80, 40], [60, 40]]  # Reset snake position
            direction = 'RIGHT'  # Reset direction
            score = 0  # Reset score
            fruit_pos = spawn_fruit()  # Respawn fruit
        else:
            pygame.quit()
            sys.exit()

    # Graphics update
    screen.fill(black)
    for pos in snake_pos[1:-1]:
        body_text = font.render('0', True, green)
        screen.blit(body_text, (pos[0], pos[1]))
    head_tail_text = font.render('3', True, font_color)
    screen.blit(head_tail_text, (snake_pos[0][0], snake_pos[0][1]))  # Snake head as '3'
    if len(snake_pos) > 1:
        screen.blit(head_tail_text, (snake_pos[-1][0], snake_pos[-1][1]))  # Snake tail as '3'
    screen.blit(fruit_image, pygame.Rect(fruit_pos[0], fruit_pos[1], snake_size, snake_size))
    score_text = font.render('Score: ' + str(score), True, white)
    screen.blit(score_text, [0, 0])

    pygame.display.update()
    clock.tick(10)
