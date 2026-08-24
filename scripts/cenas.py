import pygame
from scripts.obstaculo import Obstaculo
from scripts.jogador import Jogador
from scripts.interfaces import Texto
from scripts.interfaces import Botao

class Partida:
    def __init__(self, tela):
        self.tela = tela
        
        # Jogador posicionado no centro inferior da tela
        largura_tela = self.tela.get_width()
        altura_tela = self.tela.get_height()
        
        # Como o tamanho da imagem pode não estar definido até instanciar, passamos a posição desejada
        # Ajustaremos melhor se ficar um pouco fora do centro
        self.jogador = Jogador(tela, largura_tela / 2 - 25, altura_tela - 100)
        
        # Gerenciamento de múltiplos obstáculos (cones)
        self.obstaculos = []
        self.timer_obstaculo = 0 # Temporizador para spawnar cones
        self.intervalo_spawn = 1.0 # Segundos entre um cone e outro
        self.velocidade_obstaculo = 200 # pixels por segundo
        
        # Adiciona o primeiro cone
        self.obstaculos.append(Obstaculo(self.tela, self.velocidade_obstaculo))
        
        self.estado = "partida"
        self.pontosValor = 0
        self.contador_pontos = 0
        self.pontosTexto = Texto(tela, str(self.pontosValor), 10, 10, (255, 255, 255), 40)

    def atualizar(self, dt):
        self.estado = "partida"
        
        # Atualiza física do jogador (carro)
        self.jogador.atualizar(dt)

        # Aumenta a dificuldade com o tempo
        self.velocidade_obstaculo += 5 * dt
        self.intervalo_spawn = max(0.3, self.intervalo_spawn - 0.01 * dt)

        # Spawn de novos cones com o tempo
        self.timer_obstaculo += dt
        if self.timer_obstaculo > self.intervalo_spawn:
            self.obstaculos.append(Obstaculo(self.tela, self.velocidade_obstaculo))
            self.timer_obstaculo = 0
            
        # Lógica de pontuação: pontos baseados no tempo vivo
        self.contador_pontos += dt
        if self.contador_pontos > 1.0: # Ganha 1 ponto a cada 1 segundo
            self.pontosValor += 1
            self.contador_pontos = 0
            self.pontosTexto.atualizarTexto(str(self.pontosValor))

        # Atualiza obstáculos e checa colisão
        for obstaculo in self.obstaculos:
            obstaculo.atualizar(dt)
            if obstaculo.detectarColisao(self.jogador.getRect()):
                self.estado = "game_over"

        # Remove obstáculos que saíram da tela
        self.obstaculos = [obs for obs in self.obstaculos if not obs.saiu_da_tela()]
        
        # Desenha os elementos
        self.jogador.desenhar()
        for obstaculo in self.obstaculos:
            obstaculo.desenhar()
            
        self.pontosTexto.desenhar()

        return self.estado

    def resetar(self):
        largura_tela = self.tela.get_width()
        altura_tela = self.tela.get_height()
        self.jogador = Jogador(self.tela, largura_tela / 2 - 25, altura_tela - 100)
        self.velocidade_obstaculo = 200
        self.intervalo_spawn = 1.0
        self.obstaculos = [Obstaculo(self.tela, self.velocidade_obstaculo)]
        self.timer_obstaculo = 0
        self.pontosValor = 0
        self.contador_pontos = 0
        self.pontosTexto.atualizarTexto(str(self.pontosValor))
        self.estado = "partida"

class Menu:
    def __init__(self, tela):
        self.tela = tela
        self.titulo = Texto(tela, "Jogo do Carro", 150, 50, (255, 255, 255), 60)
        self.estado = "menu"
        self.botao_jogar = Botao(tela, "Jogar", 200, 150, 50, (200, 0, 0), (255, 255, 255))

    def atualizar(self, dt):
        self.estado = "menu"
        self.titulo.desenhar()
        self.botao_jogar.desenhar()

        if self.botao_jogar.get_click():
            self.estado = "partida"
        return self.estado

class GameOver:
    def __init__(self, tela):
        self.tela = tela
        self.titulo = Texto(tela, "GAME OVER", 150, 100, (200, 0, 0), 60)
        self.botao_voltar = Botao(tela, "Voltar ao Menu", 160, 200, 40, (0, 0, 0), (255, 255, 255))
        self.estado = "game_over"
        
    def atualizar(self, dt, pontos=0):
        self.estado = "game_over"
        
        # Fundo escurecido semi-transparente
        s = pygame.Surface((self.tela.get_width(), self.tela.get_height()))
        s.set_alpha(10) # Acumula aos poucos para um efeito legal de escurecer
        s.fill((0, 0, 0))
        self.tela.blit(s, (0, 0))
        
        self.titulo.desenhar()
        
        texto_pontos = Texto(self.tela, f"Pontos: {pontos}", 200, 160, (255, 255, 255), 40)
        texto_pontos.desenhar()
        
        self.botao_voltar.desenhar()
        
        if self.botao_voltar.get_click():
            pygame.time.delay(200)
            self.estado = "menu"
            
        return self.estado
