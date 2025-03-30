import pygame
import random
import sys
import menu
from HandGestureRecognizer import HandGestureRecognizer

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F']

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load bear frames
bear_frames = []
for i in range(1, 5):  # Adjust the range based on the number of frames
    frame_path = f"../images/BearShadow_{i:03d}.png"
    frame = pygame.image.load(frame_path)
    scaled_frame = pygame.transform.scale(frame, (200, 200))  # Scale to 200x200 size
    bear_frames.append(scaled_frame)

# Load raccoon frames
raccoon_frames = []
for i in range(1, 5):  # Adjust the range based on the number of frames
    frame_path = f"../images/RaccoonShadow_{i:03d}.png"
    frame = pygame.image.load(frame_path)
    scaled_frame = pygame.transform.scale(frame, (200, 200))  # Scale to 200x200 size
    raccoon_frames.append(scaled_frame)

# Load background images
background_images = []
for i in range(1, 4):  # Load background_001 to background_003
    try:
        background_image = pygame.image.load(f"../images/background_{i:03d}.png")
        background_images.append(pygame.transform.scale(background_image, (WIDTH, HEIGHT)))
    except Exception as e:
        print(f"Error loading background_{i:03d}.png: {e}")
        sys.exit()

# Scale the images to fit the game window or desired size
background_image_scaled = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
enemy_size = 225  # Adjusted size for scaled frames

class Square:
    def __init__(self, x, y, letter, speed=1, frames=None):
        self.rect = pygame.Rect(x, y, enemy_size, enemy_size)  # Adjusted rectangle size
        self.letter = letter
        self.speed = speed
        self.frames = frames
        self.frame_index = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.font = pygame.font.Font("../fonts/WildFont.ttf", 48)  # Use custom font

    def draw(self):
        if self.frames:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= 200:  # Change frame every 200 milliseconds
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.last_frame_time = current_time
            screen.blit(self.frames[self.frame_index], self.rect)
        text = self.font.render(self.letter, True, (0, 0, 0))  # Black text on top of image
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def move(self):
        if self.rect.x < WIDTH / 2:
            self.rect.x += self.speed
        elif self.rect.x > WIDTH / 2:
            self.rect.x -= self.speed
        if self.rect.y < HEIGHT / 2:
            self.rect.y += self.speed
        elif self.rect.y > HEIGHT / 2:
            self.rect.y -= self.speed


def draw_restart_screen(score):
    # Load game over screen background
    try:
        game_over_background = pygame.image.load("../images/game_over_screen.png")
        game_over_background_scaled = pygame.transform.scale(game_over_background, (1200, 800))
    except Exception as e:
        print(f"Error loading game_over_screen.png: {e}")
        screen.fill((255, 255, 255))  # Default white background if image fails to load
    else:
        screen.blit(game_over_background_scaled, (0, 0))

    font = pygame.font.Font("../fonts/WildFont.ttf", 38)  # Use custom font for restart screen text
    high_score = load_high_score()
    if score > high_score:
        high_score_text = font.render(f"NEW HIGH SCORE!", True, (124, 252, 0))
        save_high_score(score)
    else:
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))

    high_score_rect = high_score_text.get_rect(center=(600, 350))
    screen.blit(high_score_text, high_score_rect)

    text = font.render("Aww shucks! Your tent got rummaged!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(600, 200))
    screen.blit(text, text_rect)

    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(600, 300))
    screen.blit(score_text, score_rect)

    restart_text = font.render("Press SPACE to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(600, 400))
    screen.blit(restart_text, restart_rect)

    reset_text = font.render("Press BACKSPACE to go to Menu", True, (255, 255, 255))
    reset_rect = reset_text.get_rect(center=(600, 500))
    screen.blit(reset_text, reset_rect)

    pygame.display.flip()

import json

def load_high_score():
    try:
        with open('high_score.json', 'r') as file:
            return json.load(file)['high_score']
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open('high_score.json', 'w') as file:
        json.dump({'high_score': score}, file)

def main():
    clock = pygame.time.Clock()
    recognizer = HandGestureRecognizer()
    squares = []
    spawn_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_timer, 2500)  # Spawn every second
    score = 0
    speed = 1
    lives = 3
    background_index = 0
    game_over = False
    start_time = pygame.time.get_ticks()  # Record the start time

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    squares.clear()
                    score = 0
                    speed = 1
                    lives = 3
                    background_index = 0
                elif event.key == pygame.r and game_over:
                    # Reset game state and return to main menu
                    game_over = False
                    running = False
                    squares = []
                    score = 0
                    speed = 1
                    lives = 3
                    background_index = 0
                    menu.main(load_high_score())
            elif event.type == spawn_timer and not game_over:
                side = random.choice(['top', 'bottom', 'left', 'right'])
                letter = random.choice(LETTERS)
                if side == 'top':
                    square_frames = bear_frames if random.random() < 0.5 else raccoon_frames
                    square = Square(random.randint(0, WIDTH - 200),
                                    0,
                                    letter,
                                    speed,
                                    frames=square_frames)
                elif side == 'bottom':
                    square_frames = bear_frames if random.random() < 0.5 else raccoon_frames
                    square = Square(random.randint(0, WIDTH - 200),
                                    HEIGHT - 200,
                                    letter,
                                    speed,
                                    frames=square_frames)
                elif side == 'left':
                    square_frames = bear_frames if random.random() < 0.5 else raccoon_frames
                    square = Square(0,
                                    random.randint(0, HEIGHT - 200),
                                    letter,
                                    speed,
                                    frames=square_frames)
                elif side == 'right':
                    square_frames = bear_frames if random.random() < 0.5 else raccoon_frames
                    square = Square(WIDTH - 200,
                                    random.randint(0, HEIGHT - 200),
                                    letter,
                                    speed,
                                    frames=square_frames)
                squares.append(square)

        if not game_over:
            screen.blit(background_images[background_index], (0, 0))
            result = recognizer.recognize_gesture()
            if result:
                for square in squares[:]:
                    if square.letter == result:
                        squares.remove(square)
                        score += 1

            # Gradually increase speed over time
            speed += 0.0012  # Increase speed by a small amount every second

            for square in squares[:]:
                square.speed = speed  # Update square speed
                square.draw()
                square.move()
                if square.rect.collidepoint(WIDTH // 2, HEIGHT // 2):
                    lives -= 1
                    background_index = min(background_index + 1, len(background_images) - 1)
                    # Clear all enemies on the screen when hit
                    squares.clear()  # This line clears all squares
                    if lives == 0:
                        game_over = True

            font = pygame.font.Font("../fonts/WildFont.ttf", 34)
            score_text = font.render(f"Score:{score}", True, (255, 215, 0))

            # Draw score
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
        else:
            draw_restart_screen(score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_over = False
                        squares = []
                        score = 0
                        speed = 1
                        lives = 3
                        background_index = 0
                    if event.key == pygame.K_BACKSPACE:
                        game_over = False
                        squares = []
                        score = 0
                        speed = 1
                        lives = 3
                        background_index = 0
                        menu.main(load_high_score())

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
