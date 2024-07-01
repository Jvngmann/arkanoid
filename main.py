# Section #1. Initial setup
import pygame
import random

pygame.init()

W, H = 800, 600
FPS = 60

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
done = False
bg = (255, 192, 43)

# Section #2. Adding objects for the ball and paddle
paddleW = 200
paddleH = 25
paddleSpeed = 20
paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)

# Ball
ballRadius = 20
initial_ball_speed = 6
ballSpeed = initial_ball_speed
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

unbreakable_brick_color = (100, 100, 100)
bonus_brick_color = (0, 0, 255)
unbreakable_probability = 0.15  
bonus_probability = 0.05  

# Adding bricks with some unbreakable and bonus bricks
for row in range(brick_rows):
    brick_row = []
    for col in range(brick_cols):
        brick_x = col * (brick_width + brick_padding) + brick_padding
        brick_y = row * (brick_height + brick_padding) + 50
        brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        
        if random.random() < bonus_probability:
            brick_color = bonus_brick_color
            breakable = True
            bonus = 'double_paddle'  # Bonus flag for doubling the paddle width
        else:
            is_unbreakable = random.random() < unbreakable_probability
            brick_color = unbreakable_brick_color if is_unbreakable else [random.randint(0, 255) for _ in range(3)]
            breakable = not is_unbreakable
            bonus = None
        
        brick_row.append((brick, brick_color, breakable, bonus))
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

# Increase ball speed and shrink paddle over time
speed_increase_interval = 5000  # milliseconds
paddle_shrink_interval = 10000  # milliseconds
last_speed_increase_time = pygame.time.get_ticks()
last_paddle_shrink_time = pygame.time.get_ticks()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(bg)

    # Draw paddle
    pygame.draw.rect(screen, pygame.Color(250, 250, 250), paddle)
    # Draw ball
    pygame.draw.circle(screen, pygame.Color(30, 30, 30), ball.center, ballRadius)
    
    # Draw bricks
    for brick_row in bricks:
        for brick, color, breakable, bonus in brick_row:
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
    # Collision top
    if ball.centery < ballRadius + 50:
        dy = -dy
    # Collision with paddle
    if ball.colliderect(paddle) and dy > 0:
        dy = -dy
    # Collision with bricks
    for brick_row in bricks:
        for brick, color, breakable, bonus in brick_row:
            if ball.colliderect(brick):
                if breakable:
                    brick_row.remove((brick, color, breakable, bonus))
                    if bonus == 'double_paddle':
                        paddle.width = min(paddle.width * 2, W)  # Double the paddle width
                        paddle.left = max(paddle.left - (paddle.width // 4), 0)  # Adjust position
                dy = -dy
                break

    # Check if all breakable bricks are broken (win)
    if all(not brick_row or all(not breakable for _, _, breakable, _ in brick_row) for brick_row in bricks):
        screen.fill((0, 0, 0))
        screen.blit(win_text, win_textRect)

    # Check if the ball is out of the screen (game over)
    if ball.y > H:
        screen.fill((0, 0, 0))
        screen.blit(text, textRect)

    # Increase ball speed over time
    current_time = pygame.time.get_ticks()
    if current_time - last_speed_increase_time >= speed_increase_interval:
        ballSpeed += 1  # Increase the ball speed
        last_speed_increase_time = current_time

    # Shrink paddle over time
    if current_time - last_paddle_shrink_time >= paddle_shrink_interval:
        if paddle.width > 40:  # Ensure paddle doesn't become too small
            paddle.width -= 20  # Shrink the paddle
            paddle.left += 10  # Adjust position to keep it centered
            last_paddle_shrink_time = current_time

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
