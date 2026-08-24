import pygame
import math
from scripts.obstaculo import Obstaculo
from scripts.jogador import Jogador
from scripts.interfaces import Texto, Botao, _draw_neon_text

# ---- Constantes de Layout HD (1280x720) ----
LARGURA = 1280
ALTURA  = 720
CX      = LARGURA // 2
CY      = ALTURA  // 2

# ---- Paleta ----
COR_NEON_AZUL   = (80, 200, 255)
COR_NEON_ROXO   = (180, 80,  255)
COR_NEON_VERDE  = (80,  255, 160)
COR_AMARELO     = (255, 220, 50)
COR_VERMELHO    = (220, 40,  40)
COR_BRANCO      = (255, 255, 255)


class Partida:
    def __init__(self, tela):
        self.tela = tela

        # Carro posicionado no centro da pista
        self.jogador = Jogador(tela, CX - 45, ALTURA - 200)

        # Obstáculos
        self.obstaculos          = []
        self.timer_obstaculo     = 0.0
        self.intervalo_spawn     = 0.7   # segundos entre cones
        self.velocidade_obstaculo = 600  # pixels/s

        self.obstaculos.append(Obstaculo(self.tela, self.velocidade_obstaculo))

        self.estado          = "partida"
        self.pontosValor     = 0
        self.contador_pontos = 0.0

        pygame.font.init()
        self._fonte_hud   = pygame.font.Font(None, 72)
        self._fonte_label = pygame.font.Font(None, 36)

    # ---- HUD ----
    def _desenhar_hud(self):
        """HUD de pontuação no canto superior esquerdo com efeito neon."""
        label = self._fonte_label.render("PONTOS", True, COR_NEON_AZUL)
        valor = self._fonte_hud.render(str(self.pontosValor), True, COR_BRANCO)

        # Painel semi-transparente
        painel_w = max(label.get_width(), valor.get_width()) + 30
        painel_h = label.get_height() + valor.get_height() + 20
        painel   = pygame.Surface((painel_w, painel_h), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 120))
        pygame.draw.rect(painel, COR_NEON_AZUL, (0, 0, painel_w, painel_h), 2, border_radius=8)
        self.tela.blit(painel, (18, 18))

        self.tela.blit(label, (18 + (painel_w - label.get_width()) // 2, 24))
        self.tela.blit(valor, (18 + (painel_w - valor.get_width()) // 2,
                                24 + label.get_height() + 4))

    def atualizar(self, dt):
        self.estado = "partida"

        self.jogador.atualizar(dt)

        # Aumenta dificuldade gradualmente
        self.velocidade_obstaculo += 25 * dt
        self.intervalo_spawn       = max(0.2, self.intervalo_spawn - 0.015 * dt)

        # Spawn de cones
        self.timer_obstaculo += dt
        if self.timer_obstaculo >= self.intervalo_spawn:
            self.obstaculos.append(Obstaculo(self.tela, self.velocidade_obstaculo))
            self.timer_obstaculo = 0.0

        # Pontuação
        self.contador_pontos += dt
        if self.contador_pontos >= 1.0:
            self.pontosValor     += 1
            self.contador_pontos  = 0.0

        # Atualiza/colide obstáculos
        for obs in self.obstaculos:
            obs.atualizar(dt)
            if obs.detectarColisao(self.jogador.getRect()):
                self.estado = "game_over"

        self.obstaculos = [o for o in self.obstaculos if not o.saiu_da_tela()]

        # Desenha
        self.jogador.desenhar()
        for obs in self.obstaculos:
            obs.desenhar()

        self._desenhar_hud()

        return self.estado

    def resetar(self):
        self.jogador             = Jogador(self.tela, CX - 45, ALTURA - 200)
        self.velocidade_obstaculo = 600
        self.intervalo_spawn      = 0.7
        self.obstaculos           = [Obstaculo(self.tela, self.velocidade_obstaculo)]
        self.timer_obstaculo      = 0.0
        self.pontosValor          = 0
        self.contador_pontos      = 0.0
        self.estado               = "partida"


class Menu:
    def __init__(self, tela):
        self.tela        = tela
        self.estado      = "menu"
        self.tempo       = 0.0

        pygame.font.init()
        self._fonte_titulo = pygame.font.Font(None, 130)
        self._fonte_sub    = pygame.font.Font(None, 46)

        # Botão centralizado
        self.botao_jogar = Botao(
            tela, "JOGAR",
            cx=CX, cy=CY + 80,
            largura=320, altura=70,
            cor_borda=COR_NEON_VERDE,
            cor_texto=COR_BRANCO
        )

    def atualizar(self, dt):
        self.estado  = "menu"
        self.tempo  += dt

        # Título com pulso
        pulso = int(15 * math.sin(self.tempo * 2.5))
        _draw_neon_text(
            self.tela, self._fonte_titulo,
            "JOGO DO CARRO",
            CX, CY - 110,
            cor=(255, 255, 255),
            glow_cor=COR_NEON_AZUL,
            glow_passes=5
        )

        # Subtítulo
        sub = self._fonte_sub.render("Desvie dos obstáculos e vá o mais longe possível!", True, COR_NEON_AZUL)
        self.tela.blit(sub, (CX - sub.get_width() // 2, CY - 20))

        # Dica de teclas
        dica = self._fonte_sub.render("← → ou A / D para mover", True, (140, 140, 180))
        self.tela.blit(dica, (CX - dica.get_width() // 2, CY + 30))

        self.botao_jogar.desenhar(dt)

        if self.botao_jogar.get_click():
            self.estado = "partida"
        return self.estado


class GameOver:
    def __init__(self, tela):
        self.tela   = tela
        self.estado = "game_over"
        self.tempo  = 0.0

        pygame.font.init()
        self._fonte_titulo = pygame.font.Font(None, 160)
        self._fonte_pontos = pygame.font.Font(None, 90)
        self._fonte_label  = pygame.font.Font(None, 46)

        self.botao_voltar = Botao(
            tela, "VOLTAR AO MENU",
            cx=CX, cy=CY + 160,
            largura=450, altura=70,
            cor_borda=COR_NEON_ROXO,
            cor_texto=COR_BRANCO
        )

    def atualizar(self, dt, pontos=0):
        self.estado = "game_over"
        self.tempo += dt

        # Overlay escurecido acumulativo (retém o frame anterior visível)
        s = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        s.fill((0, 0, 0, 12))
        self.tela.blit(s, (0, 0))

        # "GAME OVER" com neon vermelho pulsante
        _draw_neon_text(
            self.tela, self._fonte_titulo,
            "GAME OVER",
            CX, CY - 150,
            cor=COR_VERMELHO,
            glow_cor=(255, 80, 80),
            glow_passes=6
        )

        # Pontuação
        _draw_neon_text(
            self.tela, self._fonte_pontos,
            f"{pontos} PONTOS",
            CX, CY - 30,
            cor=COR_AMARELO,
            glow_cor=(200, 160, 0),
            glow_passes=4
        )

        # Mensagem motivacional
        msgs = [
            "Boa tentativa!",
            "Quase lá!",
            "Você consegue mais!",
            "Impressionante!",
        ]
        msg = msgs[min(pontos // 10, len(msgs) - 1)]
        surf_msg = self._fonte_label.render(msg, True, (180, 180, 220))
        self.tela.blit(surf_msg, (CX - surf_msg.get_width() // 2, CY + 70))

        self.botao_voltar.desenhar(dt)

        if self.botao_voltar.get_click():
            pygame.time.delay(150)
            self.estado = "menu"

        return self.estado
