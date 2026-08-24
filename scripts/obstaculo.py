import pygame
import random
import math
from scripts.recursos import Recursos

# Tamanho maior do cone para resolução HD
TAMANHO_CONE = (72, 90)

class Obstaculo:
    def __init__(self, tela, velocidade_base):
        self.tela = tela
        self.imagem = Recursos.get_imagem('assets/cone.png', TAMANHO_CONE)
        self.tamanho = self.imagem.get_size()

        # Área da pista (excluindo a grama de 130px em cada lado)
        pista_esq = 130 + 15
        pista_dir = self.tela.get_width() - 130 - 15 - self.tamanho[0]
        self.x = float(random.randint(pista_esq, pista_dir))

        # Começa acima da tela
        self.y = -float(self.tamanho[1])

        self.velocidade = velocidade_base

        # Pequena oscilação lateral para dar vida
        self.oscilacao_fase   = random.uniform(0, math.pi * 2)
        self.oscilacao_amp    = random.uniform(0, 18)  # pixels
        self.oscilacao_vel    = random.uniform(1.5, 3.5)  # rad/s
        self.tempo = 0.0

    def atualizar(self, dt):
        self.y += self.velocidade * dt
        self.tempo += dt
        # Oscila levemente para dificultar o desvio
        self.x += math.sin(self.oscilacao_fase + self.tempo * self.oscilacao_vel) \
                  * self.oscilacao_amp * dt

        # Mantém dentro da pista
        pista_esq = 130 + 15
        pista_dir = self.tela.get_width() - 130 - 15 - self.tamanho[0]
        self.x = max(pista_esq, min(self.x, pista_dir))

    def desenhar(self):
        ix, iy = int(self.x), int(self.y)

        # Sombra do cone
        sw = int(self.tamanho[0] * 0.8)
        sh = 12
        sombra = pygame.Surface((sw, sh), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 90), (0, 0, sw, sh))
        self.tela.blit(sombra, (ix + self.tamanho[0] // 2 - sw // 2, iy + self.tamanho[1] - 6))

        # Cone em si
        self.tela.blit(self.imagem, (ix, iy))

    def detectarColisao(self, rectJogador):
        margem = 10
        rect_cone = pygame.Rect(
            self.x + margem,
            self.y + margem,
            self.tamanho[0] - margem * 2,
            self.tamanho[1] - margem * 2,
        )
        return rectJogador.colliderect(rect_cone)

    def saiu_da_tela(self):
        return self.y > self.tela.get_height()
