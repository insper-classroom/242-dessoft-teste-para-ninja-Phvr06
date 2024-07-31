import pygame
from settings import WIDTH, HEIGH

class Botao (pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        
        self.image = pygame.Surface([WIDTH/3, HEIGH/10])
        self.image.fill((173, 216, 230))
        
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGH/2))
    
    def update(self):
        pass