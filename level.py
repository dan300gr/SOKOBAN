import pygame

class Level:
    def __init__(self, level_data):
        # Inicializa los atributos del nivel con los datos proporcionados
        self.level_data = level_data  
        self.layout = level_data['layout']
        self.level_number = level_data['number']
        self.player_start = self.find_player_start()
        self.player_pos = self.player_start  
        self.boxes = self.find_boxes()
        self.targets = self.find_targets()
        self.walls = self.find_walls()
        self.box_moved = False
        self.level_info = None

    def find_player_start(self):
        # Busca la posición inicial del jugador en el layout
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == '@':
                    return (x, y)
        return (1, 1)  # Posición por defecto si no se encuentra

    def find_boxes(self):
        # Encuentra todas las posiciones de las cajas en el layout
        boxes = []
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == '$':
                    boxes.append((x, y))
        return boxes

    def find_targets(self):
        # Encuentra todas las posiciones de los objetivos en el layout
        targets = []
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == '.':
                    targets.append((x, y))
        return targets

    def find_walls(self):
        # Encuentra todas las posiciones de las paredes en el layout
        walls = []
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == '#':
                    walls.append((x, y))
        return walls

    def move_player(self, player, dx, dy):
        # Intenta mover al jugador en la dirección especificada
        new_x, new_y = player.x + dx, player.y + dy
        self.box_moved = False  # Reinicia el indicador de movimiento de caja

        # Verifica si la nueva posición es una pared
        if (new_x, new_y) in self.walls:
            return False # No se permite el movimiento si hay una pared

        # Verifica si hay una caja en la nueva posición y si se puede mover
        if (new_x, new_y) in self.boxes:
            new_box_x, new_box_y = new_x + dx, new_y + dy
             # Verifica si la caja puede moverse (no debe chocar con paredes ni otras cajas)
            if (new_box_x, new_box_y) not in self.walls and (new_box_x, new_box_y) not in self.boxes:
                self.boxes.remove((new_x, new_y)) # Elimina la caja de su posición actual
                self.boxes.append((new_box_x, new_box_y)) # Añade la caja en su nueva posición
                self.box_moved = True  # Indica que una caja fue movida
            else:
                 # Si la caja no puede moverse, el movimiento del jugador también es inválido
                return False

         # Si no hay obstáculos, mueve al jugador actualizando su posición
        player.move(dx, dy)
        self.player_pos = (player.x, player.y) # Actualiza la posición del jugador en el nivel
        return True # Retorna True indicando que el movimiento fue exitoso

    def is_completed(self):
        # Verifica si todas las cajas están en los objetivos
        return all(box in self.targets for box in self.boxes)

    def draw(self, screen, images):
        # Dibuja el nivel en la pantalla
        screen_width, screen_height = screen.get_size()
        level_width = len(self.layout[0])
        level_height = len(self.layout)
        
        # Calcula el tamaño de los tiles y el offset para centrar el nivel
        tile_size = min(screen_width // (level_width + 2), screen_height // (level_height + 2))
        offset_x = (screen_width - tile_size * level_width) // 2
        offset_y = (screen_height - tile_size * level_height) // 2

        self.level_info = (tile_size, offset_x, offset_y)

        # Dibuja el fondo del nivel
        screen.blit(images['level_background'], (0, 0))

        # Dibuja las paredes y los objetivos
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                pos = (offset_x + x * tile_size, offset_y + y * tile_size)
                if cell == '#':
                    screen.blit(images['stone_wall'], pos)
                elif cell == '.':
                    screen.blit(images['crystal'], pos)
        
        # Dibuja las cajas
        for box in self.boxes:
            screen.blit(images['wooden_box'], (offset_x + box[0] * tile_size, offset_y + box[1] * tile_size))