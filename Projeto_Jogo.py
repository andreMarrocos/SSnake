import Buttons
import sys
from Snake_and_Apple import *
from decimal import Decimal
from pygame.locals import *
from pygame import mixer

# Create Game Window
pygame.init()
pygame.display.set_caption('Menu')

# Variables
clock = pygame.time.Clock()
volume = Decimal('0.1')


# load button images
play_img = pygame.image.load('Images/Play Rect.png').convert_alpha()
resume_img = pygame.image.load('Images/resume.png').convert_alpha()
options_img = pygame.image.load('Images/Options Rect.png').convert_alpha()
bg_img = pygame.image.load('Images/SSnake.png').convert_alpha()
quit_img = pygame.image.load('Images/Quit Rect.png').convert_alpha()
up_img = pygame.image.load('Images/up.png').convert_alpha()
down_img = pygame.image.load('Images/down.png').convert_alpha()
volume_img = pygame.image.load('Images/volume.png').convert_alpha()
return_img = pygame.image.load('Images/return.png').convert_alpha()
bggame_img = pygame.image.load('Images/bggame.png').convert_alpha()
bggame_img = pygame.transform.scale(bggame_img, (1280, 720))
# Create button instaces
play_button = Buttons.Button(350, 550, play_img, 1)
resume_button = Buttons.Button(350, 550, resume_img, 1)
options_button = Buttons.Button(550, 550, options_img, 1)
quit_button = Buttons.Button(750, 550, quit_img, 1)
volume_button = Buttons.Button(350, 550, volume_img, 1)
return_button = Buttons.Button(600, 550, return_img, 1)
up_button = Buttons.Button(230, 545, up_img, 1)
down_button = Buttons.Button(465, 545, down_img, 1)


# Music/Sounds
pygame.mixer.music.set_volume(volume)
mixer.music.load('sounds/AdhesiveWombat - Night Shade.mp3')
mixer.music.play(-1)
collision_sound = pygame.mixer.Sound('sounds/Mario-coin-sound.mp3')
collision_sound.set_volume(volume)

# write function
def screenText(text, color, x, y, size, style, bold=False, itallic=False):
    font = pygame.font.SysFont(style, size, bold=bold, italic=itallic)
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))


# Menu Loop
def main_menu():
    while True:
        pygame.display.set_caption('Menu')
        screen.blit(bg_img, (0, 0))
        play_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.draw(screen):
                    play()
                if options_button.draw(screen):
                    options()
                if quit_button.draw(screen):
                    pygame.quit()
        pygame.display.update()


# Options Loop
def options():
    global volume
    while True:
        pygame.display.set_caption('Options')
        screen.blit(bg_img, (0, 0))
        volume_button.draw(screen)
        return_button.draw(screen)
        up_button.draw(screen)
        down_button.draw(screen)
        screenText(f"Options", (255, 255, 255), 530, 100, size=50, style="arialblack")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if up_button.draw(screen) and volume < Decimal('1.0'):
                    volume = volume + Decimal('0.1')
                if down_button.draw(screen) and volume > Decimal('0.0'):
                    volume = volume - Decimal('0.1')
                round(volume, 1)
                pygame.mixer.music.set_volume(volume)
                collision_sound.set_volume(volume)
                if return_button.draw(screen):
                    main_menu()
        pygame.display.update()


# pause loop
def pause():
    screen.fill((0, 0, 0))
    paused = True
    pygame.display.set_caption('Paused')

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if resume_button.draw(screen):
                paused = False
            if quit_button.draw(screen):
                pygame.quit()
        pygame.display.update()


# Game Loop
def play():
    pygame.display.set_caption('Play')
    snake = Snake()
    apple = Apple()

    while True:

        screen.blit(bggame_img, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pause()


        snake.handle_keys()
        snake.move()
        snake.update_body()

        if snake.check_collision():
            pygame.quit()
            sys.exit()

        snake.eat_apple(apple)

        snake.draw()
        apple.draw()

        screenText(f"Score {snake.score}", (255, 255, 255), 10, 10, size=30, style="arialblack")

        pygame.display.flip()
        clock.tick(15)


main_menu()
