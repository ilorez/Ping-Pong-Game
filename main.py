import pygame
import random
from pygame import mixer  # for sounds
import json

#================== settings ==================#
with open('settings.json') as data:
  settings = json.load(data)

LIGHT = settings["LIGHT"]                                                                   # mode if light = false it's will be dark
WINDOW_SIZE = settings["WINDOW_SIZE"]                                                       # windows size
show_game_info = settings["show_game_info"]                                                 # show controller when open programme
game_info_posisiton = ((WINDOW_SIZE[0]-800)/2,(WINDOW_SIZE[1]-720)/2)                       # get center
FPS = settings["FPS"]                                                                       # FPS OF GAME 
DEGRE_COLOR = settings["DEGRE_COLOR"]                                                       # degre that random color work on
BG_COLOR = settings["BG_COLOR"]                                                             # background
COLOR = settings["COLOR"]                                                                   # text color
ROUNDS = settings["ROUNDS"]                                                                 # game rounds
MAX_SPEED = WINDOW_SIZE[1] / FPS
MAX_ANG = settings["MAX_ANG"]

bar = {"w": WINDOW_SIZE[0] * (0.09), "h": 100000000, 'wallSp':  5, 'speed': 720 / FPS, 'color': (210, 210, 210), 'multiAng': WINDOW_SIZE[0]/100}                          # bar object or dict have default value of bars
main_features = {'color': (50, 50, 50), 'position': (50, 50)}                                                                                                             # game place featuresl
ball_feat = {'w': 8, 'h': 8, "defaultSpeed": settings["DEFAULT_SPEED"],"defaultAng": ((WINDOW_SIZE[1] / FPS) / 4), 'addAng': 3/FPS, 'addSpeed':(FPS+10)/FPS, 'move': False,'dir_s': 0, 'ang': 0}  # ball features 

#set some paramatert
if LIGHT: 
    main_features['color'] = (220,220,220)
    BG_COLOR = (255,255,255)
    COLOR = (0,0,0)
    DEGRE_COLOR = (0,125)
def setMaxMove(ang,dir_s):
    global ball_feat
    if ang > MAX_ANG:
        ball_feat['ang'] = MAX_ANG
    if dir_s > MAX_SPEED:
        ball_feat['dir_s'] = MAX_SPEED
# ==================================== #





# initialize all imported pygame modules
pygame.init()
# set window display size
window = pygame.display.set_mode(WINDOW_SIZE)
window.fill(BG_COLOR)


# background music
pygame.mixer.music.load("./sounds/bg.mp3")
# Set the volume of the background music
pygame.mixer.music.set_volume(0.1)
# Start playing the background music
pygame.mixer.music.play(-1)  # -1: playing bg music on a loop
# create canvas main for make play on it
main_SIZE = (WINDOW_SIZE[0] - 100, WINDOW_SIZE[1] - 100)
main = pygame.Surface(main_SIZE)
main.fill(main_features['color'])




# players bars

# end or right
# bar_max_R = main_SIZE[0]-bar['w']-5

