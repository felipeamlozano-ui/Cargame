import pygame
import sys
import math
from scripts.cenas import Partida, Menu, GameOver

pygame.init()

# --- Configurações da Tela ---
LARGURA, ALTURA = 1280, 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo do Carro")
relogio = pygame.time.Clock()
TARGET_FPS = 120

# --- Paleta de Cores ---
COR_ASFALTO       = (30, 30, 40)
COR_ASFALTO_CLARA = (42, 42, 55)
COR_GRAMA_ESCURA  = (20, 80, 30)
COR_GRAMA_CLARA   = (30, 105, 40)
COR_FAIXA         = (220, 220, 220)
COR_FAIXA_AMARELA = (255, 200, 0)
COR_CEU_TOPO      = (10, 10, 25)
COR_CEU_BASE      = (30, 20, 60)

# --- Estado das Cenas ---
listaCenas = {
    'partida': Partida(tela),
    'menu':    Menu(tela),
    'game_over': GameOver(tela)
}
cenaAtual = 'menu'

# --- Variáveis de animação da pista ---
linha_y      = 0.0
detalhe_y    = 0.0  # Animação dos detalhes de polígono na grama
tempo_total  = 0.0  # Usado para efeitos de ondulação

# ---- Funções de Renderização com Polígonos ----

def desenhar_ceu(surface):
    """Gradiente de céu noturno com polígonos."""
    largura = surface.get_width()
    altura  = surface.get_height()
    # Gradiente vertical por faixas de polígonos (trapézios)
    fatias = 20
    for i in range(fatias):
        t_topo  = i / fatias
        t_base  = (i + 1) / fatias
        r = int(COR_CEU_TOPO[0] + (COR_CEU_BASE[0] - COR_CEU_TOPO[0]) * t_topo)
        g = int(COR_CEU_TOPO[1] + (COR_CEU_BASE[1] - COR_CEU_TOPO[1]) * t_topo)
        b = int(COR_CEU_TOPO[2] + (COR_CEU_BASE[2] - COR_CEU_TOPO[2]) * t_topo)
        y_topo = int(t_topo * altura * 0.5)
        y_base = int(t_base * altura * 0.5)
        pygame.draw.polygon(surface, (r, g, b), [
            (0, y_topo), (largura, y_topo),
            (largura, y_base), (0, y_base)
        ])


def desenhar_estrelas(surface, tempo):
    """Estrelas cintilantes no céu."""
    estrelas = [
        (100, 40), (250, 80), (400, 20), (600, 60),
        (800, 30), (950, 70), (1100, 50), (1200, 15),
        (50,  10), (700, 90), (150, 55), (1050, 25),
        (500, 45), (350, 15), (900, 65), (1150, 80),
    ]
    for i, (sx, sy) in enumerate(estrelas):
        brilho = int(180 + 75 * math.sin(tempo * 1.5 + i * 0.7))
        brilho = max(100, min(255, brilho))
        tamanho = 2 if i % 3 == 0 else 1
        cor = (brilho, brilho, int(brilho * 0.8))
        pygame.draw.circle(surface, cor, (sx, sy), tamanho)


def desenhar_montanhas(surface, tempo):
    """Montanhas de polígonos no horizonte com efeito parallax."""
    largura = surface.get_width()
    horizonte = int(surface.get_height() * 0.5)
    horizonte_y = horizonte + 5

    # Camada 2 - montanhas mais claras (mais perto)
    COR_M2 = (40, 30, 70)
    picos2 = [
        (0, horizonte_y), (60, horizonte - 60), (160, horizonte - 20),
        (280, horizonte - 80), (380, horizonte - 30), (500, horizonte - 90),
        (620, horizonte - 40), (740, horizonte - 100), (860, horizonte - 35),
        (980, horizonte - 85), (1100, horizonte - 45), (1200, horizonte - 70),
        (largura, horizonte - 20), (largura, horizonte_y),
    ]
    pygame.draw.polygon(surface, COR_M2, picos2)

    # Camada 3 - montanhas ainda mais claras (frente)
    COR_M3 = (25, 50, 55)
    picos3 = [
        (0, horizonte_y), (90, horizonte - 35), (200, horizonte - 5),
        (310, horizonte - 55), (430, horizonte - 15), (540, horizonte - 65),
        (660, horizonte - 10), (770, horizonte - 75), (900, horizonte - 20),
        (1000, horizonte - 50), (1150, horizonte - 15), (largura, horizonte - 40),
        (largura, horizonte_y),
    ]
    pygame.draw.polygon(surface, COR_M3, picos3)


