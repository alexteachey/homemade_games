import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with SuperHot Mechanics, AI Opponent, and Spin")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle class
class Paddle:
    def __init__(self, x):
        self.width = 15
        self.height = 100
        self.x = x
        self.y = HEIGHT // 2 - self.height // 2
        self.speed = 5
        self.score = 0

    def move(self, dy):
        self.y += dy
        # Ensure paddle stays on the screen
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

# Ball class
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = 3 * random.choice([-1, 1])
        self.dy = 3 * random.choice([-1, 1])
        self.spin_factor = 1  # Adjust this to control spin intensity

    def move(self, factor):
        # Move the ball based on the player's movement factor
        self.x += self.dx * factor
        self.y += self.dy * factor
        # Bounce off top and bottom walls
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.dy *= -1

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

    def reset_position(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = 3 * random.choice([-1, 1])
        self.dy = 3 * random.choice([-1, 1])

    def apply_spin(self, paddle):
        # Calculate the difference between the center of the paddle and the impact point
        paddle_center = paddle.y + paddle.height // 2
        impact_distance = self.y - paddle_center

        # Normalize impact distance to be between -1 and 1
        max_distance = paddle.height // 2
        normalized_impact = impact_distance / max_distance

        # Apply spin to the ball's vertical speed (dy)
        self.dy += normalized_impact * self.spin_factor

# AI paddle movement
def ai_move(ai_paddle, ball):
    if ai_paddle.y + ai_paddle.height / 2 < ball.y:
        ai_paddle.move(ai_paddle.speed)
    elif ai_paddle.y + ai_paddle.height / 2 > ball.y:
        ai_paddle.move(-ai_paddle.speed)

# Draw score on screen
def draw_score(paddle, ai_paddle):
    font = pygame.font.Font(None, 36)
    player_text = font.render(f"Player: {paddle.score}", True, WHITE)
    ai_text = font.render(f"AI: {ai_paddle.score}", True, WHITE)
    screen.blit(player_text, (50, 20))
    screen.blit(ai_text, (WIDTH - 150, 20))

# Game loop
def main():
    clock = pygame.time.Clock()

    # Create player, AI paddles and the ball
    player_paddle = Paddle(x=50)
    ai_paddle = Paddle(x=WIDTH - 65)
    ball = Ball()

    running = True
    ball_moving = False  # Ball will only move when player moves
    win_score = 5

    while running:
        screen.fill(BLACK)

        # Paddle movement
        keys = pygame.key.get_pressed()
        player_movement = 0
        if keys[pygame.K_UP]:
            player_movement = -player_paddle.speed
        elif keys[pygame.K_DOWN]:
            player_movement = player_paddle.speed

        # If player moves the paddle, the ball moves proportionally
        movement_factor = abs(player_movement) / player_paddle.speed if player_movement != 0 else 0

        player_paddle.move(player_movement)

        # Move ball only if player moved the paddle
        if movement_factor > 0:
            ball.move(movement_factor)

        # Move AI paddle
        ai_move(ai_paddle, ball)

        # Check for paddle-ball collision (Player)
        if ball.x - ball.radius <= player_paddle.x + player_paddle.width:
            if player_paddle.y < ball.y < player_paddle.y + player_paddle.height:
                ball.dx *= -1  # Reverse ball direction
                ball.apply_spin(player_paddle)  # Apply spin based on impact location

        # Check for paddle-ball collision (AI)
        if ball.x + ball.radius >= ai_paddle.x:
            if ai_paddle.y < ball.y < ai_paddle.y + ai_paddle.height:
                ball.dx *= -1  # Reverse ball direction
                ball.apply_spin(ai_paddle)  # Apply spin based on impact location

        # Scoring
        if ball.x - ball.radius <= 0:
            ai_paddle.score += 1
            ball.reset_position()

        if ball.x + ball.radius >= WIDTH:
            player_paddle.score += 1
            ball.reset_position()

        # Check for win condition
        if player_paddle.score == win_score or ai_paddle.score == win_score:
            winner = "Player" if player_paddle.score == win_score else "AI"
            print(f"{winner} wins!")
            running = False

        # Draw everything
        player_paddle.draw()
        ai_paddle.draw()
        ball.draw()
        draw_score(player_paddle, ai_paddle)

        # Handle game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)  # Limit frame rate to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()

