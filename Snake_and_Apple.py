import pygame
import random

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))


# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Carregando as imagens dos objetos

apple_image = pygame.image.load("Images/apple.png").convert_alpha()
apple_image = pygame.transform.scale(apple_image, (10, 10))
head_image = pygame.image.load("Images/snakehead.png").convert_alpha()
head_image = pygame.transform.scale(head_image, (10, 10))
body_image = pygame.image.load("Images/snakebody.png").convert_alpha()
body_image = pygame.transform.scale(body_image, (10, 10))


# Função para girar uma imagem
def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)

class Snake:
    global score

    def __init__(self):
        self.size = 10
        self.x = 0
        self.y = 0
        self.dx = 10
        self.dy = 0
        self.head_image = head_image
        self.body_image = body_image
        self.body = [(self.x, self.y)]
        self.length = 3
        self.score = 0

        # Inicializa o corpo da cobra
        for i in range(self.length):
            self.body.append((self.x - i * self.size, self.y))

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.dx != self.size:
            self.dx = -self.size
            self.dy = 0
            self.head_image = rotate_image(head_image, 180)
        elif keys[pygame.K_RIGHT] and self.dx != -self.size:
            self.dx = self.size
            self.dy = 0
            self.head_image = rotate_image(head_image, 0)
        elif keys[pygame.K_UP] and self.dy != self.size:
            self.dy = -self.size
            self.dx = 0
            self.head_image = rotate_image(head_image, 90)
        elif keys[pygame.K_DOWN] and self.dy != -self.size:
            self.dy = self.size
            self.dx = 0
            self.head_image = rotate_image(head_image, -90)

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        # Desenha a cabeça da cobra
        screen.blit(self.head_image, (self.body[0][0], self.body[0][1]))

        # Desenha o corpo da cobra
        for i in range(1, len(self.body)):
            segment = self.body[i]
            dx = segment[0] - self.body[i-1][0]
            dy = segment[1] - self.body[i-1][1]
            if dx == self.size:
                image = rotate_image(self.body_image, 0)
            elif dx == -self.size:
                image = rotate_image(self.body_image, 180)
            elif dy == self.size:
                image = rotate_image(self.body_image, -90)
            elif dy == -self.size:
                image = rotate_image(self.body_image, 90)
            screen.blit(image, (segment[0], segment[1]))

    def update_body(self):
        self.body.insert(0, (self.x, self.y))
        if len(self.body) > self.length:
            del self.body[-1]

    def check_collision(self):
        if self.x < 0 or self.x >= screen_width or self.y < 0 or self.y >= screen_height:
            return True
        for segment in self.body[1:]:
            if segment == (self.x, self.y):
                return True
        return False

    def eat_apple(self, apple):
        if self.x == apple.x and self.y == apple.y:
            self.length += 1
            self.score += 10
            apple.generate_new_position()


class Apple:
    def __init__(self):
        self.size = 10
        self.x = random.randint(0, 1280) // 10 * 10
        self.y = random.randint(0, 720) // 10 * 10

    def draw(self):
        screen.blit(apple_image, (self.x, self.y))

    def generate_new_position(self):
        self.x = random.randint(0, 1280) // 10 * 10
        self.y = random.randint(0, 720) // 10 * 10
