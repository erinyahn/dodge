import random
import pygame

pygame.init()

screen_width = 560
screen_height = 375
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("dodge")

# FPS
clock = pygame.time.Clock()

# set background
background = pygame.image.load("/Users/randyli/personal-proj/dodge/background.jpg")

# set player
class Player(pygame.sprite.Sprite):
        def __init__(self,):
            pygame.sprite.Sprite(self)

player = pygame.image.load("/Users/randyli/personal-proj/dodge/player.png")
player_size = player.get_rect().size  # getting the size of the image
player_width = player_size[0]  # width of player
player_height = player_size[1]  # height of player
player_x_pos = (screen_width / 2) - (player_width / 2)  # in middle of the screen
player_y_pos = screen_height - player_height  # at the bottom of the screen
player_rect = player.get_rect()
player_gravity = 0

gameover = pygame.image.load("/Users/randyli/personal-proj/dodge/gameover.png")
gameover_size = gameover.get_rect().size  # getting the size of the image
gameover_width = gameover_size[0]  # width
gameover_height = gameover_size[1]  # height

# direction player moves
to_x = 0
to_y = 0

# movement speed
player_speed = 0.6

# font
game_font = pygame.font.Font(None, 40)  # font type set at default and size at 40

# start time info
start_ticks = pygame.time.get_ticks()

# life info
num_life = 5

# falling from sky: mush
mush = pygame.image.load("/Users/randyli/personal-proj/dodge/mush.png")
mush_size = mush.get_rect().size
mush_width = mush_size[0]
mush_height = mush_size[1]
mush_x_pos = random.randint(0, screen_width - mush_width)
mush_y_pos = 0
mush_speed = 10
num_mush = 0

# slime
slime = pygame.image.load("/Users/randyli/personal-proj/dodge/slime.png")
slime_size = slime.get_rect().size
slime_width = slime_size[0]
slime_height = slime_size[1]
slime_x_pos = random.randint(0, screen_width - slime_width)
slime_y_pos = -2 * slime_height
slime_speed = 15
num_slime = 0

total_dodged = num_mush + num_slime

# potion
potion = pygame.image.load("/Users/randyli/personal-proj/dodge/potion.png")
potion_size = potion.get_rect().size
potion_width = potion_size[0]
potion_height = potion_size[1]
potion_x_pos = random.randint(0, screen_width - potion_width)
potion_y_pos = screen_height - (3 * (potion_height/2))
# potion_speed = 30
potion_rect = potion.get_rect()

# dragon
dragon = pygame.image.load("/Users/randyli/personal-proj/dodge/dragon.png")
dragon_size = dragon.get_rect().size
dragon_width = dragon_size[0]
dragon_height = dragon_size[1]
dragon_x_pos = -1 * dragon_width
dragon_y_pos = random.randint(0, screen_height - dragon_height)
dragon_speed = 5
dragon_rect = dragon.get_rect()
num_dragon = 0

