import pygame
from settings import WIDTH, HEIGH, TAMANHO_CHAO

class Chao (pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        
        self.image = pygame.Surface([WIDTH, TAMANHO_CHAO])
        self.image.fill((99, 99, 99))
        
        self.rect = self.image.get_rect(midbottom=(WIDTH/2, HEIGH))
        
    def update(self):
        pass