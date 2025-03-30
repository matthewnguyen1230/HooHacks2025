import pygame
import pygame.freetype
import os

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Sign of the Wild")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up title
current_dir = os.path.dirname(__file__)
title_image_path = os.path.join(current_dir, "../assets/images/title.png")
title_image = pygame.image.load(title_image_path)

# Load the background image
bg_image_path = os.path.join(current_dir, "../assets/images/title_background.png")
background = pygame.image.load(bg_image_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Button class
class Button:
    def __init__(self, x, y, width, height, text, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont("Arial", font_size)
        self.is_hovered = False

    def draw(self, surface):
        # Draw button background
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border

        # Render text
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click


# Main function
def main():
    clock = pygame.time.Clock()
    running = True

    # Get title image dimensions
    title_width = title_image.get_width()
    title_height = title_image.get_height()

    # Calculate position to center the title image
    title_x = WIDTH // 2 - title_width // 2
    title_y = 0

    # Create start button
    start_button = Button(WIDTH // 2 - 100, title_height,
                          200, 50, "START GAME")

    while running:
        mouse_click = False
        mouse_pos = pygame.mouse.get_pos()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_click = True

        # Check button interaction
        start_button.check_hover(mouse_pos)
        if start_button.is_clicked(mouse_pos, mouse_click):
            print("Game started!")  # Replace with your game start function

        # Fill background
        screen.blit(background, (0, 0))

        # Draw title image
        screen.blit(title_image, (title_x, title_y))

        # Draw button
        start_button.draw(screen)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()