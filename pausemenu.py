# This is the page object for the pause menu of the application
# This page object is used for the user to choose an option when the game is paused.
import pygame
import sys
import subprocess

# Initialize the Pygame
pygame.init()
# initialize the font
pygame.font.init()

# Get the screen size
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Logic Quest")

# load background image
BG = pygame.transform.scale(pygame.image.load("backgrounds/bg_offwhite.jpg"), (WIDTH, HEIGHT))

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# Calculate the center coordinates
center_x = WIDTH / 2 - 200 / 2
center_y = HEIGHT / 2 - 100 / 2

# Create the buttons
# create the resume button at the center of the screen
resume = pygame.Rect(600, 350, 320, 100)
# create the save game button
save_game = pygame.Rect(600, 500, 320, 100)
# go back to exit game button
exit_game = pygame.Rect(600, 650, 320, 100)

class Button:
    def __init__(self, text, color, width, height, pos, elevation, action=None):
        # attributes
        self.pressed = False
        self.elevation = elevation
        self.dElevation = elevation
        self.original_y_position = pos[1]
        self.action = action

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = color
        self.main_color = color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = BLACK

        # text
        self.text_surf = pygame.font.SysFont('Arial', 50).render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevate the button
        self.top_rect.y = self.original_y_position - self.dElevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dElevation

        pygame.draw.rect(WIN, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(WIN, self.top_color, self.top_rect, border_radius=12)
        WIN.blit(self.text_surf, self.text_rect)
        self.checkClick()

    def checkClick(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#0096FF'
            if pygame.mouse.get_pressed()[0]:
                self.dElevation = 0
                self.pressed = True
            else:
                self.dElevation = self.elevation
                if self.pressed:
                    self.pressed = False
        else:
            self.dElevation = self.elevation
            self.top_color = self.main_color

        if self.pressed:
            if self.action:
                self.action()
            self.pressed = False

def resume():
    path = "trainingmode.py"
    subprocess.run([sys.executable, path])



def save_progress():
    """Save the current game progress."""
    # You might need a more complex logic to handle the current level
    global current_username, current_level
    with open('progress.txt', 'a+') as file:
        file.seek(0)
        progress_data = file.readlines()
        progress_dict = {line.split(':')[0]: int(line.split(':')[1]) for line in progress_data if ':' in line}

        if current_username in progress_dict:
            if current_level > progress_dict[current_username]:
                progress_dict[current_username] = current_level
        else:
            progress_dict[current_username] = current_level

        file.truncate(0)  # Clear the file before writing the updated progress
        for username, level in progress_dict.items():
            file.write(f"{username}:{level}\n")

    print(f"Progress saved for {current_username}: Level {current_level}")

def quit_game():
    path = 'landingPage.py'
    subprocess.run([sys.executable, path])
    pygame.quit()

# create the buttons
resume_game = Button("RESUME", '#89CFF0', 320, 80, (WIDTH / 2 - 340 / 2, HEIGHT / 2 - 200), 6, resume)
save_game = Button("SAVE GAME", '#89CFF0', 320, 80, (WIDTH / 2 - 340 / 2, HEIGHT / 2 - 80), 6, save_progress)
main_menu = Button("EXIT GAME", '#89CFF0', 320, 80, (WIDTH / 2 - 340 / 2, HEIGHT / 2 + 40), 6, quit_game)

def main():
    global WIN, run
    run = True
    WIN.blit(BG, (0, 0))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
            if event.type == pygame.VIDEORESIZE:
                WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # draw()

        # draw a title on screen
        font = pygame.font.SysFont('Arial', 100)
        text = font.render("GAME PAUSED", True, BLACK)
        WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, 100))

        # draw the buttons
        resume_game.draw()
        save_game.draw()
        main_menu.draw()

        pygame.display.update()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
