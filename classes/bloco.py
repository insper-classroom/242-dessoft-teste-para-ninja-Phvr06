import pygame
from settings import WIDTH, HEIGH, TAMANHO_BLOCO

class Bloco (pygame.sprite.Sprite):
    def __init__(self, cor: tuple, pos: int) -> None:
        super().__init__()
        
        self.image = pygame.Surface([TAMANHO_BLOCO, TAMANHO_BLOCO])
        self.image.fill(cor)
        
        self.posicao = (WIDTH/2, HEIGH - 99 - pos * TAMANHO_BLOCO)
        
        self.rect = self.image.get_rect(midbottom=self.posicao)
        
        self.pos = pos
        
        self.clicado = False
    
    def apaga(self):
        if self.clicado:
            self.kill()
    
    def update(self):
        self.apaga()