#!/usr/bin/env python

# import the pygame module, so you can use it
import pygame

# define a main function
def main():
    # create a screen surface of a given size
    screen = pygame.display.set_mode((320,240))

    # set window caption
    pygame.display.set_caption("PONG")

    # control variable for the main loop
    running = True

    # create background surface
    background = pygame.Surface([320, 240])
    background.fill(pygame.Color("black"))
    for y in range(0, 240, 10):
        pygame.draw.line(background, pygame.Color("white"), (160,y), (160,y+3))

    # draw background on screen
    screen.blit(background, (0, 0))

    # draw a ball (color, position, radius)
    pygame.draw.circle(screen, pygame.Color("white"), (160,120), 3)

    # draw racket on the left
    rectangle = pygame.Rect(10, 120-10, 4, 20) # (x, y, width, height)
    pygame.draw.rect(screen, pygame.Color("white"), rectangle)

    # draw racket on the right
    rectangle = pygame.Rect(310-4, 120-10, 4, 20) # (x, y, width, height)
    pygame.draw.rect(screen, pygame.Color("white"), rectangle)
    
    # display screen surface
    pygame.display.flip()

    # main game loop
    while running:

        # read events from the event queue
        for event in pygame.event.get():
            # on QUIT event, exit the main loop
            if event.type == pygame.QUIT:
                running = False

# if this module is executed as a script, run the main function
if __name__ == "__main__":
    main()

