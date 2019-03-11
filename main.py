import pygame
from config import config
from src import Game

def main():
    display = pygame.display.set_mode((config["game"]["height"], config["game"]["width"]))
    pygame.display.set_caption('Rycerz')
    game = Game(display)
    game.loop()

if __name__ == '__main__':
    main()