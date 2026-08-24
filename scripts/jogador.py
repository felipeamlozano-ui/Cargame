import pygame
from scripts.recursos import Recursos

class Jogador:
    def __init__(self, tela, x, y):
        self.tela = tela
        self.posicao = [x, y]
        # Carrega a imagem original do carro
        self.imagem = Recursos.get_imagem('assets/carro.png')
        # Pega o tamanho real da imagem ou podemos forçar um tamanho
        self.tamanho = self.imagem.get_size()
        self.rect = pygame.Rect(self.posicao, self.tamanho)
        
        self.velocidadeMaxima = 300 # pixels por segundo

    def desenhar(self):
        self.tela.blit(self.imagem, self.rect.topleft)

    def atualizar(self, dt):
        self.teclas = pygame.key.get_pressed()
        
        # Movimentação lateral
        if self.teclas[pygame.K_LEFT] or self.teclas[pygame.K_a]:
            self.posicao[0] -= self.velocidadeMaxima * dt
        if self.teclas[pygame.K_RIGHT] or self.teclas[pygame.K_d]:
            self.posicao[0] += self.velocidadeMaxima * dt
            
        # Limita o carro nas bordas da tela
        largura_tela = self.tela.get_width()
        if self.posicao[0] < 0:
            self.posicao[0] = 0
        elif self.posicao[0] > largura_tela - self.tamanho[0]:
            self.posicao[0] = largura_tela - self.tamanho[0]
            
        # Atualiza o rect
        self.rect.topleft = (int(self.posicao[0]), int(self.posicao[1]))

    def getRect(self):
        return self.rect
