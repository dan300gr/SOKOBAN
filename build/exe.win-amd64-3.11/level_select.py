import pygame

class LevelSelect:
    def __init__(self):
        self.levels = [
            {'number': 1, 'name': 'Nivel I', 'sublevels': [
                {'number': 1, 'name': 'Nivel I - 1', 'layout': self.load_level(1)},
                {'number': 2, 'name': 'Nivel I - 2', 'layout': self.load_level(2)},
                {'number': 3, 'name': 'Nivel I - 3', 'layout': self.load_level(3)},
            ]},
            {'number': 2, 'name': 'Nivel II', 'sublevels': [
                {'number': 4, 'name': 'Nivel II - 1', 'layout': self.load_level(4)},
                {'number': 5, 'name': 'Nivel II - 2', 'layout': self.load_level(5)},
                {'number': 6, 'name': 'Nivel II - 3', 'layout': self.load_level(6)},
            ]},
            {'number': 3, 'name': 'Nivel III', 'sublevels': [
                {'number': 7, 'name': 'Nivel III - 1', 'layout': self.load_level(7)},
                {'number': 8, 'name': 'Nivel III - 2', 'layout': self.load_level(8)},
                {'number': 9, 'name': 'Nivel III - 3', 'layout': self.load_level(9)},
            ]},
        ]
        self.completed_levels = set()
        self.selected_level = 0
        self.selected_sublevel = None
        self.current_selection = 0
        self.load_images()

    def load_images(self):
        self.checkmark = pygame.image.load("img_buttons/checkmark.png")
        self.cross = pygame.image.load("img_buttons/cross.png")
        self.checkmark = pygame.transform.scale(self.checkmark, (30, 30))
        self.cross = pygame.transform.scale(self.cross, (30, 30))
        self.back_button = pygame.image.load("img_buttons/back_button.png")
        self.back_button = pygame.transform.scale(self.back_button, (50, 50))
        self.beach_ball = pygame.image.load("img_buttons/beach_ball.png")
        self.beach_ball = pygame.transform.scale(self.beach_ball, (40, 40))

    def load_level(self, level_number):
        levels = {
            # Nivel I
            
            1: [
                "#######",
                "#     #",
                "#     #",
                "#  $  #",
                "#  .  #",
                "#  @  #",
                "#######"
            ],
            
            2: [
                "########",
                "#      #",
                "#  $   #",
                "#     ##",
                "#  @   #",
                "#     ##",
                "#  .   #",
                "########"
            ],
            
            3: [
                "#########",
                "#       #",
                "#   @   #",
                "# $     #",
                "#####  ##",
                "#   #   #",
                "#   .   #",
                "#       #",
                "#########"
            ],
            # Nivel II
            # 1
            4: [
                "########",
                "#   .. #",
                "#  @$$ #",
                "##### ##",
                "#      #",
                "#      #",
                "#      #",
                "########"
            ],
            # 15
            5: [
                "####    ",
                "#  #### ",
                "#     # ",
                "#     # ",
                "### ### ",
                "# $$  ##",
                "# . .@ #",
                "####   #",
                "   #####"
            ],
            # 28
            6: [
                "  #### ",
                "  #  # ",
                "###  # ",
                "#  $$##",
                "# . . #",
                "###  @#",
                "  #####"
            ],
            # Nivel III
            # 150
            7: [
                "#####  ",
                "#.  ###",
                "# # $@#",
                "# . # #",
                "#  .$ #",
                "##$ ###",
                " #  #  ",
                " ####  "
            ],
            # 203
            8: [
                "####  ",
                "#  ###",
                "# $$ #",
                "#... #",
                "# @$ #",
                "#   ##",
                "##### "
            ],
            # 182
            9: [
                " #######",
                " #     #",
                " # .$. #",
                "## $@$ #",
                "#  .$. #",
                "#      #",
                "########"
            ]
        }
        
        if level_number in levels: # Verifica si el nivel solicitado (level_number) está en la colección de niveles predefinidos (levels).
            return [list(row) for row in levels[level_number]] # Si existe, convierte cada fila del nivel en una lista y lo retorna.
        else:
            return self.generate_level(12, 12)

    def generate_level(self, width, height):
        layout = [['#' for _ in range(width)] for _ in range(height)] #cuadricula
        layout[1][1] = '@' #jugador
        layout[height-2][width-2] = '$' #objetivo
        layout[height-2][width-3] = '.' #obejto a arrastrar
        for i in range(2, width-2): # Itera sobre las columnas internas (evitando las paredes de los extremos).
            layout[1][i] = ' ' # Crea un camino vacío en la fila 1 (parte superior).
            layout[height-2][i] = ' '  # Crea un camino vacío en la penúltima fila
        for i in range(2, height-2): # Itera sobre las filas internas
            layout[i][1] = ' ' # Crea un camino vacío en la segunda columna 
            layout[i][width-2] = ' '  # Crea un camino vacío en la penúltima columna
        return layout

    def draw(self, screen, level_blocks, sublevel_buttons):
        if self.selected_sublevel is None:
            self.draw_main_levels(screen, level_blocks)
        else:
            self.draw_sublevels(screen, sublevel_buttons)

    def draw_main_levels(self, screen, level_blocks):
        screen_width, screen_height = screen.get_size()
        start_x = (screen_width - (len(level_blocks) * 200 + (len(level_blocks) - 1) * 20)) // 2
        y_position = 300

        for i, block in enumerate(level_blocks): # Itera sobre los bloques de niveles.
            block_rect = block.get_rect(center=(start_x + i * 220 + 100, y_position))
            screen.blit(block, block_rect)

            completed_levels = sum(1 for sublevel in self.levels[i]['sublevels'] if sublevel['number'] in self.completed_levels)
             # Calcula cuántos subniveles de este nivel han sido completados.
            completed_text = pygame.font.Font(None, 36).render(f"{completed_levels}/3", True, (255, 255, 255))
            completed_rect = completed_text.get_rect(center=(block_rect.centerx, block_rect.bottom + 30))
            screen.blit(completed_text, completed_rect)

            if i == self.current_selection:
                # Ajustamos la posición de la pelotita de playa para cada nivel
                ball_pos = (block_rect.left - -45, block_rect.centery - 20)
                screen.blit(self.beach_ball, ball_pos)

    def draw_sublevels(self, screen, sublevel_buttons):
        screen_width, screen_height = screen.get_size()
        level = self.levels[self.selected_sublevel]
        
        for i, sublevel in enumerate(level['sublevels']):
            button = sublevel_buttons[self.selected_sublevel][i]
            button_rect = button.get_rect(center=(screen_width // 2, 200 + i * 120))
            screen.blit(button, button_rect)

            if sublevel['number'] in self.completed_levels:
                screen.blit(self.checkmark, (button_rect.right + 10, button_rect.centery - 15))
            else:
                screen.blit(self.cross, (button_rect.right + 10, button_rect.centery - 15))

            if i == self.current_selection:
                ball_pos = (button_rect.left - 50, button_rect.centery - 20)
                screen.blit(self.beach_ball, ball_pos)

        back_button_rect = self.back_button.get_rect(topleft=(20, 20))
        screen.blit(self.back_button, back_button_rect)

    def handle_click(self, pos):
        if self.selected_sublevel is None:
            return self.handle_main_level_click(pos)
        else:
            return self.handle_sublevel_click(pos)

    def handle_main_level_click(self, pos):
        screen_width, _ = pygame.display.get_surface().get_size()
        start_x = (screen_width - (3 * 200 + 2 * 20)) // 2
        y_position = 300

        for i in range(3):
            block_rect = pygame.Rect(start_x + i * 220, y_position - 100, 200, 200)
            if block_rect.collidepoint(pos):
                self.selected_sublevel = i
                self.current_selection = 0
                return None
        return None

    def handle_sublevel_click(self, pos):
        screen_width, _ = pygame.display.get_surface().get_size()
        for i, sublevel in enumerate(self.levels[self.selected_sublevel]['sublevels']):
            button_rect = pygame.Rect(screen_width // 2 - 100, 200 + i * 120 - 50, 200, 100)
            if button_rect.collidepoint(pos):
                self.selected_level = sublevel['number'] - 1
                return sublevel

        back_button_rect = pygame.Rect(20, 20, 50, 50)
        if back_button_rect.collidepoint(pos):
            self.selected_sublevel = None
            self.current_selection = 0
            return None

        return None

    def mark_level_completed(self, level_number):
        self.completed_levels.add(level_number)

    def get_next_level(self):
        next_level_index = self.selected_level + 1
        if next_level_index < sum(len(level['sublevels']) for level in self.levels):
            self.selected_level = next_level_index
            for level in self.levels:
                for sublevel in level['sublevels']:
                    if sublevel['number'] == next_level_index + 1:
                        return sublevel
        return None

    def get_selected_level(self):
        for level in self.levels:
            for sublevel in level['sublevels']:
                if sublevel['number'] == self.selected_level + 1:
                    return sublevel
        return None

    def move_selection(self, direction):
        if self.selected_sublevel is None:
            self.current_selection = (self.current_selection + direction) % 3
        else:
            self.current_selection = (self.current_selection + direction) % 3

    def select_current(self):
        if self.selected_sublevel is None:
            self.selected_sublevel = self.current_selection
            self.current_selection = 0
        else:
            self.selected_level = self.levels[self.selected_sublevel]['sublevels'][self.current_selection]['number'] - 1
            return self.levels[self.selected_sublevel]['sublevels'][self.current_selection]

    def reset_sublevel_selection(self):
        self.selected_sublevel = None
        self.current_selection = 0