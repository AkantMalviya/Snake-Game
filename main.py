import random
import pygame

# snake block size
SIZE = 40


class Apple:
    def __init__(self, window):
        self.window = window
        self.apple_img = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.window.blit(self.apple_img, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(1, 29) * SIZE
        self.y = random.randint(1, 14) * SIZE


class Snake:
    def __init__(self, window, length):
        self.window = window
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * self.length
        self.y = [SIZE] * self.length
        self.direction = "down"

    def draw(self):
        for i in range(self.length):
            self.window.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == "up":
            self.y[0] -= SIZE
            self.draw()
        if self.direction == "down":
            self.y[0] += SIZE
            self.draw()
        if self.direction == "left":
            self.x[0] -= SIZE
            self.draw()
        if self.direction == "right":
            self.x[0] += SIZE
            self.draw()

    def increase_block(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.backgroundmusic()
        self.window = pygame.display.set_mode((1300, 660))
        pygame.display.set_caption('Snake Mafia By Akant')
        self.snake = Snake(self.window, 1)
        self.snake.draw()
        self.apple = Apple(self.window)
        self.apple.draw()
        file1 = open("high.txt", "r")
        sc = int(file1.read())
        self.highscore = sc
        file1.close()

    def draw_outsideborders(self):
        pygame.draw.rect(self.window, (0, 0, 0), pygame.Rect(10, 0, 1280, 650), 20)
        pygame.draw.rect(self.window, (255, 0, 0), pygame.Rect(30, 20, 1240, 610), 8)
        pygame.display.update()

    def render_background(self, name):
        bg = pygame.image.load(f"resources/{name}.jpg")
        self.window.blit(bg, [-190, -190])

    def backgroundmusic(self):
        pygame.mixer.music.load("resources/bgmusic.mp3")
        pygame.mixer.music.play()

    def playsound(self, music):
        sound = pygame.mixer.Sound(f"resources/{music}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background("background1")
        self.draw_outsideborders()
        self.snake.walk()
        self.apple.draw()
        self.display_score()

        # Snake collided with apple
        if self.is_collision(self.apple.x, self.apple.y, self.snake.x[0], self.snake.y[0]):
            self.playsound("eatsound2")
            self.snake.increase_block()
            self.apple.move()

        # Snake Collided with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.playsound("gameoversound")
                raise "game over"

        # snake collided with outside borders
        if not (5 <= self.snake.x[0] <= 1200 and 5 <= self.snake.y[0] <= 580):
            raise "Hit outside boundry error"

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont("arial", 30, bold=True)
        score = font.render(f"SCORE : {self.snake.length}", True, (255, 255, 255))
        highscoree = font.render(f"HIGH-SCORE : {self.highscore}", True, (255, 255, 255))
        self.window.blit(score, (50, 40))
        self.window.blit(highscoree, (1050, 40))
        pygame.display.update()

    def show_gameover(self):
        if self.highscore < self.snake.length:
            self.highscore = self.snake.length
            file1 = open("high.txt", "w")
            file1.write(str(self.highscore))
            file1.close()
        self.render_background("background")
        self.draw_outsideborders()
        pygame.mixer.music.pause()
        font = pygame.font.SysFont("arial", 35, bold=True)
        creator = font.render(f"SNAKE MAFIA CREATED BY AKANT", True, (192, 192, 192))
        gameover = font.render(f"GAME  OVER  WITH  SCORE  =  {self.snake.length}", True, (255, 255, 255))
        endline1 = font.render(f"PRESS  ENTER  TO  PLAY  AGAIN", True, (255, 255, 255))
        endline2 = font.render(f"PRESS  ESCAPE  FOR  EXIT", True, (255, 255, 255))
        self.window.blit(creator, (50, 50))
        self.window.blit(gameover, (410, 220))
        self.window.blit(endline1, (410, 270))
        self.window.blit(endline2, (410, 320))
        pygame.display.update()

    def resetgame(self):
        self.snake = Snake(self.window, 1)
        self.apple = Apple(self.window)

    def increase_difficulty(self):

        if 1 <= self.snake.length <= 10:
            return 15
        elif 10 <= self.snake.length <= 20:
            return 25
        elif 20 <= self.snake.length <= 30:
            return 35
        else:
            return 55

    def run(self):
        game_over = False
        pause = False
        clock = pygame.time.Clock()
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == pygame.K_UP:
                            self.snake.move_up()
                        if event.key == pygame.K_DOWN:
                            self.snake.move_down()
                        if event.key == pygame.K_LEFT:
                            self.snake.move_left()
                        if event.key == pygame.K_RIGHT:
                            self.snake.move_right()
                elif event.type == pygame.QUIT:
                    game_over = True
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_gameover()
                pause = True
                self.resetgame()
            clock.tick(self.increase_difficulty())


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    quit()
