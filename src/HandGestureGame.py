import pygame
import random
import sys
from HandGestureRecognizer import HandGestureRecognizer

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F']

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load HighMount font
try:
    highmount_font = pygame.font.Font("../fonts/HighMount.ttf", 36)
except Exception as e:
    print(f"Error loading HighMount font: {e}")
    highmount_font = pygame.font.Font(None, 36)  # Default font if HighMount font fails to load

# Load bear frames
bear_frames = []
for i in range(1, 5):  # Adjust the range based on the number of frames
    frame_path = f"../images/bear_{i:03d}.png"
    frame = pygame.image.load(frame_path)
    scaled_frame = pygame.transform.scale(frame, (200, 200))  # Scale to 200x200 size
    bear_frames.append(scaled_frame)

# Load raccoon frames
raccoon_frames = []
for i in range(1, 5):  # Adjust the range based on the number of frames
    frame_path = f"../images/raccoon_{i:03d}.png"
    frame = pygame.image.load(frame_path)
    scaled_frame = pygame.transform.scale(frame, (200, 200))  # Scale to 200x200 size
    raccoon_frames.append(scaled_frame)

# Load tent image
try:
    tent_image = pygame.image.load("../images/tent.png")
except Exception as e:
    print(f"Error loading tent.png: {e}")
    sys.exit()

# Load background image
try:
    background_image = pygame.image.load("../images/background.png")
except Exception as e:
    print(f"Error loading background.png: {e}")
    sys.exit()

# Scale the images to fit the game window or desired size
background_image_scaled = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
enemy_size = 200  # Adjusted size for scaled frames

# Scale the tent image
tent_image_scaled = pygame.transform.scale(tent_image, (300, 300))  # Larger tent image

class Square:
    def __init__(self, x, y, letter, speed=0.75, frames=None):
        self.rect = pygame.Rect(x, y, enemy_size, enemy_size)  # Adjusted rectangle size
        self.letter = letter
        self.speed = speed
        self.frames = frames
        self.frame_index = 0
        self.last_frame_time = pygame.time.get_ticks()

    def draw(self):
        if self.frames:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= 200:  # Change frame every 200 milliseconds
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.last_frame_time = current_time
            screen.blit(self.frames[self.frame_index], self.rect)
        else:
            # If no frames are provided, use a default image (not needed here since we're using frames)
            pass
        letter_text = highmount_font.render(self.letter, True, (0, 0, 0))  # Black text on top of image
        letter_rect = letter_text.get_rect(center=self.rect.center)
        screen.blit(letter_text, letter_rect)

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

    game_over_text = highmount_font.render("Aw shucks! Your tent got rummaged!", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(600, 300))
    screen.blit(game_over_text, game_over_rect)
    score_text = highmount_font.render(f"Final Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(600, 400))
    screen.blit(score_text, score_rect)
    restart_text = highmount_font.render("Press Space to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(600, 500))
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    recognizer = HandGestureRecognizer()
    squares = []
    spawn_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_timer, 2500)  # Spawn every second
    score = 0
    speed = 0.75
    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    squares = []
                    score = 0
                    speed = 1
            elif event.type == spawn_timer and not game_over:
                side = random.choice(['top', 'bottom', 'left', 'right'])
                letter = random.choice(LETTERS)
                if side == 'top':
                    if random.random() < 0.5:
                        square = Square(random.randint(0, WIDTH - enemy_size), 0, letter, speed, frames=bear_frames)
                    else:
                        square = Square(random.randint(0, WIDTH - enemy_size), 0, letter, speed, frames=raccoon_frames)
                elif side == 'bottom':
                    if random.random() < 0.5:
                        square = Square(random.randint(0, WIDTH - enemy_size), HEIGHT - enemy_size, letter, speed, frames=bear_frames)
                    else:
                        square = Square(random.randint(0, WIDTH - enemy_size), HEIGHT - enemy_size, letter, speed, frames=raccoon_frames)
                elif side == 'left':
                    if random.random() < 0.5:
                        square = Square(0, random.randint(0, HEIGHT - enemy_size), letter, speed, frames=bear_frames)
                    else:
                        square = Square(0, random.randint(0, HEIGHT - enemy_size), letter, speed, frames=raccoon_frames)
                elif side == 'right':
                    if random.random() < 0.5:
                        square = Square(WIDTH - enemy_size, random.randint(0, HEIGHT - enemy_size), letter, speed, frames=bear_frames)
                    else:
                        square = Square(WIDTH - enemy_size, random.randint(0, HEIGHT - enemy_size), letter, speed, frames=raccoon_frames)
                squares.append(square)

        if not game_over:
            # Draw the background image first
            screen.blit(background_image_scaled, (0, 0))

            # Draw the tent image in the center of the screen
            screen.blit(tent_image_scaled,
                        (WIDTH // 2 - tent_image_scaled.get_width() // 2,
                         HEIGHT // 2 - tent_image_scaled.get_height() // 2))

            result = recognizer.recognize_gesture()
            if result:
                for square in squares[:]:
                    if square.letter == result:
                        squares.remove(square)
                        score += 1
                        if score % 10 == 0:
                            speed += 1

            for square in squares:
                square.draw()
                square.move()
                if square.rect.collidepoint(WIDTH // 2, HEIGHT // 2):
                    print("Game Over!")
                    game_over = True

            # Draw score
            score_text = highmount_font.render(f"Score: {score}", True, (0, 0, 0))
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

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
