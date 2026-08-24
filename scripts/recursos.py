import pygame
import os

class Recursos:
    # Dicionário estático para armazenar imagens em cache
    _imagens = {}

    @classmethod
    def get_imagem(cls, caminho, tamanho=None):
        chave = (caminho, tamanho)
        if chave not in cls._imagens:
            # Se não existe no cache, carrega do disco
            try:
                img = pygame.image.load(caminho).convert_alpha()
                if tamanho is not None:
                    img = pygame.transform.scale(img, tamanho)
                cls._imagens[chave] = img
            except Exception as e:
                print(f"Erro ao carregar a imagem {caminho}: {e}")
                # Cria uma surface vazia caso a imagem falhe (para não quebrar o jogo)
                surface = pygame.Surface((32, 32) if tamanho is None else tamanho)
                surface.fill((255, 0, 255)) # Cor de erro magenta
                cls._imagens[chave] = surface

        return cls._imagens[chave]
