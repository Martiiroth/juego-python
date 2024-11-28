import sys
import pygame
from pygame.sprite import Group

from configuraciones import Configuraciones
from estadisticas import Estadisticas
from marcador import Marcador
from button import Button
from nave import Nave
import funciones_juegos as fj

def run_game():
    # Inicializa el juego, las configuraciones y crea un objeto para la pantalla
    pygame.init()
    ai_configuraciones = Configuraciones()
    pantalla = pygame.display.set_mode((ai_configuraciones.screen_width, ai_configuraciones.screen_height))
    pygame.display.set_caption("Invasión Alienígena")

    # Crea el botón de Jugar
    play_button = Button(ai_configuraciones, pantalla, "Jugar")
    
    # Crea una instancia para almacenar estadísticas del juego
    estadisticas = Estadisticas(ai_configuraciones)
    marcador = Marcador(ai_configuraciones, pantalla, estadisticas)

    # Crea una nave, un grupo de alien y un grupo de balas
    nave = Nave(ai_configuraciones, pantalla)
    balas = Group()
    aliens = Group()

    # Crea una flota de alienígenas
    fj.crear_flota(ai_configuraciones, pantalla, nave, aliens)

    # Inicia el bucle principal del juego
    while True:
        # Observa eventos de teclado y ratón
        fj.verificar_eventos(ai_configuraciones, pantalla, estadisticas, marcador, play_button, nave, aliens, balas)
        if estadisticas.game_active:
            nave.update()
            fj.update_balas(balas, ai_configuraciones, pantalla, estadisticas, marcador, nave, aliens)
            fj.update_aliens(ai_configuraciones, aliens, nave, estadisticas, pantalla, balas)
        
        fj.actualizar_pantalla(ai_configuraciones, pantalla, estadisticas, marcador, nave, balas, aliens, play_button)

run_game()