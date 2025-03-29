import pygame
import random
import sys
from HandGestureRecognizer import HandGestureRecognizer

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F']

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Square:
    def __init__(self, x, y, letter):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.letter = letter

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.letter, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def move(self):
        if self.rect.x < WIDTH / 2:
            self.rect.x += 1
        elif self.rect.x > WIDTH / 2:
            self.rect.x -= 1
        if self.rect.y < HEIGHT / 2:
            self.rect.y += 1
        elif self.rect.y > HEIGHT / 2:
            self.rect.y -= 1

def main():
    clock = pygame.time.Clock()
    recognizer = HandGestureRecognizer()
    squares = []
    spawn_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_timer, 5000)  # Spawn every second
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():  # Use pygame.event.get()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == spawn_timer:
                if pygame.time.get_ticks() - start_time < 30000:  # 30 seconds
                    side = random.choice(['top', 'bottom', 'left', 'right'])
                    letter = random.choice(LETTERS)
                    if side == 'top':
                        square = Square(random.randint(0, WIDTH - 50), 0, letter)
                    elif side == 'bottom':
                        square = Square(random.randint(0, WIDTH - 50), HEIGHT - 50, letter)
                    elif side == 'left':
                        square = Square(0, random.randint(0, HEIGHT - 50), letter)
                    elif side == 'right':
                        square = Square(WIDTH - 50, random.randint(0, HEIGHT - 50), letter)
                    squares.append(square)

        screen.fill(WHITE)
        pygame.draw.circle(screen, BLACK, (WIDTH // 2, HEIGHT // 2), 50)

        result = recognizer.recognize_gesture()
        if result:
            for square in squares[:]:
                if square.letter == result:
                    squares.remove(square)

        for square in squares:
            square.draw()
            square.move()
            if square.rect.collidepoint(WIDTH // 2, HEIGHT // 2):
                print("Game Over!")
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()