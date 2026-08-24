import pygame
import sys
from scripts.cenas import Partida, Menu, GameOver

pygame.init()

tamanhoTela = [600, 400]
tela = pygame.display.set_mode(tamanhoTela)
pygame.display.set_caption("Jogo do Carro")
relogio = pygame.time.Clock()
corFundo = (100, 100, 100) # Cor de asfalto

listaCenas = {
    'partida': Partida(tela),
    'menu': Menu(tela),
    'game_over': GameOver(tela)
}

cenaAtual = 'menu'

# Variáveis para a pista (linhas brancas no meio)
linha_y = 0

while True:
    dt = relogio.tick(60) / 1000.0
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    if cenaAtual != 'game_over':
        tela.fill(corFundo)

        # Atualiza o movimento das linhas da pista
        velocidade_pista = 200 # Ajusta de acordo com o jogo
        if cenaAtual == 'partida':
            velocidade_pista = listaCenas['partida'].velocidade_obstaculo
            
        linha_y += velocidade_pista * dt
        if linha_y >= 80:
            linha_y -= 80
            
        # Desenha as bordas da pista e grama
        pygame.draw.rect(tela, (34, 139, 34), (0, 0, 50, tela.get_height())) # Grama esquerda
        pygame.draw.rect(tela, (255, 255, 255), (50, 0, 10, tela.get_height())) # Faixa branca
        
        pygame.draw.rect(tela, (34, 139, 34), (tela.get_width() - 50, 0, 50, tela.get_height())) # Grama direita
        pygame.draw.rect(tela, (255, 255, 255), (tela.get_width() - 60, 0, 10, tela.get_height())) # Faixa branca
        
        # Desenha linhas pontilhadas no centro
        meio = tela.get_width() / 2
        for i in range(-80, tela.get_height() + 80, 80):
            pygame.draw.rect(tela, (255, 255, 255), (meio - 5, i + linha_y, 10, 40))
        
    cenaAnterior = cenaAtual
    
    if cenaAtual == 'game_over':
        cenaAtual = listaCenas[cenaAtual].atualizar(dt, listaCenas['partida'].pontosValor)
    else:
        cenaAtual = listaCenas[cenaAtual].atualizar(dt)
        
    if cenaAnterior == 'menu' and cenaAtual == 'partida':
        listaCenas['partida'].resetar()

    pygame.display.flip()
