import pygame
from pygame.locals import *
import sys
from random import randrange, randint

pygame.init()

# FPS
fps = 60
fpsClock = pygame.time.Clock()

# Pantalla
width, height = 800, 298
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dog Scape")


# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Fuente
fuente = pygame.font.SysFont("Comic Sans MS", 30)


class BackGround(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.right = []
        self.left = []
        self.index = 0
        self.vida = 3
        self.puntos = 0

        for i in range(1, 9):
            img = pygame.image.load(f"assets/sprites/running/running_{i}.png").convert()
            img = pygame.transform.scale(img, (65, 50))
            self.right.append(img)
            self.left.append(pygame.transform.flip(img, True, False))
            self.image = self.right[self.index]
            self.rect = self.image.get_rect()

    def update_right(self):
        self.index += 1
        if self.index >= len(self.right):
            self.index = 0

        self.image = self.right[self.index]

    def update_left(self):
        self.index += 1
        if self.index >= len(self.left):
            self.index = 0

        self.image = self.left[self.index]


class Helado(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(f"assets/img/helado.png").convert()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.image.convert_alpha()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, width - 20, 50)

    def update(self):
        speed = randint(3, 5)
        self.rect.y += speed
        if self.rect.y >= height:
            self.rect.x = randrange(0, width - 20, 50)
            self.rect.y = 0


# Player settings
player = Player()  # spawn player
player.rect.x = 0  # go to x
player.rect.y = height - 50  # go to y
player_list = pygame.sprite.Group()
player_list.add(player)

# helado settings
helado_list = pygame.sprite.Group()
for i in range(5):
    helado = Helado()  # spawn helado
    helado_list.add(helado)

# Backgorund
Background = BackGround("assets/img/metro_2.png", [0, 0])

# Premio
Premio_img = pygame.transform.scale(
    pygame.image.load("assets/img/dogbiscuit.png"), (20, 20)
)
Premio_rect = (randrange(0, width - 35, 40), height - 35)


# Loop principal
while True:
    keys = pygame.key.get_pressed()
    screen.fill([255, 255, 255])
    screen.blit(Background.image, Background.rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if keys[pygame.K_RIGHT]:
        player.update_right()
        if player.rect.x + 65 < width:
            player.rect.x += 5

    elif keys[pygame.K_LEFT]:
        player.update_left()
        if player.rect.x > 0:
            player.rect.x -= 5

    if player.rect.x == Premio_rect[0] or player.rect.x + 65 == Premio_rect[0]:
        player.puntos += 1
        Premio_rect = (randrange(0, width - 35, 40), height - 35)

    hits = pygame.sprite.spritecollide(player, helado_list, True)
    if hits:
        player.vida -= 1
        if player.vida == 0:
            print("perdiste")
            pygame.quit()
            sys.exit()

    # Updates and drawing
    screen.blit(Premio_img, Premio_rect)
    screen.blit(fuente.render(f"Vidas: {player.vida}", True, BLANCO), (0, 5))
    screen.blit(fuente.render(f"Puntuacion: {player.puntos}", True, BLANCO), (0, 50))
    helado_list.update()
    player_list.draw(screen)
    helado_list.draw(screen)
    pygame.display.flip()
    fpsClock.tick(fps)
