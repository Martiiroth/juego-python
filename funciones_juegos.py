import sys
import pygame
from time import sleep
from bala import Bala
from alien import Alien

def verificar_eventos_keydown(event, ai_configuraciones, pantalla, nave, balas):
    # Responde a eventos de teclado
    if event.key == pygame.K_RIGHT:
        nave.moving_right = True
    elif event.key == pygame.K_LEFT:
        nave.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Verifica que no se hayan disparado más balas que las permitidas
        fuego_bala(ai_configuraciones, pantalla, nave, balas)

def verificar_eventos_keyup(event, nave):
    # Responde a eventos de teclado
    if event.key == pygame.K_RIGHT:
        nave.moving_right = False
    elif event.key == pygame.K_LEFT:
        nave.moving_left = False

def verificar_eventos(ai_configuraciones, pantalla, estadisticas, marcador, play_button, nave, aliens, balas):
    """Responde a eventos de teclado y ratón."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            verificar_eventos_keydown(event, ai_configuraciones, pantalla, nave, balas)
        elif event.type == pygame.KEYUP:
            verificar_eventos_keyup(event, nave)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_configuraciones, pantalla, estadisticas, marcador, play_button, nave, aliens, balas, mouse_x, mouse_y)

def check_play_button(ai_configuraciones, pantalla, estadisticas, marcador, play_button, nave, aliens, balas, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not estadisticas.game_active:
        # Ocultar el mouse
        pygame.mouse.set_visible(False)

        # Reiniciar estadísticas del juego
        estadisticas.reset_stats()
        estadisticas.game_active = True

        # Restablece las imágenes
        marcador.prep_puntaje()
        marcador.prep_alto_puntaje()
        marcador.prep_nivel()
        marcador.prep_naves()

        # Vacía la lista de alien y de balas
        aliens.empty()
        balas.empty()

        # Crea una nueva flota y centra la nave
        crear_flota(ai_configuraciones, pantalla, nave, aliens)
        nave.centrar_nave()

def actualizar_pantalla(ai_configuraciones, pantalla, estadisticas, marcador, nave, balas, aliens, play_button):
    """Actualiza las imágenes en la pantalla y pasa a la nueva pantalla."""
    pantalla.fill(ai_configuraciones.bg_color)
    # Vuelve a dibujar todas las balas detrás de la nave y los alienígenas
    for bala in balas.sprites():
        bala.draw_bala()
    nave.blitme()
    aliens.draw(pantalla)

    # Dibuja la información de la puntuación
    marcador.mostrar_puntaje()

    # Dibuja el botón de Jugar si el juego está inactivo
    if not estadisticas.game_active:
        play_button.draw_button()

    # Hace visible la pantalla más reciente
    pygame.display.flip()

def update_balas(balas, ai_configuraciones, pantalla, estadisticas, marcador, nave, aliens):
    """Actualiza la posición de las balas y se deshace de las balas viejas"""
    balas.update()
    for bala in balas.copy():
        if bala.rect.bottom <= 0:
            balas.remove(bala)

    check_balas_aliens_colisiones(ai_configuraciones, pantalla, estadisticas, marcador, nave, aliens, balas)

def check_balas_aliens_colisiones(ai_configuraciones, pantalla, estadisticas, marcador, nave, aliens, balas):
    """Responde a colisiones entre balas y alienígenas"""
    colisiones = pygame.sprite.groupcollide(balas, aliens, True, True)

    if colisiones:
        for aliens in colisiones.values():
            estadisticas.puntaje += ai_configuraciones.alien_points * len(aliens)
            marcador.prep_puntaje()
        verifica_alto_puntaje(estadisticas, marcador)

    if len(aliens) == 0:
        # Se deshace de las balas existentes y crea una nueva flota
        balas.empty()
        ai_configuraciones.aumentar_velocidad()

        # Aumenta el nivel
        estadisticas.nivel += 1
        marcador.prep_nivel()

        crear_flota(ai_configuraciones, pantalla, nave, aliens)

def verifica_alto_puntaje(estadisticas, marcador):
    """Verifica si hay una nueva puntuación máxima"""
    if estadisticas.puntaje > estadisticas.alto_puntaje:
        estadisticas.alto_puntaje = estadisticas.puntaje
        marcador.prep_alto_puntaje()

def fuego_bala(ai_configuraciones, pantalla, nave, balas):
    """Dispara una bala si no se ha alcanzado el límite permitido"""
    if len(balas) < ai_configuraciones.balas_allowed:
        nueva_bala = Bala(ai_configuraciones, pantalla, nave)
        balas.add(nueva_bala)

def get_number_aliens_x(ai_configuraciones, alien_width):
    """Determina el número de alienígenas que caben en una fila"""
    available_space_x = ai_configuraciones.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_configuraciones, nave_height, alien_height):
    """Determina el número de filas de alienígenas que cabe"""
    available_space_y = (ai_configuraciones.screen_height - (3 * alien_height) - nave_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def crear_alien(ai_configuraciones, pantalla, aliens, alien_number, row_number):
    alien = Alien(ai_configuraciones, pantalla)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def crear_flota(ai_configuraciones, pantalla, nave, aliens):
    """Crea una flota completa de alienígenas"""
    alien = Alien(ai_configuraciones, pantalla)
    number_aliens_x = get_number_aliens_x(ai_configuraciones, alien.rect.width)
    number_rows = get_number_rows(ai_configuraciones, nave.rect.height, alien.rect.height)

    # Crea la flota de alienígenas
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            crear_alien(ai_configuraciones, pantalla, aliens, alien_number, row_number)

def check_fleet_edges(ai_configuraciones, aliens):
    """Responde apropiadamente si algún alienígena ha alcanzado un borde"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_configuraciones, aliens)
            break

def change_fleet_direction(ai_configuraciones, aliens):
    """Hace que toda la flota descienda y cambie de dirección"""
    for alien in aliens.sprites():
        alien.rect.y += ai_configuraciones.fleet_drop_speed
    ai_configuraciones.fleet_direction *= -1 

def nave_golpeada(ai_configuraciones, estadisticas, pantalla, nave, aliens, balas):
    """Responde a una nave siendo golpeada por un alien"""
    if estadisticas.naves_restantes > 0:
        estadisticas.naves_restantes -= 1

        # Vacia la lista de alien y de balas
        aliens.empty()
        balas.empty()

        # Crea una nueva flota y centra la nave
        crear_flota(ai_configuraciones, pantalla, nave, aliens)
        nave.centrar_nave()

        # Pausa
        sleep(0.5)
    else:
        estadisticas.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_configuraciones, estadisticas, pantalla, nave, aliens, balas):
    """Comprueba si algún alienígena ha llegado a la parte inferior de la pantalla"""
    pantalla_rect = pantalla.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= pantalla_rect.bottom:
            # Trata este caso como si la nave fuera golpeada
            nave_golpeada(ai_configuraciones, estadisticas, pantalla, nave, aliens, balas)
            break

def update_aliens(ai_configuraciones, aliens, nave, estadisticas, pantalla, balas):
    """Actualiza la posición de todos los alienígenas en la flota"""
    check_fleet_edges(ai_configuraciones, aliens)
    aliens.update()

    # Busca colisiones entre alienígenas y la nave
    if pygame.sprite.spritecollideany(nave, aliens):
        nave_golpeada(ai_configuraciones, estadisticas, pantalla, nave, aliens, balas)
       
    # Busca alienígenas que hayan llegado a la parte inferior de la pantalla    
    check_aliens_bottom(ai_configuraciones, estadisticas, pantalla, nave, aliens, balas)