from typing import Sized
import pygame
import time
from pygame.locals import *
import random

SIZE = 20
BACKGROUND = (45, 34, 44)
W = 800
H = 400
SCREEN = (W, H)


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.snake = pygame.image.load(
            "resources/snake.png").convert()  # inserting snake image

        self.snake_x = [W//2]*length  # list with 'length' number of elements
        self.snake_y = [H//2]*length

        self.direction = "left"  # default direction LEFT

    def increase_length(self):
        self.length += 1

        # adds another block to snake
        # appends a random value to the list...cause it will change immidiately in 'move()' method
        self.snake_x.append(0)
        self.snake_y.append(0)

    def draw(self):
        # self.parent_screen.fill(BACKGROUND)
        for i in range(self.length):
            self.parent_screen.blit(
                self.snake, (self.snake_x[i], self.snake_y[i]))  # drawing snake
        pygame.display.flip()

    def move(self):
        # Logic gor moving the TAIL snakes [like 2nd snake will come to 1st pos, 3rd will move to 2nd pos.]

        for i in range(self.length-1, 0, -1):  # reverse for loop
            self.snake_x[i] = self.snake_x[i-1]
            self.snake_y[i] = self.snake_y[i-1]

        # Logic for moving the head snakes

        if self.direction == 'up':
            self.snake_y[0] -= SIZE
        if self.direction == 'down':
            self.snake_y[0] += SIZE
        if self.direction == 'right':
            self.snake_x[0] += SIZE
        if self.direction == 'left':
            self.snake_x[0] -= SIZE

        self.draw()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'

# Apple class


class Food:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.food1 = pygame.image.load(
            "resources/food.png").convert()  # inserting food image
        self.food2 = pygame.image.load(
            "resources/snake1.png").convert() 

        self.food_x = SIZE*3
        self.food_y = SIZE*2

    def draw(self):
        seq = [self.food1, self.food2]
        self.parent_screen.blit(random.choice(seq), (self.food_x, self.food_y))  # drawing snake
        pygame.display.flip()

    def move(self):
        self.food_x = random.randint(0, W//SIZE - 1) * SIZE
        self.food_y = random.randint(0, H//SIZE - 1) * SIZE


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        self.surface = pygame.display.set_mode(
            SCREEN)  # crating game window 1000x720
        self.surface.fill(BACKGROUND)  # rgb color combination

        # snake object (surface, size_of_snake)
        self.snake = Snake(self.surface, 3)
        self.snake.draw()

        self.food = Food(self.surface)  # Food object(Surface)
        self.food.draw()

        pygame.mixer.init()  # pygame class mixer...for sound

        # start playing background b_music
        self.background_music()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        else:
            return False

    def play_sound(self, sound_location):
        sound = pygame.mixer.Sound(sound_location)  # sound is for short time
        pygame.mixer.Sound.play(sound)

    def background_music(self):
        pygame.mixer.music.load("resources/b_music1.mp3")
        pygame.mixer.music.play(-1) #plays music infinitely

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):

        self.render_background()  # render the background
        self.snake.move()
        self.food.draw()
        self.display_score()
        self.screen_msgs()
        pygame.display.flip()

        # Snake colloding with apple
        if self.is_collision(self.snake.snake_x[0], self.snake.snake_y[0], self.food.food_x, self.food.food_y):
            self.food.move()  # moves apple to random position
            self.snake.increase_length()
            # play sound when eating the food
            self.play_sound("resources/ding.mp3")  # passing the music location
            # to play the sound

        # Snake colliding with itself Game Over logic
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.snake_x[0], self.snake.snake_y[0], self.snake.snake_x[i], self.snake.snake_y[i]):
                # play sound when game Over
                self.play_sound("resources/fail_buzz.mp3")

                raise "Game Over"  # raising exeption
        
        self.touch_border_action()
    
    def pause_msg(self):
        font = pygame.font.SysFont('arial', 20)
        font1 = pygame.font.SysFont('Rockwell', 80)
        line1 = font1.render(
            f"<Paused>", True, (200, 200, 200))
        line2 = font.render(
            f"Press <UP, DOWN, LEFT, RIGHT> To Resume", True, (255,255, 0))
        self.surface.blit(line1, (W//4 + 20, H//3))
        self.surface.blit(line2, (W//4 + 30, H//3 + 100))

        pygame.display.flip()

    def show_game_over(self):
        # self.surface.fill(BACKGROUND)
        self.render_background()

        font = pygame.font.SysFont('Cooper Black', 30)
        font1 = pygame.font.SysFont('Cooper Black', 60)
        line1 = font1.render(
            f"GAME OVER !!", True, (200, 0, 0))
        line1B = font.render(
            f"<<Score : {self.snake.length - 3}>>", True, (10, 255, 10))

        line2 = font.render(
            f"Press <UP, DOWN, LEFT, RIGHT> To Play Again", True, (200, 200, 200))
        line3 = font.render(
            f"Press ESC to EXIT!", True, (255, 200, 0))

        self.surface.blit(line1, (W//4 - 25, H//3-45))
        self.surface.blit(line1B, (W//4 + 100, H//3 + 60))
        self.surface.blit(line2, (45, H//3 + 110))
        self.surface.blit(line3, (W//4+50, H//3 + 160))

        pygame.display.flip()
        # pause the background_music when game over
        pygame.mixer.music.rewind()
        pygame.mixer.music.pause()
    
    def touch_border_action(self):
        if self.snake.snake_x[0] == W:
            self.snake.snake_x[0] = 0
        elif self.snake.snake_x[0] < 0:
            self.snake.snake_x[0] = W 
        
        if self.snake.snake_y[0] == H:
            self.snake.snake_y[0] = 0
        elif self.snake.snake_y[0] < 0:
            self.snake.snake_y[0] = H

    def reset_game(self):
        self.snake = Snake(self.surface, 3)

        self.food = Food(self.surface)  # Food object(Surface)

    def display_score(self):
        font = pygame.font.SysFont('Algerian', 30)
        score = font.render(
            f"[Score : {self.snake.length - 3}]", True, (0, 255, 255))
        self.surface.blit(score, (W //2 - 70 , 5))

    def screen_msgs(self):
        font = pygame.font.SysFont('aharoni',16)
        msgs1 = font.render("[SPACE] to Pause", True, (200, 204, 255))
        msgs2 = font.render("[ESC] to EXIT", True, (200, 204, 255))
        self.surface.blit(msgs1, (W - 100, H - 20))
        self.surface.blit(msgs2, (10, H - 20))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        pause_game = False
        while running:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # PRESS esc to escape the screen
                        running = False
                    if event.key == K_SPACE:  # to pause the game
                        pygame.mixer.music.pause()
                        self.pause_msg()
                        pause_game = True

                    if event.key == K_UP:
                        self.snake.move_up()
                        pause_game = False
                        pygame.mixer.music.unpause()

                    if event.key == K_DOWN:
                        self.snake.move_down()
                        pause_game = False
                        pygame.mixer.music.unpause()

                    if event.key == K_LEFT:
                        self.snake.move_left()
                        pause_game = False
                        pygame.mixer.music.unpause()

                    if event.key == K_RIGHT:
                        self.snake.move_right()
                        pause_game = False
                        pygame.mixer.music.unpause()

                elif event.type == QUIT:
                    running = False

            if not pause_game:
                try:
                    self.play()
                except Exception as e:
                    self.show_game_over()
                    pause_game = True
                    self.reset_game()

            clock.tick(60)


if __name__ == "__main__":

    game = Game()  # Game class object
    game.run()

    # auto-py-to-exe.exe # run this commande to  convert to exe
