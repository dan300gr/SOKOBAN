import pygame
import os
import time
from level_select import LevelSelect
from level import Level
from player import Player
from solver import Solver
import cv2

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Sokoban - UVP")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'  # 'start', 'level_select', 'playing', 'game_completed'
        
        self.level_select = LevelSelect()
        self.current_level = None
        self.player = None
        
        self.steps = 0
        self.moves_history = []
        
        self.play_button_hovered = False
        
        self.load_sounds()
        self.sound_enabled = True
        
        self.load_fonts()
        self.load_images()
        self.load_button_images()
        self.load_celebration_images()
        self.load_sublevel_buttons()
        self.load_celebration_video()

        self.solver = Solver()
        self.solution = None
        self.solution_index = 0
        self.solution_delay = 0.5
        self.last_solution_move_time = 0

    def load_sounds(self):
        self.background_music = pygame.mixer.Sound("sounds/background.mp3")
        self.move_sound = pygame.mixer.Sound("sounds/move.mp3")
        self.box_sound = pygame.mixer.Sound("sounds/box.mp3")
        self.victory_sound = pygame.mixer.Sound("sounds/victory.mp3")
        self.celebration_sound = pygame.mixer.Sound("sounds/victory.mp3")
        self.background_music.play(-1)

    def load_fonts(self):
        pygame.font.init()
        try:
            self.font = pygame.font.Font("minecraft.ttf", 36)
        except FileNotFoundError:
            print("Minecraft font not found. Using system default font.")
            self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)

    def load_images(self):
        screen_width, screen_height = self.screen.get_size()
        
        tile_size = min(screen_width // 10, screen_height // 10)

        self.images = {
            'wooden_box': self.load_and_scale("img_box/wooden_box.png", tile_size),
            'crystal': self.load_and_scale("img_levels/crystal.png", tile_size),
            'stone_wall': self.load_and_scale("img_levels/stone_wall.png", tile_size),
            'background': pygame.transform.scale(pygame.image.load("img_inicio/inicio.png"), (screen_width, screen_height)),
            'level_select_background': pygame.transform.scale(pygame.image.load("img_inicio/niveles.png"), (screen_width, screen_height)),
            'sublevel_select_background': pygame.transform.scale(pygame.image.load("img_inicio/subniveles.png"), (screen_width, screen_height)),
            'level_background': pygame.transform.scale(pygame.image.load("img_levels/level_background.png"), (screen_width, screen_height)),
        }

        self.level_blocks = []
        for i in range(3):
            block = pygame.image.load(f"img_inicio/level_blocks_{i+1}.png")
            block = pygame.transform.scale(block, (350, 250))
            self.level_blocks.append(block)

    def load_and_scale(self, image_path, size):
        image = pygame.image.load(image_path)
        return pygame.transform.smoothscale(image, (size, size))

    def load_button_images(self):
        screen_width, _ = self.screen.get_size()
        self.play_button = pygame.transform.scale(pygame.image.load("img_inicio/play_button.png"), (240, 140))
        self.play_button_hover = pygame.transform.scale(pygame.image.load("img_inicio/play_button_hover.png"), (240, 140))
        self.play_button_rect = self.play_button.get_rect(center=(screen_width // 2, 350))

        button_size = (50, 50)
        self.restart_button = pygame.transform.scale(pygame.image.load("img_buttons/restart.png"), button_size)
        self.undo_button = pygame.transform.scale(pygame.image.load("img_buttons/undo.png"), button_size)
        self.sound_button = pygame.transform.scale(pygame.image.load("img_buttons/sound_on.png"), button_size)
        self.sound_off_button = pygame.transform.scale(pygame.image.load("img_buttons/sound_off.png"), button_size)
        self.menu_button = pygame.transform.scale(pygame.image.load("img_buttons/menu.png"), button_size)
        self.solve_button = pygame.transform.scale(pygame.image.load("img_buttons/solve.png"), button_size)

    def load_celebration_images(self):
        self.celebration_images = []
        for i in range(10):
            image = pygame.image.load(f"img_celebration/celebrate_{i+1}.png")
            image = pygame.transform.scale(image, (100, 100))
            self.celebration_images.append(image)

    def load_sublevel_buttons(self):
        self.sublevel_buttons = []
        for i in range(1, 4):
            level_buttons = []
            for j in range(1, 4):
                button = pygame.image.load(f"img_buttons/sublevel_{i}_{j}.png")
                button = pygame.transform.scale(button, (200, 100))
                level_buttons.append(button)
            self.sublevel_buttons.append(level_buttons)

    def load_celebration_video(self):
        self.celebration_video = cv2.VideoCapture("playita.mp4")
        self.celebration_video_frames = []
        screen_width, screen_height = self.screen.get_size()
        while True:
            ret, frame = self.celebration_video.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (screen_width, screen_height))
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.celebration_video_frames.append(frame)
        self.celebration_video.release()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_press(event.key)

    def handle_mouse_click(self, pos):
        if self.state == 'start':
            if self.play_button_rect.collidepoint(pos):
                self.state = 'level_select'
        elif self.state == 'level_select':
            level = self.level_select.handle_click(pos)
            if level:
                self.start_level(level)
        elif self.state == 'playing':
            if self.menu_rect.collidepoint(pos):
                self.state = 'level_select'
                self.level_select.reset_sublevel_selection()
            elif self.restart_rect.collidepoint(pos):
                self.restart_level()
            elif self.undo_rect.collidepoint(pos):
                self.undo_move()
            elif self.sound_rect.collidepoint(pos):
                self.toggle_sound()
            elif self.solve_rect.collidepoint(pos):
                self.solve_level()

    def handle_mouse_motion(self, pos):
        if self.state == 'start':
            self.play_button_hovered = self.play_button_rect.collidepoint(pos)

    def handle_key_press(self, key):
        if self.state == 'playing':
            if key == pygame.K_LEFT:
                self.move_player(-1, 0)
            elif key == pygame.K_RIGHT:
                self.move_player(1, 0)
            elif key == pygame.K_UP:
                self.move_player(0, -1)
            elif key == pygame.K_DOWN:
                self.move_player(0, 1)
            elif key == pygame.K_r:
                self.restart_level()
            elif key == pygame.K_ESCAPE:
                self.state = 'level_select'
                self.level_select.reset_sublevel_selection()
        elif self.state == 'level_select':
            if key == pygame.K_ESCAPE:
                if self.level_select.selected_sublevel is not None:
                    self.level_select.reset_sublevel_selection()
                else:
                    self.state = 'start'
            elif key == pygame.K_LEFT:
                self.level_select.move_selection(-1)
            elif key == pygame.K_RIGHT:
                self.level_select.move_selection(1)
            elif key == pygame.K_RETURN:
                level = self.level_select.select_current()
                if level:
                    self.start_level(level)

    def move_player(self, dx, dy):
        if self.current_level.move_player(self.player, dx, dy):
            self.steps += 1
            self.moves_history.append((dx, dy))
            if self.sound_enabled:
                self.move_sound.play()
                if self.current_level.box_moved:
                    self.box_sound.play()

    def undo_move(self):
        if self.moves_history:
            last_move = self.moves_history.pop()
            dx, dy = last_move

            current_player_pos = (self.player.x, self.player.y)
            previous_player_pos = (self.player.x - dx, self.player.y - dy)

            potential_box_pos = (self.player.x + dx, self.player.y + dy)
            if potential_box_pos in self.current_level.boxes:
                self.current_level.boxes.remove(potential_box_pos)
                self.current_level.boxes.append(current_player_pos)

            self.player.move(-dx, -dy)
            self.current_level.player_pos = previous_player_pos

            self.steps -= 1

    def update(self):
        if self.state == 'playing':
            if self.current_level.is_completed():
                self.play_victory_sound()
                self.level_select.mark_level_completed(self.current_level.level_number)
                self.celebrate()
                next_level = self.level_select.get_next_level()
                if next_level:
                    self.start_level(next_level)
                else:
                    self.state = 'game_completed'
            elif self.solution and self.solution_index < len(self.solution):
                current_time = time.time()
                if current_time - self.last_solution_move_time >= self.solution_delay:
                    self.move_player(*self.solution[self.solution_index])
                    self.solution_index += 1
                    self.last_solution_move_time = current_time

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.state == 'start':
            self.draw_start_screen()
        elif self.state == 'level_select':
            self.draw_level_select()
        elif self.state == 'playing':
            self.current_level.draw(self.screen, self.images)
            if self.current_level.level_info:
                self.player.draw(self.screen, self.current_level.level_info)
            self.draw_game_ui()
        elif self.state == 'game_completed':
            self.draw_game_completed()
        pygame.display.flip()

    def draw_start_screen(self):
        self.screen.blit(self.images['background'], (0, 0))
        if self.play_button_hovered:
            self.screen.blit(self.play_button_hover, self.play_button_rect)
        else:
            self.screen.blit(self.play_button, self.play_button_rect)

    def draw_level_select(self):
        if self.level_select.selected_sublevel is None:
            self.screen.blit(self.images['level_select_background'], (0, 0))
        else:
            self.screen.blit(self.images['sublevel_select_background'], (0, 0))
        self.level_select.draw(self.screen, self.level_blocks, self.sublevel_buttons)

    def draw_game_ui(self):
        level_text = self.font.render(f"Nivel: {self.current_level.level_number}", True, (255, 255, 255))
        self.screen.blit(level_text, (20, 20))
        
        steps_text = self.font.render(f"Pasos: {self.steps}", True, (255, 255, 255))
        self.screen.blit(steps_text, (20, 60))

        screen_width, screen_height = self.screen.get_size()
        button_y = screen_height - 60
        
        self.menu_rect = self.screen.blit(self.menu_button, (screen_width - 300, button_y))
        self.restart_rect = self.screen.blit(self.restart_button, (screen_width - 240, button_y))
        self.undo_rect = self.screen.blit(self.undo_button, (screen_width - 180, button_y))
        self.solve_rect = self.screen.blit(self.solve_button, (screen_width - 120, button_y))
        
        if self.sound_enabled:
            self.sound_rect = self.screen.blit(self.sound_button, (screen_width - 60, button_y))
        else:
            self.sound_rect = self.screen.blit(self.sound_off_button, (screen_width - 60, button_y))

    def start_level(self, level_data):
        self.current_level = Level(level_data)
        self.player = Player(self.current_level.player_start)
        self.state = 'playing'
        self.steps = 0
        self.moves_history = []
        self.solution = None
        self.solution_index = 0

    def restart_level(self):
        self.start_level(self.current_level.level_data)

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.background_music.play(-1)
        else:
            self.background_music.stop()

    def solve_level(self):
        self.solution = self.solver.solve(self.current_level)
        self.solution_index = 0
        self.last_solution_move_time = time.time()
        if not self.solution:
            print("No se pudo encontrar una solución.")

    def play_victory_sound(self):
        if self.sound_enabled and self.victory_sound:
            try:
                self.victory_sound.play()
            except pygame.error:
                print("Error al reproducir el sonido de victoria")

    def celebrate(self):
        celebration_duration = 3  # seconds
        frames_per_second = 30
        total_frames = celebration_duration * frames_per_second

        start_time = pygame.time.get_ticks()
        if self.sound_enabled:
            self.celebration_sound.play()

        for frame in range(total_frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.blit(self.images['level_background'], (0, 0))
            
            self.current_level.draw(self.screen, self.images)
            
            video_frame_index = frame % len(self.celebration_video_frames)
            video_frame = self.celebration_video_frames[video_frame_index]
            
            self.screen.blit(video_frame, (0, 0))

            pygame.display.flip()
            self.clock.tick(frames_per_second)

        if self.sound_enabled:
            self.celebration_sound.stop()

    def draw_game_completed(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("¡Felicidades! Has completado todos los niveles", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)

if __name__ == "__main__":
    game = Game()
    game.run()