from typing import Any
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_configuraciones, pantalla):
        super(Alien, self).__init__()
        self.pantalla = pantalla  
        self.ai_configuraciones = ai_configuraciones

        # Carga la imagen del alienígena y establece su atributo rect
        self.image = pygame.image.load('imagenes/alien.bmp')
        self.rect = self.image.get_rect()

        # Cada nuevo alienígena aparece en la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Almacena la posición exacta del alienígena
        self.x = float(self.rect.x)

    def blitme(self):
        """Dibuja el alienígena en su posición actual"""
        self.pantalla.blit(self.image, self.rect)

    def check_edges(self):
        """Devuelve True si el alienígena está en el borde de la pantalla"""
        screen_rect = self.pantalla.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Mueve el alienígena a la derecha"""
        self.x += (self.ai_configuraciones.alien_speed_factor * self.ai_configuraciones.fleet_direction)
        self.rect.x = self.x