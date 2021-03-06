import pygame
import math
import random
import pygame_menu

from pygame.time import Clock

"""
Add a "high score" feature where:

# 1. Let's break down the criterias:
- when the game is running, display a seperate score to track the current high score

  - we need a seperate variable to track the high score (line 138)
  - let's call it raw_high_score
  - we can reuse the logic for drawing the current score (line 201)
    - convert high score from int to string
    - convert from string to image
    - blit image

- we update the high score if the user's current score is higher than the high score

  - we need to compare high score with current score
  - if raw_high_score > raw_score: (line 197)
        raw_high_score = raw_score

- when the user dies, we display the game over menu with the high score
    - we need to add some label to the menu class (line 170)

    https://pygame-menu.readthedocs.io/en/4.2.7/_source/widgets_label.html
    - use menu.add.label()
    - label.set_title(title)
"""

def restart():
    # not really recommended
    # we will discuss how to make this better next class

    # global tells the python compiler that the variable is actually belonging to somewhere else
    # modifying these variables here will modify the variables outside of the function
    global menu
    global trees
    global user_died
    global raw_score

    """
    It is usually better practice to pass the variable in as an argument 
    and modify it that way.

    However, for primitive values such as boolean and integers, we cannot update the
    passed in value and still have the global variable become updated.

    See https://realpython.com/python-pass-by-reference/
    """

    menu.set_onclose(pygame_menu.events.CLOSE)
    menu.close()
    trees = [[450, 350], [750, 350], [1100, 350], [2000, 350]]
    user_died = False
    raw_score = 0

def get_score_string_from_raw_score(raw_score):
    return "Score: "+str(math.floor(raw_score/10))

def get_high_score_string_from_raw_score(raw_score):
    return "High Score: "+str(math.floor(raw_score/10))

def add_new_tree(trees):
    if trees[0][0] > 0:
        return

    # pop the front tree that has reached the end
    trees.pop(0)
    last_tree_x = trees[-1][0]
    last_tree_y = trees[-1][1]

    new_tree_x = last_tree_x + random.randint(250, 500)
    trees.append([new_tree_x, last_tree_y])
    return trees

# --- Constants - constant variables do not change and are usually capitalized ----

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# tree values
MAX_NUM_TREES = 5
TREE_STARTING_X = 450
TREE_STARTING_Y = 350
SECONDS_PER_TREE = 5

# player values
PLAYER_STARTING_X = 10
PLAYER_STARTING_Y = 350
MAX_JUMP_HEIGHT = 120
JUMP_SPEED = 10

# screen values
MAX_FPS = 40
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

# Load your image in
bg_image = pygame.image.load("assets/backgroundCastles.png")
bg_image = pygame.transform.scale(bg_image, [700, 500])
player_image = pygame.image.load("assets/character_robot_walk0.png")
player_image = pygame.transform.scale(player_image, [40, 50])

tree_image = pygame.image.load("assets/tree.png")
tree_image = pygame.transform.scale(tree_image, [25, 50])

# ----------Update code here below here (Uncomment everything below this line using 'cmd+/' or 'ctrl+/')-----------
pygame.init()
 
# Set the width and height of the screen [width, height]
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Run Game")

# Loop until the user clicks the close button.
done = False

# Current player position
cur_player_x = PLAYER_STARTING_X
cur_player_y = PLAYER_STARTING_Y


# Jump vars
cur_jump_count = 0
has_jumped = False

# Trees

trees = [[450, 350], [750, 350], [1100, 350], [2000, 350]]

# Time
clock = Clock()
user_died = False 

# Score
raw_score = 0
raw_high_score = 0


# Initialize a font
score_font = pygame.font.SysFont("calibri", 30)

# Initialize menu
menu = pygame_menu.Menu('Game Over', 400, 300, theme=pygame_menu.themes.THEME_DARK)
high_score_label = menu.add.label("", max_char=-1, font_size=20)
menu.add.button('Restart', restart)

# game loops until done == False
while not done:
    # syncs game with FPS
    clock.tick(MAX_FPS)
    # watch for spacebar press event or close game event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not has_jumped:
              has_jumped = True
    if user_died:
        # if user died, we don't move to code that updates
        menu.enable()
        high_score_str = get_high_score_string_from_raw_score(raw_high_score)
        high_score_label.set_title(high_score_str)
        menu.mainloop(screen)

        continue
    # user has not died yet, we keep going!

    if has_jumped:
        if cur_jump_count < MAX_JUMP_HEIGHT:
            # player going up towards teh jump apex
            cur_player_y -= JUMP_SPEED
            cur_jump_count += JUMP_SPEED
        elif cur_jump_count >= (MAX_JUMP_HEIGHT * 2) - 10:
            # player has finished jumping and we need to reset to original player position
            cur_player_y = PLAYER_STARTING_Y
            # cur_player_x = PLAYER_STARTING_X
            cur_jump_count = 0
            has_jumped = False
        elif cur_jump_count >= MAX_JUMP_HEIGHT:
            # player coming down from the jump apex
            cur_player_y += (JUMP_SPEED * .8)
            cur_jump_count += (JUMP_SPEED * .8) 



    screen.blit(bg_image, (0, 0))
    user_surface = screen.blit(player_image, (cur_player_x, cur_player_y))

    for cur_tree_coordinates in trees:
        cur_tree_coordinates[0] -= 8
        tree_surface = screen.blit(tree_image, cur_tree_coordinates)
        user_surface = user_surface.inflate(-10, -5)
        if pygame.Rect.colliderect(user_surface, tree_surface):
            user_died = True
    
    add_new_tree(trees)
  
    raw_score += 1
    raw_high_score = max(raw_score, raw_high_score)

    score_str = get_score_string_from_raw_score(raw_score)
    score_img = score_font.render(score_str, True, BLACK)
    screen.blit(score_img, (20, 40))

    high_score_str = get_high_score_string_from_raw_score(raw_high_score)
    high_score_img = score_font.render(high_score_str, True, RED)
    screen.blit(high_score_img, (20, 10))
 
    pygame.draw.rect(screen, GREEN, (0, 400, 700, 500))
    pygame.display.update()
