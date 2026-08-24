import pygame
from scripts.recursos import Recursos

# Tamanho maior e proporcional para HD (pinto mucho do paulo)
TAMANHO_CARRO = (90, 150)

class Jogador:
    def __init__(self, tela, x, y):
        self.tela = tela
        self.posicao = [float(x), float(y)]

        # Carrega o carro com tamanho grande para HD
        self.imagem = Recursos.get_imagem('assets/carro.png', TAMANHO_CARRO)
        self.tamanho = self.imagem.get_size()
        self.rect = pygame.Rect(self.posicao, self.tamanho)

        # Velocidade horizontal mais rápida para a tela maior
        self.velocidadeMaxima = 550  # pixels por segundo

        # --- Efeito visual de inclinação ---
        self.inclinacao = 0.0       # ângulo atual de inclinação
        self.inclinacao_alvo = 0.0  # ângulo destino (suave)

    def desenhar(self):
        # Inclina suavemente o carro na direção do movimento
        if abs(self.inclinacao) > 0.2:
            imagem_rotacionada = pygame.transform.rotate(self.imagem, -self.inclinacao)
            rect_rot = imagem_rotacionada.get_rect(center=self.rect.center)
            self.tela.blit(imagem_rotacionada, rect_rot.topleft)
        else:
            self.tela.blit(self.imagem, self.rect.topleft)

        # Sombra simples abaixo do carro
        sombra_w = int(self.tamanho[0] * 0.85)
        sombra_h = 14
        sx = self.rect.centerx - sombra_w // 2
        sy = self.rect.bottom - 8
        sombra = pygame.Surface((sombra_w, sombra_h), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 80), (0, 0, sombra_w, sombra_h))
        self.tela.blit(sombra, (sx, sy))

    def atualizar(self, dt):
        teclas = pygame.key.get_pressed()

        movendo_esq = teclas[pygame.K_LEFT] or teclas[pygame.K_a]
        movendo_dir = teclas[pygame.K_RIGHT] or teclas[pygame.K_d]

        # Inclinação visual
        if movendo_esq:
            self.inclinacao_alvo = 8.0
        elif movendo_dir:
            self.inclinacao_alvo = -8.0
        else:
            self.inclinacao_alvo = 0.0

        # Interpola suavemente a inclinação
        self.inclinacao += (self.inclinacao_alvo - self.inclinacao) * min(1.0, 10 * dt)

        # Movimentação lateral
        if movendo_esq:
            self.posicao[0] -= self.velocidadeMaxima * dt
        if movendo_dir:
            self.posicao[0] += self.velocidadeMaxima * dt

        # Limita o carro nas bordas da pista (130px de grama em cada lado)
        limite_esq = 130 + 8
        limite_dir = self.tela.get_width() - 130 - 8 - self.tamanho[0]
        self.posicao[0] = max(limite_esq, min(self.posicao[0], limite_dir))

        self.rect.topleft = (int(self.posicao[0]), int(self.posicao[1]))

    def getRect(self):
        # Rect de colisão levemente menor que o visual para ser mais justo
        margem = 12
        return pygame.Rect(
            self.rect.x + margem,
            self.rect.y + margem,
            self.rect.width  - margem * 2,
            self.rect.height - margem * 2,
        )