def desenhar_pista(surface, linha_y):
    """Renderiza a pista 2D clássica com faixas rolando."""
    largura = surface.get_width()
    altura  = surface.get_height()
    horizonte_y = 0
    
    # 1. Chão verde escuro base
    surface.fill(COR_GRAMA_ESCURA)

    # 2. Pista (Centralizada, 1020 de largura)
    pista_w = 1020
    pista_x = (largura - pista_w) // 2
    pygame.draw.rect(surface, COR_ASFALTO, (pista_x, horizonte_y, pista_w, altura - horizonte_y))

    # 3. Detalhes na grama (polígonos 2D)
    tam_celula = 100
    deslocamento_grama = int(linha_y * 0.5) % tam_celula
    for i in range(horizonte_y - tam_celula, altura, tam_celula):
        y_atual = i + deslocamento_grama
        # Padrão para a esquerda
        pontos_esq = [
            (0, y_atual), (pista_x, y_atual + 50),
            (pista_x, y_atual + tam_celula), (0, y_atual + 50)
        ]
        pygame.draw.polygon(surface, COR_GRAMA_CLARA, pontos_esq)
        
        # Padrão para a direita
        pontos_dir = [
            (largura - pista_x, y_atual + 50), (largura, y_atual),
            (largura, y_atual + 50), (largura - pista_x, y_atual + tam_celula)
        ]
        pygame.draw.polygon(surface, COR_GRAMA_CLARA, pontos_dir)

    # 4. Faixas da Pista
    deslocamento_pista = int(linha_y) % 80
    for i in range(horizonte_y - 80, altura, 80):
        y_atual = i + deslocamento_pista
        
        # Faixas Amarelas Laterais
        pygame.draw.rect(surface, COR_FAIXA_AMARELA, (pista_x, y_atual, 15, 40))
        pygame.draw.rect(surface, COR_FAIXA_AMARELA, (pista_x + pista_w - 15, y_atual, 15, 40))
        
        # Faixa Branca Central
        pygame.draw.rect(surface, COR_FAIXA, (largura // 2 - 5, y_atual, 10, 40))

# ===== LOOP PRINCIPAL =====
while True:
    dt = relogio.tick(TARGET_FPS) / 1000.0
    dt = min(dt, 0.033)  # Limita dt máximo para evitar saltos físicos
    tempo_total += dt

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if cenaAtual != 'game_over':
        # ---- Velocidade de scroll ----
        velocidade_pista = 400.0
        if cenaAtual == 'partida':
            velocidade_pista = listaCenas['partida'].velocidade_obstaculo

        linha_y    += velocidade_pista * dt
        detalhe_y  += velocidade_pista * 0.5 * dt

        # ---- Renderiza camadas ----
        # Renderiza a pista 2D (ocupando toda a tela)
        desenhar_pista(tela, linha_y)

    # ---- Atualiza a cena atual ----
    cenaAnterior = cenaAtual

    if cenaAtual == 'game_over':
        cenaAtual = listaCenas[cenaAtual].atualizar(dt, listaCenas['partida'].pontosValor)
    else:
        cenaAtual = listaCenas[cenaAtual].atualizar(dt)

    if cenaAnterior == 'menu' and cenaAtual == 'partida':
        listaCenas['partida'].resetar()

    # ---- FPS no título ----
    fps_atual = relogio.get_fps()
    pygame.display.set_caption(f"Jogo do Carro  |  {fps_atual:.0f} FPS")

    pygame.display.flip()
