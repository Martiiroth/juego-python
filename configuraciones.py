class Configuraciones():
    """Una clase para almacenar todas las configuraciones de Invasión Alienígena."""

    def __init__(self):
        """Inicializa las configuraciones del juego."""
        # Configuraciones de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Configuraciones de la nave
        self.cantidad_naves = 3

        # Configuraciones de las balas
        self.bala_width = 3
        self.bala_height = 15
        self.bala_color = 60, 60, 60
        self.balas_allowed = 3

        # Configuraciones de los alienígenas
        self.fleet_drop_speed = 10
        self.puntaje_escala = 1.5

        # Qué tan rápido se acelera el juego
        self.speedup_scale = 1.1

        self.inicializa_configuraciones_dinamicas()

    def inicializa_configuraciones_dinamicas(self):
        """Inicializa las configuraciones que cambian a lo largo del juego."""
        self.factor_velocidad_nave = 1.5
        self.bala_factor_velocidad = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        # Puntuación
        self.alien_points = 50

    def aumentar_velocidad(self):
        """Aumenta la velocidad de la nave y de los alienígenas, y la cantidad de puntos por alienígena."""
        self.factor_velocidad_nave *= self.speedup_scale
        self.bala_factor_velocidad *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.puntaje_escala)