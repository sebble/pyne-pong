#!/usr/bin/env python

# import the pygame module, so you can use it
import pygame
import random
import math
from pygame.sprite import Sprite

WIDTH, HEIGHT = 640, 480
HEIGHT = int(WIDTH/4.0*3.0)
SPEED = int(WIDTH/64)

PADDLE_DEPTH = WIDTH / 128
PADDLE_LENGTH = HEIGHT / 12


# no operation, dummy function
def nop():
    pass

class Score(Sprite):
    """
    Displays the game score.

    """
    def __init__(self, color, position):
        pygame.sprite.Sprite.__init__(self)
        self.color = pygame.Color(color)
        self.score = [0,0]

        self.font = pygame.font.Font(None, 36)
        self.render_text()
        self.rect = self.image.get_rect()
        self.rect.center = position

    def render_text(self):
        self.image = self.font.render("{0}     {1}".format(*self.score), True, self.color)

    def increase(self, side):
        self.score[side] += 1
        self.render_text()


class Ball(Sprite):
    """
    Handles behaviour of the ball.

    """
    def __init__(self, color, position, rackets, score):
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

        # remember racket sprites for collision check
        self.rackets = rackets

        # remember score
        self.score = score

    def update(self):
        self.rect.move_ip(*self.velocity)

        # bounce the ball of the top screen border
        if self.rect.top < 0:
            self.velocity[1] *= -1
            self.rect.top = 1
        # bounce the ball of the bottom screen border
        elif self.rect.bottom > HEIGHT:
            self.velocity[1] *= -1
            self.rect.bottom = HEIGHT-1

        # detect collision with the rackets
        for racket in self.rackets:
            if self.rect.colliderect(racket.rect):
                # bounce the ball of the racket
                self.velocity[0] *= -1
                self.rect.x += self.velocity[0]
                # pass some racket velocity to the ball
                self.velocity[1] += 0.5 * racket.velocity
                # don't check both rackets
                break

        # detect goal
        if self.rect.centerx < 0 or self.rect.centerx > WIDTH:
            # add a point to the score
            side = 1 if self.rect.centerx < 0 else 0
            self.score.increase(side)
            # set the ball in the starting position
            self.rect.center = self.start

            self.velocity = [0,0]


    def serve(self):
        # if the ball is already in play, do nothing
        if self.velocity[0] != 0:
            return

        # random angle in radians (between 0 and 90 degrees)
        angle = random.uniform(1, math.pi/8.0*3.0)
        angle *= random.choice([-1,1])

        # choose serving side randomly
        side = random.choice([-1,1])
        # rotate the velocity vector [5, 0], flip horizontally if side < 0
        self.velocity = [side * SPEED * math.cos(angle), SPEED * math.sin(angle)]


class Racket(Sprite):
    """
    Handles behaviour of the players racket.

    """
    def __init__(self, color, position):
        Sprite.__init__(self)
        self.image = pygame.Surface([PADDLE_DEPTH, PADDLE_LENGTH])
        self.rect = pygame.Rect(0, 0, PADDLE_DEPTH, PADDLE_LENGTH) # (x, y, WIDTH, HEIGHT)
        pygame.draw.rect(self.image, pygame.Color(color), self.rect)
        self.rect.center = position

        # one dimensional velocity vector (vertical axis only)
        self.velocity = 0

    def up(self):
        self.velocity -= SPEED

    def down(self):
        self.velocity += SPEED

    def update(self):
        self.rect.move_ip(0, self.velocity)
        # move only within the screen border
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(HEIGHT, self.rect.bottom)

# Make some IA !
class Agent():
    def __init__(self, ball, racket):
        self.racket = racket

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
        pygame.draw.line(background, pygame.Color("white"), (WIDTH/2,y), (WIDTH/2,y+3))

    # draw background on screen
    screen.blit(background, (0, 0))

    # display screen surface
    pygame.display.flip()

    # clock to control the game frame rate
    clock = pygame.time.Clock()

    # create two racket sprites
    player1 = Racket("green", (10, HEIGHT/2))
    player2 = Racket("orange", (WIDTH - 10, HEIGHT/2))

    # create the score sprite
    pygame.font.init()
    score = Score("grey", (WIDTH/2,HEIGHT/12))

    # create the ball sprite
    ball = Ball("white", (WIDTH/2,HEIGHT/2), [player1, player2], score)

    # create the AI
    ai = Agent(ball, player2)

    # A map for keys
    key_map = {
        pygame.K_w: [player1.up, player1.down],
        pygame.K_s: [player1.down, player1.up],
        pygame.K_UP: [player2.up, player2.down],
        pygame.K_DOWN: [player2.down, player2.up],
        pygame.K_SPACE: [ball.serve, nop]

    }

    # list of sprites to render
    sprites = pygame.sprite.RenderClear([ball, player1, player2, score])

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

