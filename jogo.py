import pygame
from settings import WIDTH, HEIGH, TAMANHO_BLOCO
from classes.bloco import Bloco
from classes.chao import Chao
from classes.botao import Botao
from sys import exit
from gerador import gera_numeros

# Inicializa o Pygame e o relógio para controlar o framerate
pygame.init()
clock = pygame.time.Clock()

# Configura a tela do jogo
tela = pygame.display.set_mode((WIDTH, HEIGH))
pygame.display.set_caption("Ninja")

# Carrega a fonte para o texto
font = pygame.font.Font('font/Lato-Regular.ttf', 40)

# Define as cores dos blocos
cores_blocos = {
    2: (255, 0, 0),  # Vermelho
    1: (0, 255, 0),  # Verde
    0: (0, 0, 255)   # Azul
}

# Grupos de sprites para gerenciar blocos, chão e botão
blocos = pygame.sprite.Group()
chao = pygame.sprite.GroupSingle()
botao = pygame.sprite.GroupSingle()
botao.add(Botao())

# Variáveis para controle do jogo
certo_errado_texto = None
tempo_inicial = None
num_bloco = None
vidas = 3
tempo_jogo_restante = 0
clicavel = True

# Estados do jogo
estado_jogo = {
    'inicial': True,
    'jogando': False,
    'final': False
}

# Função para verificar se a soma dos números excluindo o bloco clicado é igual ao número sorteado
def verifica_soma(num_bloco: int) -> str:
    soma = 0
    for i in range(len(numeros_sorteados)):
        if i != num_bloco and i != len(numeros_sorteados) - 1:
            soma += numeros_sorteados[i]
    
    if numeros_sorteados[-1] == soma:
        return "Certo!"
    else:
        return "Errado!"

# Loop principal do jogo
while True:
    # Processa eventos como fechamento da janela e cliques do mouse
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if evento.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            # Se o jogo está no estado inicial
            if estado_jogo['inicial']:
                if botao.sprite.rect.collidepoint(pos):  # Verifica se o botão foi clicado
                    botao.empty()
                    
                    blocos.add(Bloco(cores_blocos[2], 2))
                    blocos.add(Bloco(cores_blocos[1], 1))
                    blocos.add(Bloco(cores_blocos[0], 0))
                    
                    chao.add(Chao())
                    
                    numeros_sorteados = gera_numeros()
                    
                    tempo_inicial_jogo = pygame.time.get_ticks()
                    
                    acertos = 0
                    
                    estado_jogo['inicial'] = False
                    estado_jogo['jogando'] = True
                
            # Se o jogo está em andamento
            elif estado_jogo['jogando']:
                for bloco in blocos:
                    if bloco.rect.collidepoint(pos) and clicavel:  # Verifica se o mouse estava em cima de algum bloco quando foi clicado
                        bloco.clicado = True
                        num_bloco = bloco.pos
                        resultado = verifica_soma(num_bloco)
                        certo_errado_texto = font.render(f"{resultado}", True, (0, 0, 0))
                        
                        certo_errado_texto_rect = certo_errado_texto.get_rect(center=(bloco.posicao[0], bloco.posicao[1] - TAMANHO_BLOCO/2))
                        tempo_inicial = pygame.time.get_ticks()
                        if resultado != "Certo!":
                            vidas -= 1
                        else:
                            acertos += 1

    # Funcionamento do jogo durante estado inicial
    if estado_jogo['inicial']:
        tela.fill((255, 255, 255))
        botao.draw(tela)
        botao.update()
        
        jogar_texto = font.render("Jogar", True, (0, 0, 0)) 
        jogar_texto_rect = jogar_texto.get_rect(center=(WIDTH/2, HEIGH/2))
        
        tela.blit(jogar_texto, jogar_texto_rect)
    
    # Funcionamento do jogo durante estado jogando
    elif estado_jogo['jogando']:
        tela.fill((255, 255, 255))
        blocos.draw(tela)
        blocos.update()
        chao.draw(tela)
        chao.update()
        
        # Desenha os números sobre os blocos
        for i, bloco in enumerate(blocos):
            num_texto = font.render(f"{numeros_sorteados[bloco.pos]}", True, (0, 0, 0))
            num_texto_rect = num_texto.get_rect(center=(bloco.posicao[0], bloco.posicao[1] - TAMANHO_BLOCO/2))
            tela.blit(num_texto, num_texto_rect)
        
        # Desenha o número da soma desejada no canto superior esquerdo
        num_texto = font.render(f"{numeros_sorteados[-1]}", True, (0, 0, 0))
        num_texto_rect = num_texto.get_rect(topleft=(10, 10))
        tela.blit(num_texto, num_texto_rect)
        
        # Calcula o tempo de jogo
        tempo_jogo = pygame.time.get_ticks() - tempo_inicial_jogo
        
        # Verifica se passou um minuto e encerra o jogo
        if (tempo_jogo / 60_000) >= 1:
            blocos.empty()
            chao.empty()
            estado_jogo['final'] = True
            estado_jogo['jogando'] = False
        
        # Exibe o texto de resultado (Certo ou Errado) quando o jogador clica em algum bloco e espera 1 segundo para prosseguir
        if certo_errado_texto:
            tela.blit(certo_errado_texto, certo_errado_texto_rect)
            clicavel = False # Não permite que o jogador clique em outros blocos enquanto está na espera de 1 segundo
            
            if pygame.time.get_ticks() - tempo_inicial >= 1000:
                certo_errado_texto = None
                tempo_inicial = None
                numeros_sorteados = gera_numeros()
                blocos.add(Bloco(cores_blocos[num_bloco], num_bloco))
                clicavel = True
                
                # Verifica se o jogador perdeu todas as vidas e caso tenha perdido, prossegue para a tela final
                if vidas == 0:
                    blocos.empty()
                    chao.empty()
                    estado_jogo['final'] = True 
                    estado_jogo['jogando'] = False
                    tempo_jogo_restante = (60000 - tempo_jogo) / 1000
                    
    # Renderiza o estado final do jogo com tempo restante, pontuação e fim de jogo
    else:
        tela.fill((255, 255, 255))
        acertos_texto = font.render(f"Acertos: {acertos}", True, (0, 0, 0))
        acertos_texto_rect = acertos_texto.get_rect(topleft=(10, 10))
        fim_texto = font.render("Fim de Jogo!", True, (0, 0, 0))
        fim_texto_rect = fim_texto.get_rect(center=(WIDTH/2, HEIGH/2))
        tempo_texto = font.render(f"Tempo Restante: {tempo_jogo_restante}s", True, (0, 0, 0))
        tempo_texto_rect = tempo_texto.get_rect(topright=(WIDTH - 10, 10))
        tela.blit(acertos_texto, acertos_texto_rect)
        tela.blit(fim_texto, fim_texto_rect)
        tela.blit(tempo_texto, tempo_texto_rect)

    pygame.display.update()  # Atualiza a tela
    clock.tick(60)  # Controla o framerate para 60 FPS