import pygame

class Player:

    def __init__(self, start_pos):
        # Método de inicialización del jugador, que se llama al crear una instancia de la clase.
        self.x, self.y = start_pos
        # Establece las coordenadas iniciales del jugador a partir de la posición proporcionada (start_pos).
        self.direction = 'down'
        # Inicializa la dirección del jugador como 'abajo' (por defecto).
        self.load_images()
        # Llama al método load_images para cargar las imágenes asociadas con el jugador.

    def load_images(self):

        self.images = {
            'up': pygame.image.load("img_player/player_up.png"),
            # Carga la imagen correspondiente a cuando el jugador se mueve hacia arriba.
            'down': pygame.image.load("img_player/player_down.png"),
            # Carga la imagen correspondiente a cuando el jugador se mueve hacia abajo.
            'left': pygame.image.load("img_player/player_left.png"),
            # Carga la imagen correspondiente a cuando el jugador se mueve hacia la izquierda.
            'right': pygame.image.load("img_player/player_right.png")
            # Carga la imagen correspondiente a cuando el jugador se mueve hacia la derecha.
        }

    def move(self, dx, dy):
        # Método para mover al jugador, cambiando su posición y dirección.
        self.x += dx
        # Incrementa o disminuye la posición x del jugador según el valor de dx.
        self.y += dy
        # Incrementa o disminuye la posición y del jugador según el valor de dy.
        if dx < 0:
            self.direction = 'left'
            # Si dx es negativo, el jugador se está moviendo a la izquierda.
        elif dx > 0:
            self.direction = 'right'
            # Si dx es positivo, el jugador se está moviendo a la derecha.
        elif dy < 0:
            self.direction = 'up'
            # Si dy es negativo, el jugador se está moviendo hacia arriba.
        elif dy > 0:
            self.direction = 'down'
            # Si dy es positivo, el jugador se está moviendo hacia abajo.

    def draw(self, screen, level_info):
        # Método para dibujar al jugador en la pantalla.
        tile_size, offset_x, offset_y = level_info
        # Obtiene el tamaño de los "tiles" y los desplazamientos en x e y desde la información del nivel.
        player_image = pygame.transform.smoothscale(self.images[self.direction], (tile_size, tile_size))
        # Escala la imagen del jugador (según su dirección actual) para que coincida con el tamaño del tile.
        screen.blit(player_image, (offset_x + self.x * tile_size, offset_y + self.y * tile_size))
        # Dibuja la imagen del jugador en la pantalla, ajustada por su posición y los desplazamientos.
