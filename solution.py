import pygame
pygame.init()

#CONSTANTS
WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

PADDLE_HEIGHT, PADDLE_WIDTH = 20, 100 

class Paddle():
    COLOR = WHITE
    def __init__ (self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rectangle(window, self.COLOR(self.x, self.y, self.width, self.height))

def draw(win):
    win.fill(BLACK)
    pygame.display.update()



def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT//2 -PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH -  10, PADDLE_WIDTH, HEIGHT//2 -PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    while (run):
        clock.tick(FPS)
        draw(WINDOW)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.QUIT()


if __name__ == '__main__':
    main()
