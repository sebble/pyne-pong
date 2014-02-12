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
