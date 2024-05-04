import sys
import random
import pygame
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False
        self.min_length = 3

        self.head_up = pygame.image.load('Visual/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Visual/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Visual/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Visual/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Visual/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Visual/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Visual/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Visual/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Visual/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Visual/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Visual/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Visual/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Visual/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Visual/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sounds/eating.wav')
        self.bg_music = pygame.mixer.Sound('Sounds/background.wav')


    def half_length(self):
        new_length = max(self.min_length, len(self.body) * 3//4)
        self.body = self.body[:new_length]

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down


    def move_snake(self):
        if self.new_block ==True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False

        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_eating_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction= Vector2(0,0)

    def play_music(self):
        self.bg_music.play(loops=-1)

class FRUIT:
    def __init__(self):
        self.common_types = [self.draw_fries, self.draw_burgir, self.draw_soda]  # List of methods to draw each item
        self.rare_type = self.draw_broc
        self.count = 0
        self.rare_threshold = random.randint(8, 12)
        self.randomize()

    def randomize(self):
        self.x = random.randint(1, cell_number_width - 2)
        self.y = random.randint(1, cell_number_height - 2)
        self.pos = Vector2(self.x, self.y)

        if self.count >= self.rare_threshold:
            self.current_type = self.rare_type
            self.count = 0  # Reset count
            self.rare_threshold = random.randint(10, 15)  # Reset threshold
        else:
            self.current_type = random.choice(self.common_types)
            self.count += 1




    def draw_fries(self):  # Moved back to be a method of the class
        fries_rect = pygame.Rect(int (self.pos.x * cell_size), int (self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(fries, fries_rect)

    def draw_burgir(self):  # Moved back to be a method of the class
        burgir_rect = pygame.Rect(int (self.pos.x * cell_size), int (self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(burgir, burgir_rect)

    def draw_soda(self):  # Moved back to be a method of the class
        soda_rect = pygame.Rect(int (self.pos.x * cell_size), int (self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(soda, soda_rect)

    def draw_broc(self):
        broc_rect = pygame.Rect(int (self.pos.x * cell_size), int (self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(broc, broc_rect)

    def draw(self):
        self.current_type()


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.snake.play_music()
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_soil()
        self.fruit.draw()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.play_eating_sound()
            # creste sarpiliii
            if self.fruit.current_type == self.fruit.draw_broc:
                self.snake.half_length()
                self.snake.add_block()
                self.score += 10
                self.fruit.randomize()

            else:
                self.snake.add_block()
                self.score += 10
                self.fruit.randomize()


        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()



    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number_width or not 0 <= self.snake.body[0].y < cell_number_height:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        self.score = 0

    def draw_soil(self):
        soil_color1 = (119, 85, 24)


        for row in range(cell_number_height):
            if row % 2 == 0:
                for col in range(cell_number_width):
                    if col % 2 == 0:
                        soil_rect = pygame.Rect(col * cell_size,row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen,soil_color1,soil_rect)

            else:
                for col in range(cell_number_width):
                    if col % 2 != 0:
                        soil_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, soil_color1, soil_rect)

    def draw_score(self):
        score_text = str(self.score)
        score_surface = game_font.render(score_text,True ,(0, 255, 13))
        score_x =int(cell_size * cell_number_width - 80)
        score_y = int (cell_size*cell_number_height - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y ))
        bg_rect = pygame.Rect(score_rect.left -2, score_rect.top - 2, score_rect.width + 4 , score_rect.height )

        pygame.draw.rect(screen, (166, 124, 51), bg_rect)
        screen.blit(score_surface, score_rect)
        pygame.draw.rect(screen, (0, 255, 13), bg_rect, 2)



pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number_width = 30
cell_number_height = 22
screen = pygame.display.set_mode((cell_number_width * cell_size , cell_number_height * cell_size))
clock = pygame.time.Clock()
fries = pygame.image.load('Visual/fries.png').convert_alpha()
burgir = pygame.image.load('Visual/burgir.png').convert_alpha()
broc = pygame.image.load('Visual/broccoli.png').convert_alpha()
soda = pygame.image.load('Visual/soda.png').convert_alpha()
game_font = pygame.font.Font('Dino_Care.ttf',28)


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,120)

main_game = MAIN()



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
           main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y!=1:
                    main_game.snake.direction = Vector2(0,-1)

            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x!= -1:
                    main_game.snake.direction = Vector2(1, 0)

            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)

            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)


    screen.fill((166, 124, 51))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(180)



