import pygame
import random

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")

# Colors (Light Green background)
green = (33, 155, 66)
black = (0, 0, 0)
white = (255, 255, 255)

# Paddle and Ball Properties
paddle_speed = 1  # Reduced paddle speed
ball_speed_x = 1  # Reduced ball speed
ball_speed_y = 1# Reduced ball speed
paddle_width = 10
paddle_height = 80
ball_radius = 10

# Game Objects
player_paddle = pygame.Rect(width - paddle_width - 20, height // 2 - paddle_height // 2, paddle_width, paddle_height)
cpu_paddle = pygame.Rect(20, height // 2 - paddle_height // 2, paddle_width, paddle_height)
ball = pygame.Rect(width // 2 - ball_radius, height // 2 - ball_radius, ball_radius * 2, ball_radius * 2)

# Game State and Score
game_started = False
game_over = False
player_score = 0
cpu_score = 0
winning_score = 5

# Additional variable to store ball color
current_ball_color = white  # Initial color

# Game Loop
running = True
while running:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started and not game_over:
                    game_started = True
                if game_over:
                    # Reset game state
                    game_started = False
                    game_over = False
                    player_score = 0
                    cpu_score = 0
                    ball.x = width // 2 - ball_radius
                    ball.y = height // 2 - ball_radius
                    player_paddle.y = height // 2 - paddle_height // 2
                    cpu_paddle.y = height // 2 - paddle_height // 2
                    ball_speed_x = 0.5  # Reset ball speed
                    ball_speed_y = 0.5  # Reset ball speed
                    # Reset ball color to initial
                    current_ball_color = white

    # Update Game State
    if game_started:
        # Player Controls (W and S keys)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # 'W' key for up
            player_paddle.y -= paddle_speed
        if keys[pygame.K_s]:  # 'S' key for down
            player_paddle.y += paddle_speed

        # CPU Controls
        if ball.y < cpu_paddle.y:
            cpu_paddle.y -= paddle_speed
        if ball.y > cpu_paddle.y:
            cpu_paddle.y += paddle_speed

        # Ball Movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Collisions
        if ball.colliderect(player_paddle) or ball.colliderect(cpu_paddle):
            ball_speed_x *= -1
            # Change ball color on collision
            current_ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        if ball.top <= 0 or ball.bottom >= height:
            ball_speed_y *= -1

        # Scoring
        if ball.left <= 0:
            player_score += 1
            ball.x = width // 2 - ball_radius
            ball.y = height // 2 - ball_radius
            ball_speed_x *= -1
            ball_speed_y *= -1
            game_started = False
        if ball.right >= width:
            cpu_score += 1
            ball.x = width // 2 - ball_radius
            ball.y = height // 2 - ball_radius
            ball_speed_x *= -1
            ball_speed_y *= -1
            game_started = False

        # Check for a winner
        if player_score >= winning_score or cpu_score >= winning_score:
            game_over = True
            game_started = False

    # Drawing
    screen.fill(green)  # Light Blue background
    pygame.draw.rect(screen, white, player_paddle)
    pygame.draw.rect(screen, white, cpu_paddle)
    pygame.draw.circle(screen, current_ball_color, ball.center, ball_radius)  # Use current_ball_color
    pygame.draw.aaline(screen, white, (width // 2, 0), (width // 2, height))  # Center line

    # Score Display
    font = pygame.font.Font(None, 50)  # Default font
    player_text = font.render(f"{player_score}", True, white)
    cpu_text = font.render(f"{cpu_score}", True, white)
    screen.blit(player_text, (width // 2 + 50, 20))
    screen.blit(cpu_text, (width // 2 - 100, 20))

    # Start Screen
    if not game_started and not game_over:
        start_text = font.render("Press SPACE to start", True, white)
        screen.blit(start_text, (width // 2 - 180, height // 2 - 50))

    # End Game Screen
    if game_over:
        if player_score >= winning_score:
            winner_text = font.render("Player Wins!", True, white)
        else:
            winner_text = font.render("CPU Wins!", True, white)
        screen.blit(winner_text, (width // 2 - 150, height // 2 - 50))
        restart_text = font.render("Press SPACE to restart", True, white)
        screen.blit(restart_text, (width // 2 - 180, height // 2 + 20))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
