import pygame, sys, random
from pygame.math import Vector2

pygame.init()

cell_size = 15
number_of_cells = 30

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)
OFFSET = 50

title_font = pygame.font.Font(None, 40)
score_font = pygame.font.Font(None, 20)

pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((cell_size*number_of_cells + OFFSET*2, cell_size*number_of_cells + OFFSET*2))

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.vel = 200

    def draw(self):
        for body in self.body:
            snake_rect = pygame.Rect(body.x * cell_size + OFFSET, body.y * cell_size + OFFSET, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, snake_rect, 0, 3)

    def update(self):
        self.body.pop()
        self.body.insert(0, self.body[0] + self.direction)

food_img = pygame.transform.scale((pygame.image.load("Food/food.png")), (10, 10))
class Food:
    def __init__(self, snake_body):
        self.position = self.generate_pos(snake_body)

    def draw(self):
        apple_rect = pygame.Rect(self.position.x*cell_size + OFFSET, self.position.y*cell_size + OFFSET, cell_size, cell_size)
        screen.blit(food_img, apple_rect)

    def generate_cell(self):
        x = random.randint(1, number_of_cells -1)
        y = random.randint(1, number_of_cells - 1)
        return Vector2(x, y)

    def generate_pos(self, snake_body):
        position = self.generate_cell()
        while position in snake_body:
            self.generate_cell()
        return position

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.eat_sound = pygame.mixer.Sound("Sounds/eat.mp3")
        self.hit_sound = pygame.mixer.Sound("Sounds/wall.mp3")
        self.run = True
        self.score = 0

    def draw(self):
        self.snake.draw()
        self.food.draw()

    def update(self):
        if self.run:
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.snake.body.insert(0, self.snake.body[0] +  self.snake.direction)
            self.food.position = self.food.generate_pos(self.snake.body)
            self.snake.vel -= 10
            self.score += 1
            self.eat_sound.play()

    def check_collision_with_edges(self):
        if self.snake.body[0].x == 0 or self.snake.body[0].x == number_of_cells:
            self.game_over()
        if self.snake.body[0].y == 0 or self.snake.body[0].y == number_of_cells:
            self.game_over()

    def check_collision_with_tail(self):
        headless = self.snake.body[1:]
        if self.snake.body[0] in headless:
            self.game_over()

    def game_over(self):
        self.snake.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.snake.direction = Vector2(1, 0)
        self.food.position = self.food.generate_pos(self.snake.body)
        self.snake.vel = 200
        self.hit_sound.play()
        self.run = False
        self.score = 0

game = Game()
clock = pygame.time.Clock()
FPS = 60


SNAKE_UPDATE = pygame.USEREVENT
while True:
    for event in pygame.event.get():
        pygame.time.set_timer(SNAKE_UPDATE, game.snake.vel)
        if event.type == SNAKE_UPDATE:
            game.update()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.run is False:
                game.run = True
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)

    clock.tick(FPS)
    screen.fill(GREEN)
    pygame.draw.rect(screen, DARK_GREEN, (OFFSET-5, OFFSET-5, cell_size*number_of_cells + 10 , cell_size*number_of_cells + 10), 5)
    game.draw()
    title_surface = title_font.render("Retro Snake", True, DARK_GREEN)
    score_surface = score_font.render(str(game.score), True, DARK_GREEN)
    screen.blit(title_surface, (OFFSET, 10))
    screen.blit(score_surface, (cell_size*number_of_cells + OFFSET, 10))
    pygame.display.update()