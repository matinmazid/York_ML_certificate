import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 10
BUMPER_WIDTH = BALL_RADIUS * 5
BAND_THICKNESS = BALL_RADIUS
BAND_GAP_WIDTH = BALL_RADIUS * 3
BALL_COLOR = (255, 165, 0)  # Orange
BAND_COLOR = (169, 169, 169)  # Grey
BUMPER_COLOR = (255, 215, 0)  # Yellow
BACKGROUND_COLOR = (0, 0, 0)  # Black

# Game Variables
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_velocity = [5 * random.choice([-1, 1]), 5 * random.choice([-1, 1])]
band_x_position = SCREEN_WIDTH // 2
bumper_x_position = SCREEN_WIDTH // 2
score = 0

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Inspired Game")

# Load sounds
happy_sound = pygame.mixer.Sound("happy_trumpet.wav")

def draw_ball():
    """Draws the ball on the screen."""
    pygame.draw.circle(screen, BALL_COLOR, (ball_pos[0], ball_pos[1]), BALL_RADIUS)

def draw_band():
    """Draws the grey band at the top with a gap."""
    pygame.draw.rect(screen, BAND_COLOR, (0, 0, SCREEN_WIDTH, BAND_THICKNESS))
    pygame.draw.rect(screen, BACKGROUND_COLOR, (band_x_position - BAND_GAP_WIDTH // 2, 0, BAND_GAP_WIDTH, BAND_THICKNESS))

def draw_bumper():
    """Draws the yellow bumper at the bottom."""
    pygame.draw.rect(screen, BUMPER_COLOR, (bumper_x_position - BUMPER_WIDTH // 2, SCREEN_HEIGHT - BAND_THICKNESS, BUMPER_WIDTH, BAND_THICKNESS))

def check_collision():
    """Checks for collisions between the ball and game elements."""
    global score, ball_velocity

    # Check collision with the band
    if ball_pos[1] <= BAND_THICKNESS and band_x_position - BAND_GAP_WIDTH // 2 < ball_pos[0] < band_x_position + BAND_GAP_WIDTH // 2:
        happy_sound.play()
        score += 1  # Increment score when the ball goes through the gap
        ball_velocity[1] = -ball_velocity[1]  # Reverse the ball's vertical direction

    # Check collision with the bumper
    elif ball_pos[1] >= SCREEN_HEIGHT - BAND_THICKNESS and bumper_x_position - BUMPER_WIDTH // 2 < ball_pos[0] < bumper_x_position + BUMPER_WIDTH // 2:
        ball_velocity[1] = -ball_velocity[1]  # Reverse the ball's vertical direction

    # Bounce off the sides
    if ball_pos[0] <= BALL_RADIUS or ball_pos[0] >= SCREEN_WIDTH - BALL_RADIUS:
        ball_velocity[0] = -ball_velocity[0]  # Reverse the ball's horizontal direction

    # Check if the ball falls below the bumper
    if ball_pos[1] > SCREEN_HEIGHT:
        print("Game Over! Final Score:", score)
        pygame.quit()
        sys.exit()

def move_elements():
    """Moves the band based on the game's mechanics."""
    global band_x_position
    band_x_position += random.choice([-1, 1]) * 5  # Move band left or right
    band_x_position = max(BAND_GAP_WIDTH // 2, min(band_x_position, SCREEN_WIDTH - BAND_GAP_WIDTH // 2))  # Keep band within bounds

def main():
    """Main game loop."""
    global ball_pos, ball_velocity, bumper_x_position

    while True:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update ball position
        ball_pos[0] += ball_velocity[0]
        ball_pos[1] += ball_velocity[1]

        # Move bumper based on keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and bumper_x_position > BUMPER_WIDTH // 2:
            bumper_x_position -= 10  # Move bumper left
        if keys[pygame.K_RIGHT] and bumper_x_position < SCREEN_WIDTH - BUMPER_WIDTH // 2:
            bumper_x_position += 10  # Move bumper right

        # Draw game elements
        draw_ball()
        draw_band()
        draw_bumper()

        # Check for collisions
        check_collision()

        # Move band
        move_elements()

        # Update the display
        pygame.display.flip()
        pygame.time.delay(30)

if __name__ == "__main__":
    main()