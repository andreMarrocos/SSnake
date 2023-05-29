import Buttons
import pygame
import random
import tkinter
from pygame.locals import *
from pygame import mixer
from tkinter import *

# trabalhando com musica aqui
#frame = tkinter.Tk()
#frame.geometry = ("400x600")
#label_music = tkinter.LabelFrame()
#label_music.pack(ipady = 300, ipadx=300 )
#volume_mixer_music = tkinter.Scale(label_music)
#volume_mixer_music.pack()
#frame.mainloop()

# Create Game Window
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Menu')


def on_grid_random():
    x = random.randint(0, 1270)
    y = random.randint(0, 710)
    return x // 10 * 10, y // 10 * 10


# Collisions
def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


def off_limits(pos):
    if 0 <= pos[0] < screen_width and 0 <= pos[1] < screen_height:
        return False
    else:
        return True


# write function
def screenText(text, color, x, y, size, style, bold=False, itallic=False):
    font = pygame.font.SysFont(style, size, bold=bold, italic=itallic)
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))


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
            if options_button.draw(screen):
                pass
            if quit_button.draw(screen):
                pygame.quit()
        pygame.display.update()

# Variables
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
clock = pygame.time.Clock()
volume = 0.02

# load button images
play_img = pygame.image.load('Images/Play Rect.png').convert_alpha()
resume_img = pygame.image.load('Images/resume.png').convert_alpha()
options_img = pygame.image.load('Images/Options Rect.png').convert_alpha()
bg_img = pygame.image.load('Images/Background.png').convert_alpha()
quit_img = pygame.image.load('Images/Quit Rect.png').convert_alpha()
up_img = pygame.image.load('Images/up.png').convert_alpha()
down_img = pygame.image.load('Images/down.png').convert_alpha()
music_img = pygame.image.load('Images/music.png').convert_alpha()
return_img = pygame.image.load('Images/return.png').convert_alpha()

# Create button instaces
play_button = Buttons.Button(550, 200, play_img, 0.4)
resume_button = Buttons.Button(550, 200, resume_img, 0.4)
options_button = Buttons.Button(550, 300, options_img, 0.4)
quit_button = Buttons.Button(550, 400, quit_img, 0.4)
music_button = Buttons.Button(550, 300, music_img, 0.4)
return_button = Buttons.Button(550, 400, return_img, 0.4)
up_button = Buttons.Button(500, 310, up_img, 0.4)
down_button = Buttons.Button(708, 310, down_img, 0.4)

# Music/Sounds
pygame.mixer.music.set_volume(volume)
mixer.music.load('sounds/AdhesiveWombat - Night Shade.mp3')
mixer.music.play(-1)
collision_sound = pygame.mixer.Sound('sounds/Mario-coin-sound.mp3')
collision_sound.set_volume(volume)

# Create Apple
apple = pygame.Surface((10, 10))
apple.fill((255, 0, 0))
apple_pos = on_grid_random()

# Create Snake
snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((255, 255, 255))


# Menu Loop
def main_menu():
    while True:
        pygame.display.set_caption('Menu')
        screen.blit(bg_img, (0, 0))
        play_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)

        screenText("SSnake", (255, 255, 255), 530, 100, size=50, style="arialblack")

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
    while True:
        pygame.display.set_caption('Options')
        screen.blit(bg_img, (0, 0))
        music_button.draw(screen)
        return_button.draw(screen)
        up_button.draw(screen)
        down_button.draw(screen)
        screenText("Options", (255, 255, 255), 530, 100, size=50, style="arialblack")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if up_button.draw(screen):
                    volume += 0.01
                if down_button.draw(screen):
                    volume -= 0.01
                if return_button.draw(screen):
                    main_menu()
        pygame.display.update()


# Game Loop
def play():
    apple_pos = on_grid_random()
    my_direction = DOWN
    score = 0
    pygame.display.set_caption('Play')

    while True:

        screen.fill((0, 0, 0))
        screen.blit(apple, apple_pos)

        for pos in snake:
            screen.blit(snake_skin, pos)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    my_direction = UP
                elif event.key in (K_DOWN, K_s):
                    my_direction = DOWN
                elif event.key in (K_LEFT, K_a):
                    my_direction = LEFT
                elif event.key in (K_RIGHT, K_d):
                    my_direction = RIGHT
                elif event.key == K_SPACE:
                    pause()

        if collision(snake[0], apple_pos):
            apple_pos = on_grid_random()
            snake.append((0, 0))
            collision_sound.play()
            score += 10

        for i in range(len(snake) - 1, 0, -1):
            if collision(snake[0], snake[i]):
                pygame.quit()

        if off_limits(snake[0]):
            pygame.quit()

        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i - 1][0], snake[i - 1][1])

        if my_direction == UP:
            snake[0] = (snake[0][0], snake[0][1] - 10)
        if my_direction == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 10)
        if my_direction == RIGHT:
            snake[0] = (snake[0][0] + 10, snake[0][1])
        if my_direction == LEFT:
            snake[0] = (snake[0][0] - 10, snake[0][1])

        screenText(f"Score {score}", (255, 255, 255), 10, 10, size=30, style="arialblack")

        pygame.display.update()
        clock.tick(10)


main_menu()
