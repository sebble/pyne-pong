#!/usr/bin/env python

# import the pygame module, so you can use it
import pygame
import random
from pygame.sprite import Sprite

width, height = 320, 240

class Ball(Sprite):
    """
    Handles behaviour of the ball.

    """
    def __init__(self, color, position):
        # call parent class constructor
        Sprite.__init__(self)

        # create surface
        self.image = pygame.Surface([6, 6])
        # draw filled circle
        pygame.draw.circle(self.image, pygame.Color(color), (3,3), 3)

        # get sprite bounding box
        self.rect = self.image.get_rect()
        # set sprite initial position
        self.rect.center = position

    def update(self):
        x = random.randint(-3,3)
        y = random.randint(-3,3)
        self.rect.move_ip(x, y)

class Racket(Sprite):
    """
    Handles behaviour of the players racket.

    """
    def __init__(self, color, position):
        Sprite.__init__(self)
        self.image = pygame.Surface([4, 20])
        self.rect = pygame.Rect(0, 0, 4, 20) # (x, y, width, height)
        pygame.draw.rect(self.image, pygame.Color(color), self.rect)
        self.rect.center = position

    def update(self):
        y = random.randint(-10,10)
        self.rect.move_ip(0, y)

# define a main function
def main():
    # create a screen surface of a given size
    screen = pygame.display.set_mode((width,height))

    # set window caption
    pygame.display.set_caption("PONG")

    # control variable for the main loop
    running = True

    # create background surface
    background = pygame.Surface([width, height])
    background.fill(pygame.Color("black"))
    for y in range(0, height, 10):
        pygame.draw.line(background, pygame.Color("white"), (width / 2,y), (width / 2,y+3))

    # draw background on screen
    screen.blit(background, (0, 0))

    # draw a ball (color, position, radius)
    x, y = width / 2, height / 2
    pygame.draw.circle(screen, pygame.Color("white"), (x,y), 3)

    # draw racket on the left
    rectangle = pygame.Rect(10, (height/2)-10, 4, 20) # (x, y, width, height)
    pygame.draw.rect(screen, pygame.Color("white"), rectangle)

    # draw racket on the right
    rectangle = pygame.Rect(310-4, (height/2)-10, 4, 20) # (x, y, width, height)
    pygame.draw.rect(screen, pygame.Color("white"), rectangle)

    # display screen surface
    pygame.display.flip()

    # clock to control the game frame rate
    clock = pygame.time.Clock()

    # create the ball sprite
    ball = Ball("white", (width /2,height /2))

    # create two racket sprites
    player1 = Racket("green", (10, 120))
    player2 = Racket("orange", (310, 120))

    # list of sprites to render
    sprites = pygame.sprite.RenderPlain([ball, player1, player2])

    # main game loop
    while running:

        # set game frame rate
        clock.tick(60)
        pygame.display.set_caption("PONG - {0:.2f} fps".format(clock.get_fps()))

        # animate sprites
        sprites.update()
        sprites.draw(screen)

        # display screen
        pygame.display.flip()

        # draw background over sprites
        sprites.clear(screen, background)        
        # read events from the event queue
        for event in pygame.event.get():
            # on QUIT event, exit the main loop
            if event.type == pygame.QUIT:
                running = False



# if this module is executed as a script, run the main function
if __name__ == "__main__":
    main()

