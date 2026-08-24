import pygame
import math

# ---- Constantes de Layout HD (1280x720) ----
LARGURA  = 1280
ALTURA   = 720
CX       = LARGURA // 2   # Centro X

# ---- Paleta de cores da UI ----
COR_NEON_AZUL    = (80, 200, 255)
COR_NEON_ROXO    = (180, 80, 255)
COR_NEON_VERDE   = (80, 255, 160)
COR_BRANCO       = (255, 255, 255)
COR_AMARELO      = (255, 220, 50)
COR_VERMELHO_VIF = (220, 40,  40)
COR_PRETO_SEMI   = (0,   0,  0, 160)


class Texto:
    def __init__(self, tela, texto, x, y, cor, tamanho):
        self.tela    = tela
        self.texto   = texto
        self.posicao = (x, y)
        self.cor     = cor
        self.tamanho = tamanho
        pygame.font.init()
        self.fonte = pygame.font.Font(None, self.tamanho)
        self.imagemTexto = self.fonte.render(self.texto, True, self.cor)

    def desenhar(self):
        self.tela.blit(self.imagemTexto, self.posicao)

    def atualizarTexto(self, novoTexto):
        self.imagemTexto = self.fonte.render(novoTexto, True, self.cor)


class Botao:
    """Botão moderno com borda neon e efeito de hover."""

    def __init__(self, tela, texto, cx, cy, largura, altura, cor_borda, cor_texto):
        self.tela      = tela
        self.cx        = cx
        self.cy        = cy
        self.largura   = largura
        self.altura    = altura
        self.cor_borda = cor_borda
        self.cor_texto = cor_texto
        self.texto_str = texto
        pygame.font.init()
        self.fonte = pygame.font.Font(None, int(altura * 1.4))
        self.surf_texto = self.fonte.render(texto, True, cor_texto)
        self.tempo = 0.0

    @property
    def rect(self):
        return pygame.Rect(
            self.cx - self.largura // 2,
            self.cy - self.altura  // 2,
            self.largura,
            self.altura
        )

    def desenhar(self, dt=0.016):
        self.tempo += dt
        r = self.rect
        hover = r.collidepoint(pygame.mouse.get_pos())

        # Pulso suave da borda
        pulso = int(40 * math.sin(self.tempo * 3))

        # Fundo semi-transparente
        fundo = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        fundo.fill((0, 0, 0, 140 if hover else 100))
        self.tela.blit(fundo, r.topleft)

        # Borda neon com brilho
        cor = tuple(min(255, c + pulso + (40 if hover else 0)) for c in self.cor_borda)
        pygame.draw.rect(self.tela, cor, r, 3, border_radius=10)

        # Glow: borda extra mais grossa e translúcida
        glow_surf = pygame.Surface((r.width + 12, r.height + 12), pygame.SRCALPHA)
        cor_glow = (*[min(255, c + pulso) for c in self.cor_borda], 60)
        pygame.draw.rect(glow_surf, cor_glow,
                         (0, 0, r.width + 12, r.height + 12), 4, border_radius=14)
        self.tela.blit(glow_surf, (r.x - 6, r.y - 6))

        # Texto centralizado
        tx = r.centerx - self.surf_texto.get_width()  // 2
        ty = r.centery - self.surf_texto.get_height() // 2
        self.tela.blit(self.surf_texto, (tx, ty))

    def get_click(self):
        r = self.rect
        return r.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]


def _draw_neon_text(surface, fonte, texto, cx, cy, cor, glow_cor=None, glow_passes=3):
    """Renderiza texto com efeito neon (glow ao redor)."""
    if glow_cor is None:
        glow_cor = cor
    for offset in range(glow_passes, 0, -1):
        alpha = max(0, 255 - offset * 60)
        glow = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        surf = fonte.render(texto, True, (*glow_cor, alpha))
        gx = cx - surf.get_width() // 2
        gy = cy - surf.get_height() // 2
        for dx in [-offset, 0, offset]:
            for dy in [-offset, 0, offset]:
                glow.blit(surf, (gx + dx, gy + dy))
        surface.blit(glow, (0, 0))
    # Texto principal nítido
    surf_main = fonte.render(texto, True, cor)
    surface.blit(surf_main, (cx - surf_main.get_width() // 2, cy - surf_main.get_height() // 2))
