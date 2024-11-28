import pygame
from pygame.sprite import Sprite

class Nave(Sprite):
    """Clase para gestionar la nave."""

    def __init__(self, ai_configuraciones, pantalla):
        """Inicializa la nave y establece su posición inicial."""
        super(Nave, self).__init__()
        self.ai_configuraciones = ai_configuraciones
        self.pantalla = pantalla

        # Carga la imagen de la nave y obtiene su rectángulo
        self.image = pygame.image.load('imagenes/nave.bmp')
        self.rect = self.image.get_rect()
        self.pantalla_rect = pantalla.get_rect()

        # Inicia cada nueva nave en la parte inferior central de la pantalla
        self.rect.centerx = self.pantalla_rect.centerx
        self.rect.bottom = self.pantalla_rect.bottom

        # Almacena un valor decimal para el centro de la nave
        self.center = float(self.rect.centerx)

        # Bandera de movimiento
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Actualiza la posición de la nave basada en la bandera de movimiento."""
        if self.moving_right and self.rect.right < self.pantalla_rect.right:
            self.center += self.ai_configuraciones.factor_velocidad_nave

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_configuraciones.factor_velocidad_nave

        # Actualiza el objeto rect de acuerdo a self.center
        self.rect.centerx = self.center 

    def blitme(self):
        """Dibuja la nave en su posición actual."""
        self.pantalla.blit(self.image, self.rect)

    def centrar_nave(self):
        """Centra la nave en la pantalla."""
        self.center = self.pantalla_rect.centerx