# event loop
running = True
while running:
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # convert ms to sec
    dt = clock.tick(10)  # fps on screen
    # print("fps: " + str(clock.get_fps()))  # to printout the fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # check to see if keys are pressed
            if event.key == pygame.K_LEFT:  # player to left
                player = pygame.image.load("/Users/randyli/personal-proj/dodge/player.png")
                to_x -= player_speed
            elif event.key == pygame.K_RIGHT:  # to right
                player = pygame.image.load("/Users/randyli/personal-proj/dodge/player_right.png")
                to_x += player_speed
            elif event.key == pygame.K_DOWN:  # squat
                player_gravity = 20
            elif event.key == pygame.K_SPACE:  # jump
                player_gravity = -10
                print("jump")

        if event.type == pygame.KEYUP:  #stopping when event key not pressed
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_DOWN:
                player_gravity = 0
            elif event.key == pygame.K_SPACE:
                player_gravity += 0

    # allows for player to move w keyboard keys
    player_x_pos += to_x * dt
    player_y_pos += to_y * dt

    # player can't leave screen x
    if player_x_pos < 0:
        player_x_pos = 1
    elif player_x_pos > screen_width - player_width:
        player_x_pos = screen_width - (player_width + 1)

    # player can't leave screen y
    if player_y_pos < 0:
        player_y_pos = 1
    elif player_y_pos > screen_height - player_height:
        player_y_pos = screen_height - (player_height + 1)

    # player gravity
    player_gravity += 1
    player_y_pos += player_gravity
    if player_y_pos > screen_height - player_height:
        player_y_pos = screen_height - player_height
    screen.blit(player, player_rect)

    # dropping mush
    mush_y_pos += mush_speed
    if num_mush > 5:
        slime_y_pos += slime_speed

    if total_dodged != 0 and total_dodged % 5 == 0 and num_mush >= 10:
        dragon_x_pos += dragon_speed
        if dragon_x_pos > (-1 * dragon_x_pos) and dragon_x_pos < screen_width:
            dragon_x_pos += dragon_speed

    if mush_y_pos > screen_height:  # dropping more mush when it's gone
        mush_y_pos = 0
        mush_x_pos = random.randint(0, screen_width - mush_width)
    if mush_y_pos == 0 and bool(player_rect.colliderect(mush_rect)) == 0:
        num_mush += 1

    # dropping slime
    if num_mush >= 4:
        if slime_y_pos > screen_height:  # dropping more slime when it's gone
            slime_y_pos = 0
            slime_x_pos = random.randint(0, screen_width - slime_width)
        if slime_y_pos == 0 and bool(player_rect.colliderect(slime_rect)) == 0:
            num_slime += 1

    # potion appearing
    if random.randrange(100) < 1 and potion_y_pos < 0:
        potion_y_pos = screen_height - (3 * (potion_height/2))
        potion_x_pos = random.randint(0, screen_width - potion_width)
    if bool(player_rect.colliderect(potion_rect)) == 1 and num_life < 5:
        num_life += 1
        potion_y_pos = -2 * potion_height
    if bool(player_rect.colliderect(potion_rect)) == 1 and num_life == 5:
        potion_y_pos = -2 * potion_height
    # FIGURE OUT HOW TO MAKE IT DISAPPEAR IN 3 SEC

    # sliding dragon
    if dragon_x_pos > -1 * dragon_width and dragon_x_pos < screen_width:
        dragon_x_pos += dragon_speed
    if dragon_x_pos > screen_width and bool(player_rect.colliderect(dragon_rect)) == 0:
        num_dragon += 1
    if dragon_x_pos > screen_width:
        dragon_x_pos = -1 * dragon_width
        dragon_y_pos = random.randint(0, screen_height - dragon_height)
    if player_rect.colliderect(dragon_rect):
        dragon_x_pos = -1 * dragon_width

    # collision
    player_rect = player.get_rect()
    player_rect.left = player_x_pos
    player_rect.top = player_y_pos

    mush_rect = mush.get_rect()
    mush_rect.left = mush_x_pos
    mush_rect.top = mush_y_pos

    slime_rect = slime.get_rect()
    slime_rect.left = slime_x_pos
    slime_rect.top = slime_y_pos

    potion_rect = potion.get_rect()
    potion_rect.left = potion_x_pos
    potion_rect.top = potion_y_pos

    dragon_rect = dragon.get_rect()
    dragon_rect.left = dragon_x_pos
    dragon_rect.top = dragon_y_pos

    if player_rect.colliderect(mush_rect):
        num_life -= 1
        mush_y_pos = screen_height - 1
        print("bumped into mush!")

    if player_rect.colliderect(slime_rect):
        num_life -= 1
        slime_y_pos = screen_height - 1
        print("bumped into slime!")
    
    if player_rect.colliderect(dragon_rect):
        num_life -= 1
        dragon_x_pos = -1 * dragon_width
        print("jump away from dragon!")

    if num_life == 0:
        running = False
        print("no more lives")

    life_display = pygame.image.load(f"/Users/randyli/personal-proj/dodge/{num_life}.png")

    screen.blit(background, (0, 0))  # loading the background
    # screen.fill((0, 0, 255)) if not image can use rgb to fill the screen

    screen.blit(player, (player_x_pos, player_y_pos))
    screen.blit(mush, (mush_x_pos, mush_y_pos))
    screen.blit(slime, (slime_x_pos, slime_y_pos))
    screen.blit(life_display, (400, 10))
    screen.blit(potion, (potion_x_pos, potion_y_pos))
    screen.blit(dragon, (dragon_x_pos, dragon_y_pos))

    if num_life == 0:
        screen.blit(gameover, ((screen_width/2 - gameover_width/2), (screen_height/2 - gameover_height/2)))

    total_dodged = num_mush + num_slime + num_dragon
    count = game_font.render(str(int(total_dodged)), True, (255, 255, 255))
    screen.blit(count, (10, 10))

    pygame.display.update()  # updating the background

# delay quitting
pygame.time.delay(2000)  # 2ms

# quit game
pygame.quit()