# create bar obj with default features
bar_1 = pygame.Rect(main_SIZE[0] // 2 - bar['w'] // 2, bar['wallSp'] -  bar['h'] , bar['w'], bar['h'])
bar_2 = pygame.Rect(main_SIZE[0] // 2 - bar['w'] // 2, main_SIZE[1] - bar['wallSp'], bar['w'], bar['h'])
bar1_score = bar2_score = 0

# this will make sense of ball angle when move right and left
bar1_ML = bar1_MR = bar2_ML = bar2_MR = 0

# ball
ball_x = main_SIZE[0] // 2 - ball_feat['w'] // 2
ball_y = main_SIZE[1] // 2 - ball_feat['h'] // 2
ball = pygame.Rect(ball_x, ball_y, ball_feat['h'], ball_feat['h'])

# score
font = pygame.font.Font('./fonts/Soulmate.otf', 32)
# return random color from gray to white
def random_color() -> tuple:
    return random.randint(DEGRE_COLOR[0], DEGRE_COLOR[1]), random.randint(DEGRE_COLOR[0], DEGRE_COLOR[1]), random.randint(DEGRE_COLOR[0], DEGRE_COLOR[1])


def setScore():
    # set player name
    Player1 = font.render("Player I", True, COLOR)
    Player2 = font.render("Player II", True, COLOR)
    window.blit(Player1, (WINDOW_SIZE[0] - Player1.get_width() - main_features['position'][0], 10))
    window.blit(Player2, (main_features['position'][0], WINDOW_SIZE[1] - Player2.get_height() - 10))

    # set score
    scoreB1 = font.render("Score : " + str(bar1_score), True, COLOR)
    scoreB2 = font.render("Score : " + str(bar2_score), True, COLOR)
    window.blit(scoreB1, (main_features['position'][0], 10))
    window.blit(scoreB2, (
        WINDOW_SIZE[0] - scoreB2.get_width() - main_features['position'][0],
        WINDOW_SIZE[1] - scoreB2.get_height() - 10))
    if not ball_feat['move']:
        start_ball = font.render("Click \"Space\" to start", True,
                                 random.choice([random_color(), random_color(), random_color()]))
        window.blit(start_ball, (ball_x + 50 - start_ball.get_width() // 2, ball_y + 110))

# arrow direction view
# arrow 1
arrow_Img1 = pygame.image.load('./images/arrow.png')
arrow_img1 = pygame.transform.scale(arrow_Img1,(24, 45))
arrow_rect1 = arrow_img1.get_rect()
arrow_rect1.bottom = WINDOW_SIZE[1]
arrow_rect1.left = WINDOW_SIZE[0]//2 - arrow_img1.get_width()//2
# arrow 2
arrow_Img2 = pygame.image.load('./images/arrow-bottom.png')
arrow_img2 = pygame.transform.scale(arrow_Img2,(24, 45))
arrow_rect2 = arrow_img2.get_rect()
arrow_rect2.top = 0
arrow_rect2.left = WINDOW_SIZE[0]//2 - arrow_img2.get_width()//2
def set_arr(ang1, ang2):
    rotated_image1 = pygame.transform.rotate(arrow_img1, ang1)
    window.blit(rotated_image1, rotated_image1.get_rect(center=arrow_rect1.center))
    rotated_image2 = pygame.transform.rotate(arrow_img2, ang2)
    window.blit(rotated_image2, rotated_image2.get_rect(center=arrow_rect2.center))

# @EVENTS
# on ball git goal
def on_goal() -> None:
    global bar_1, bar_2, next_coll
    next_coll = 0

    mixer.Sound('./sounds/goal.wav').play()
    # bar['w'] *= 2
    bar_1 = pygame.Rect(main_SIZE[0] // 2 - bar['w'] // 2, bar['wallSp'] - bar['h'], bar['w'], bar['h'])
    bar_2 = pygame.Rect(main_SIZE[0] // 2 - bar['w'] // 2, main_SIZE[1] - bar['wallSp'], bar['w'], bar['h'])
    ball_feat['ang'] = ball_feat['dir_s'] = 0
    ball.x = ball_x
    ball.y = ball_y
    ball_feat['move'] = False


def on_collision():
    mixer.Sound('./sounds/bar_hit.wav').play()
    ball_feat['dir_s'] *= ball_feat['addSpeed']
    ball_feat['dir_s'] = -ball_feat['dir_s']

# start menu controlles:
next_coll = 0
WINNER = ""
isWin = False
controles = pygame.image.load('./images/Controles_menu.png')

# restart game
def restart():
    global isWin, show_game_info, bar1_score, bar2_score
    isWin = False
    # show_game_info = True
    on_goal()
    bar1_score = bar2_score = 0

res_te = font.render("RESTART", True,random.choice([(0, 0, 255), (255, 0, 0), (0, 255, 0)]),(255,0,0))


# create a clock object to control the frame rate
clock = pygame.time.Clock()
# window loop
run: bool = True
while run:
    if isWin:
        window.fill((20, 20, 20))

        str_winner = font.render(f"The Winner is {WINNER}", True, (255, 255, 255))
        window.blit(str_winner, (WINDOW_SIZE[0]//2 - str_winner.get_width()//2,WINDOW_SIZE[1]//2 - str_winner.get_height()//2))
        res_te = font.render("RESTART", True, random.choice([(0, 0, 255), (255, 0, 0), (0, 255, 0)]))
        window.blit(res_te,(WINDOW_SIZE[0]//2 - res_te.get_width()//2,WINDOW_SIZE[1]//2 + res_te.get_height()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    restart()

        pygame.display.flip()
        continue

    if show_game_info:
        window.fill((80, 80, 80))
        window.blit(controles, game_info_posisiton)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # set show_game_info = false when click on space
            # that will start game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_game_info = False
        continue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # move the object to the right or left
    keys = pygame.key.get_pressed()
    # for start movement of ball
    if not ball_feat['move']:
        if keys[pygame.K_SPACE]:
            ball_feat['dir_s'] = random.choice([ball_feat["defaultSpeed"], -ball_feat["defaultSpeed"]])
            ball_feat['ang'] = random.choice([ball_feat["defaultAng"], -ball_feat["defaultAng"]])
            ball_feat['move'] = True
    # for bars
    if keys[pygame.K_LEFT]:
        bar_1.move_ip(-bar['speed'], 0)
        bar1_MR = 0
        bar1_ML -= ball_feat['addAng']

    if keys[pygame.K_RIGHT]:
        bar_1.move_ip(bar['speed'], 0)
        bar1_ML = 0
        bar1_MR += ball_feat['addAng']
    if keys[pygame.K_a]:
        bar_2.move_ip(-bar['speed'], 0)
        bar2_MR = 0
        bar2_ML -= ball_feat['addAng']
    if keys[pygame.K_d]:
        bar_2.move_ip(bar['speed'], 0)
        bar2_ML = 0
        bar2_MR += ball_feat['addAng']

    # Check if the object has hit the edge of the canvas
    if bar_1.left < 0:
        bar_1.left = 0
        bar1_ML = 0
    if bar_1.right > main_SIZE[0]:
        bar_1.right = main_SIZE[0]
        bar1_MR = 0
    if bar_2.left < 0:
        bar_2.left = 0
        bar2_ML = 0
    if bar_2.right > main_SIZE[0]:
        bar_2.right = main_SIZE[0]
        bar2_MR = 0

    # movement logic of ball
    setMaxMove(ball_feat['ang'],ball_feat['dir_s'])
    ball.move_ip(ball_feat['ang'], ball_feat['dir_s'])
    # if ball.left <= 0:
    #     ball_feat['ang'] = -ball_feat['ang']

    if ball.left <= 0 or ball.right >= main_SIZE[0]:
        mixer.Sound('./sounds/wall_hit.wav').play()
        ball_feat['ang'] = -ball_feat['ang']
    

    if bar_1.colliderect(ball) and next_coll in (1,0):
        next_coll = 2
        on_collision()
        ball_feat['ang'] += bar1_ML + bar1_MR
        '''Get the point of collision'''
        # collision_point = bar_1.clip(ball).topleft
        # print("Collision at point:", collision_point)
    

    if bar_2.colliderect(ball) and next_coll in (2,0):
        on_collision()
        next_coll = 1
        ball_feat['ang'] += bar2_ML + bar2_MR
        
    

    if ball.top <= 0 and not bar_1.colliderect(ball):
        on_goal()
        bar2_score += 1
        if bar2_score == ROUNDS:
            isWin = True
            WINNER = 'Player II'
    if ball.bottom >= main_SIZE[1] and not bar_2.colliderect(ball):
        on_goal()
        bar1_score += 1
        if bar1_score == ROUNDS:
            isWin = True
            WINNER = 'Player I'

    


    window.fill(BG_COLOR)

    # refill main for remove last position of rect draw
    main.fill(main_features['color'])

    # Draw the object at its new position
    pygame.draw.rect(main, random_color(), bar_1)
    pygame.draw.rect(main, random_color(), bar_2)
    pygame.draw.rect(main, random_color(), ball)

    # set main in screen
    window.blit(main, main_features['position'])
    # set score
    setScore()
    set_arr(-(bar2_ML + bar2_MR) * bar['multiAng'], (bar1_ML + bar1_MR) * bar['multiAng'])
    # update window
    pygame.display.flip()
    clock.tick(FPS)
