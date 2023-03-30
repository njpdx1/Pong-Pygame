import pygame
pygame.init()

# CONSTANTS
WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans", 45)
WINNING_SCORE = 3


class Paddle():
    COLOR = (192, 192, 192)
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.x = self.orginal_x = x
        self.y = self.orginal_y = y
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR,
                         (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.orginal_x
        self.y = self.orginal_y


class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.orginal_x = x
        self.y = self.orignal_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.orginal_x
        self.y = self.orignal_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(window, paddles, ball, left_score, right_score):
    window.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    window.blit(left_score_text, (WIDTH//4 -
                left_score_text.get_width()//2, 20))
    window.blit(right_score_text, (WIDTH * (3/4) -
                right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(window)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
    ball.draw(window)
    pygame.display.update()


def collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_y = middle_y - ball.y
                red_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_y / red_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_y = middle_y - ball.y
                red_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_y / red_factor
                ball.y_vel = -1 * y_vel


def paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def main():
    run = True
    won = False
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while (run):
        clock.tick(FPS)
        draw(WINDOW, [left_paddle, right_paddle],
             ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
        
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player is the WINNER!!!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player is the WINNER!!!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.QUIT()


if __name__ == '__main__':
    main()
