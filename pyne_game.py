#!/usr/bin/env python

# import the pygame module, so you can use it
import pygame
import random
import math
from pygame.sprite import Sprite

WIDTH, HEIGHT = 320, 240


# no operation, dummy function
def nop():
    pass

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

        # two dimensional velocity vector
        self.velocity = [0,0]
        # remember starting point
        self.start = position

    def update(self):
        self.rect.move_ip(*self.velocity)

    def serve(self):
        # random angle in radians (between 0 and 90 degrees)
        angle = random.uniform(0, math.pi/2)
        angle *= random.choice([-1,1])

        # choose serving side randomly
        side = random.choice([-1,1])
        # rotate the velocity vector [5, 0], flip horizontally if side < 0
        self.velocity = [side * 5 * math.cos(angle), 5 * math.sin(angle)]
        # restore the ball starting position
        self.rect.center = self.start


class Racket(Sprite):
    """
    Handles behaviour of the players racket.

    """
    def __init__(self, color, position):
        Sprite.__init__(self)
        self.image = pygame.Surface([4, 20])
        self.rect = pygame.Rect(0, 0, 4, 20) # (x, y, WIDTH, HEIGHT)
        pygame.draw.rect(self.image, pygame.Color(color), self.rect)
        self.rect.center = position

        # one dimensional velocity vector (vertical axis only)
        self.velocity = 0

    def up(self):
        self.velocity -= 5

    def down(self):
        self.velocity += 5

    def update(self):
        self.rect.move_ip(0, self.velocity)
        # move only within the screen border
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(240, self.rect.bottom)


# define a main function
def main():
    # create a screen surface of a given size
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    # set window caption
    pygame.display.set_caption("PONG")

    # control variable for the main loop
    running = True

    # create background surface
    background = pygame.Surface([WIDTH, HEIGHT])
    background.fill(pygame.Color("black"))
    for y in range(0, HEIGHT, 10):
        pygame.draw.line(background, pygame.Color("white"), (WIDTH / 2,y), (WIDTH / 2,y+3))

    # draw background on screen
    screen.blit(background, (0, 0))

    # display screen surface
    pygame.display.flip()

    # clock to control the game frame rate
    clock = pygame.time.Clock()

    # create the ball sprite
    ball = Ball("white", (WIDTH /2,HEIGHT /2))

    # create two racket sprites
    player1 = Racket("green", (10, 120))
    player2 = Racket("orange", (310, 120))

    # A map for keys
    key_map = {
        pygame.K_w: [player1.up, player1.down],
        pygame.K_s: [player1.down, player1.up],
        pygame.K_UP: [player2.up, player2.down],
        pygame.K_DOWN: [player2.down, player2.up],
        pygame.K_SPACE: [ball.serve, nop]

    }

    # list of sprites to render
    sprites = pygame.sprite.RenderPlain([ball, player1, player2])

    # main game loop
    while running:

        # set game frame rate
        clock.tick(120)
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

            # on key press
            elif event.type == pygame.KEYDOWN and event.key in key_map:
                key_map[event.key][0]()
            # on key release
            elif event.type == pygame.KEYUP and event.key in key_map:
                key_map[event.key][1]()


# if this module is executed as a script, run the main function
if __name__ == "__main__":
    main()

