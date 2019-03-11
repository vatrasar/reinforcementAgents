from config import config
import pygame
class Block:
    def __init__(self, name: str, position: list):
        self.name=name
        self.position=position

    def __eq__(self, other):
        return abs(self.position[0]-other.position[0])<config["game"]["block_size"] and abs(self.position[1]-other.position[1])<config["game"]["block_size"]

    def __hash__(self):
        return hash(self.position)

    def draw(self,display):
        return pygame.draw.rect(
            display,
            config['colors'][self.name],
            [
                self.position[0],
                self.position[1],
                config["game"]['block_size'],
                config["game"]['block_size']
            ]
        )

