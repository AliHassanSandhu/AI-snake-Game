import pygame
import sys
import time
import random

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 120

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

def breadth_first_search(snake_pos, food_pos, snake_body):
    # Create a queue for BFS
    queue = [snake_pos]
    visited = set()
    parent = [[None for _ in range(frame_size_y // 10)] for _ in range(frame_size_x // 10)]
    
    while queue:
        s = queue.pop(0)
        if s == food_pos:
            path = []
            while s != snake_pos:
                path.append(s)
                s = parent[s[0] // 10][s[1] // 10]
            return path
        
        if tuple(s) in visited:
            continue
        
        visited.add(tuple(s))
        x, y = s
        
        neighbors = [(x - 10, y), (x + 10, y), (x, y - 10), (x, y + 10)]
        for nx, ny in neighbors:
            if 0 <= nx < frame_size_x and 0 <= ny < frame_size_y:
                if tuple((nx, ny)) not in visited and [nx, ny] not in queue and [nx, ny] not in snake_body:
                    queue.append([nx, ny])
                    parent[nx // 10][ny // 10] = s

    return None

def get_direction(snake_pos, food_pos, snake_body):
    path = breadth_first_search(snake_pos, food_pos, snake_body)
    if path:
        next_pos = path[-1]
        if snake_pos[0] - next_pos[0] == 10:
            return 'LEFT'
        if snake_pos[0] - next_pos[0] == -10:
            return 'RIGHT'
        if snake_pos[1] - next_pos[1] == 10:
            return 'UP'
        if snake_pos[1] - next_pos[1] == -10:
            return 'DOWN'
    return direction  # Keep the current direction if no path is found

# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)

# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Get direction from breadth-first search   
    change_to = get_direction(snake_pos, food_pos, snake_body)

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)
