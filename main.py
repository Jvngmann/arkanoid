# Section #1. Initial set up
import pygame
import random

pygame.init()

W, H = 800, 600
FPS = 60

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
done = False
bg = (255, 192, 203)

# Section #2. Adding objects of a ball and a paddle
paddleW = 200
paddleH = 25
paddleSpeed = 20
paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)

# Ball
ballRadius = 20
ballSpeed = 6
ball_rect = int(ballRadius * 2 ** 0.5)
ball = pygame.Rect(random.randrange(ball_rect, W - ball_rect), H // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Bricks
brick_rows = 3
brick_cols = 10
brick_padding = 10
brick_width = (W - (brick_cols + 1) * brick_padding) // brick_cols
brick_height = 30
bricks = []

for row in range(brick_rows):
    brick_row = []
    for col in range(brick_cols):
        brick_x = col * (brick_width + brick_padding) + brick_padding
        brick_y = row * (brick_height + brick_padding) + 50
        brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        brick_color = [random.randint(0, 255) for _ in range(3)]
        brick_row.append((brick, brick_color))
    bricks.append(brick_row)

# Game over
font = pygame.font.SysFont('comicsansms', 40)
text = font.render('Game Over', True, (255, 255, 255))
textRect = text.get_rect()
textRect.center = (W // 2, H // 2)

# Winning
win_text = font.render('You Win!', True, (255, 255, 255))
win_textRect = win_text.get_rect()
win_textRect.center = (W // 2, H // 2)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(bg)

    # Draw paddle
    pygame.draw.rect(screen, pygame.Color(234, 250, 177), paddle)
    # Draw ball
    pygame.draw.circle(screen, pygame.Color(250, 241, 157), ball.center, ballRadius)
    
    # Draw bricks
    for brick_row in bricks:
        for brick, color in brick_row:
            pygame.draw.rect(screen, color, brick)
    
    # Paddle Control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddleSpeed
    if key[pygame.K_RIGHT] and paddle.right < W:
        paddle.right += paddleSpeed

    # Ball movement
    ball.x += ballSpeed * dx
    ball.y += ballSpeed * dy

    # Collision left or right
    if ball.centerx < ballRadius or ball.centerx > W - ballRadius:
        dx = -dx
    # Collision TOP
    if ball.centery < ballRadius + 50:
        dy = -dy
    # Collision with paddle
    if ball.colliderect(paddle) and dy > 0:
        dy = -dy
    # Collision with bricks
    for brick_row in bricks:
        for brick, color in brick_row:
            if ball.colliderect(brick):
                brick_row.remove((brick, color))
                dy = -dy
                break

    # Check if all bricks are broken (win)
    if all(not brick_row for brick_row in bricks):
        screen.fill((0, 0, 0))
        screen.blit(win_text, win_textRect)

    # Check if the ball is out of the screen (game over)
    if ball.y > H:
        screen.fill((0, 0, 0))
        screen.blit(text, textRect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
