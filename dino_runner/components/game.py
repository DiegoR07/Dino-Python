import pygame


from dino_runner.utils.constants import BG, ICON, DEAD, OVER, HEART, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.message import draw_message
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.obstacles.cloud import Cloud


class Game:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        pygame.display.set_icon(DEAD)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.running = False
        self.score = 0
        self.death_count = 0
        

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.playing = True
        self.game_speed = 20
        self.score = 0
        self.power_up_manager.reset_power_ups()

    def run(self):
        # Game loop: events - update - draw
        self.obstacle_manager.reset_obstacles()
        self.playing = True
        self.cloud = Cloud()
        self.reset_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                self.score = 0
                self.death_count = 0

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_score()
        self.draw_power_up_time()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        self.screen.blit(HEART, (half_screen_width - 500, half_screen_height - 280))
        self.screen.blit(HEART, (half_screen_width - 450, half_screen_height - 280))
        self.screen.blit(HEART, (half_screen_width - 400, half_screen_height - 280))
        pygame.display.update()
        pygame.display.flip()
        

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score {self.score}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message(f'Shield enable for {time_to_show} seconds', 
                    self.screen,
                    font_size = 18,
                    pos_x_center = 500,
                    pos_y_center = 50
                )
            else:
                self.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill((80, 188, 154))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))
            draw_message('Press any key to restart', self.screen)
        else:
            self.screen.fill(( 255, 93, 71 ))
            self.screen.blit(HEART, (half_screen_width - 500, half_screen_height - 200))
            self.screen.blit(HEART, (half_screen_width - 450, half_screen_height - 200))
            self.screen.blit(HEART, (half_screen_width - 400, half_screen_height - 200))
            self.screen.blit(OVER, (half_screen_width - 150, half_screen_height - 200))
            self.screen.blit(DEAD, (half_screen_width - 20, half_screen_height - 140))
            draw_message('Press a key again to play the game again', self.screen)
            draw_message(f'Your score: {self.score}', self.screen, pos_y_center = half_screen_height + 50)
            draw_message(f'Death count: {self.death_count}', self.screen, pos_y_center = half_screen_height + 100)


        pygame.display.update()
        self.handle_events_on_menu()
