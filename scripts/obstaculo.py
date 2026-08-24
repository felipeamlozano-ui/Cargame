import pygame
import random
from scripts.recursos import Recursos

class Obstaculo:
    def __init__(self, tela, velocidade_base):
        self.tela = tela
        # Puxa do cache (Asset Manager)
        self.imagem = Recursos.get_imagem('assets/cone.png')
        self.tamanho = self.imagem.get_size()
        
        # Sorteia uma posição horizontal na tela
        largura_tela = self.tela.get_width()
        self.x = float(random.randint(0, largura_tela - self.tamanho[0]))
        
        # Inicia acima da tela
        self.y = -float(self.tamanho[1])
        
        self.velocidade = velocidade_base

    def atualizar(self, dt):
        self.y += self.velocidade * dt

    def desenhar(self):
        self.tela.blit(self.imagem, (int(self.x), int(self.y)))

    def detectarColisao(self, rectJogador):
        rectCone = pygame.Rect((self.x, self.y), self.tamanho)
        if rectJogador.colliderect(rectCone):
            return True
        return False
        
    def saiu_da_tela(self):
        # Verifica se o cone passou do fundo da tela
        return self.y > self.tela.get_height()
