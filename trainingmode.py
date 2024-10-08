"""
Training Mode for Logic Quest Game

This module implements a 'Training Mode' for the 'Logic Quest' game using Pygame. 
It features interactive draggable items for answering questions, feedback mechanisms, 
and a pause menu with options like resuming and exiting the game.

Classes:
    Button: A class for creating and managing buttons in the interface.
    DraggableItem: A class for creating draggable items used as answer choices.

Functions:
    get_question_text(): Retrieves the text for the current question.
    get_question_number_text(): Retrieves the text displaying the current question number.
    get_current_options(): Retrieves the current set of answer choices.
    get_current_answer(): Retrieves the correct answer for the current question.
    create_draggable_items(): Creates draggable items for the current question's answer choices.
    draw_pause_menu(): Draws and manages the pause menu interface.
    main(): The main function to run the training mode interface.

Author: Shayaan
Date: 30/3/2024
Version: 1.0
"""
import pygame
import sys
import subprocess

def main():
    pygame.init()

    screen_info = pygame.display.Info()
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Training Mode")

    clock = pygame.time.Clock()

    BG = pygame.transform.scale(pygame.image.load("backgrounds/bg_offwhite.jpg"),(WIDTH, HEIGHT))
    font = pygame.font.SysFont("arial", 45)
    mediumfont = pygame.font.SysFont("arial", 60)
    smallfont = pygame.font.SysFont("arial", 20)
    black = (10, 10, 10)
    grey = (112, 128, 144)
    red = (255, 0, 0)
    outline_thickness = 2

    # Set the color and thickness of the outline
    outline_color = (255, 255, 255)  # White outline
    outline_thickness = 2  # Thickness of the outline
    feedback_text= ""
    feedback_update = False

    TOP_MARGIN = 50
    BOTTOM_MARGIN = 100
    LEFT_MARGIN = 50
    ANSWER_BANK_Y = HEIGHT - BOTTOM_MARGIN + 20
    BLANKS_Y = TOP_MARGIN + 200
    BLANK_WIDTH = 100
    BLANK_HEIGHT = 30
    BLANK_SPACING = 20
    ANSWER_ITEM_SPACING = 120
    SOL_BOX_X = (WIDTH - BLANK_WIDTH) // 2
    SOL_BOX_Y = (HEIGHT - BLANK_HEIGHT) // 2 + 70

    game_state = "training"

    current_question_index = 0

    #check if load.txt is empty
    with open('load.txt', 'r') as f:
        lines = f.readlines()
        if len(lines) == 0:
            current_question_index = 0
        else:
            current_question_index = int(lines[0])
            #delete content of load.txt
            with open('load.txt', 'w') as f:
                f.write("")



    with open('cur_username.txt', 'r') as f:
        username = f.read()

    with open('questions.txt', 'r') as f:
        questions = []
        for line in f:
            if '.' in line:
                # Split line at the first dot and take the second part
                line_text = line.split('.', 1)[1].strip()
                questions.append(line_text)

    with open('options.txt', 'r') as f:
        raw_options = f.read().split('\n\n')
        options = [option.strip().split('\n') for option in raw_options]

    with open('answers.txt', 'r') as f:
        answers = []
        for line in f:
            if '.' in line:
                # Split line at the first dot and take the second part
                line_text = line.split('.', 1)[1].strip()
                answers.append(line_text)

    def get_question_text():
        return mediumfont.render(questions[current_question_index], True, black)

    def get_question_number_text():
        return font.render(f"Question Number: {current_question_index + 1}", True, black)

    def get_current_options():
        return options[current_question_index]

    def get_current_answer():
        return options[current_question_index]

    class Button:
        """
        Class for creating interactive buttons in the interface.

        Attributes:
            color (tuple): The color of the button.
            x, y (int): The x and y coordinates of the button.
            width, height (int): The width and height of the button.
            text (str): The text displayed on the button.

        Methods:
            draw(win, outline): Draws the button on the specified window.
            is_over(pos): Checks if the button is hovered over or clicked.
        """
        def __init__(self, color, x, y, width, height, text=''):
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text

        def draw(self, win, outline=None):
            if outline:
                pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

            if self.text != '':
                font = pygame.font.SysFont('Arial', 20)
                text = font.render(self.text, 1, (0, 0, 0))
                win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        def is_over(self, pos):
            # Pos is the mouse position or a tuple of (x,y) coordinates
            if self.x < pos[0] < self.x + self.width:
                if self.y < pos[1] < self.y + self.height:
                    return True
            return False

    class DraggableItem:
        """
        Class for creating draggable items representing answer choices.

        Attributes:
            text (str): The text displayed on the draggable item.
            rect (pygame.Rect): The rectangle defining the size and position.
            font (pygame.font.Font): The font used for rendering text.

        Methods:
            draw(win): Draws the draggable item on the specified window.
            handle_event(event): Handles events related to dragging the item.
            check_collision_with_ans(): Checks if the item collides with the answer area.
            is_ans(): Checks if the item is the correct answer.
        """
        def __init__(self, text, x, y, w, h, font, sol):
            self.text = text
            self.rect = pygame.Rect(x, y, w, h)
            self.font = font
            self.dragging = False
            self.offset_x = 0
            self.offset_y = 0
            self.sol = sol

        def draw(self, win):
            pygame.draw.rect(win, grey, self.rect)
            text_surface = self.font.render(self.text, True, black)
            win.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


        def handle_event(self, event):
            global current_question_index  # Reference the global variable
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mouse_x, mouse_y = event.pos
                    self.rect.x = mouse_x + self.offset_x
                    self.rect.y = mouse_y + self.offset_y

        def check_collision_with_ans(self):
            if self.rect.colliderect(pygame.Rect(SOL_BOX_X, SOL_BOX_Y, 100, 50)):
                print("collision")
                return True
            return False

        def is_ans(self):
            if self.sol:
                return True
            return False

    next_question_button = Button(grey, WIDTH - 200, HEIGHT - 60, 160, 40, 'Next Question')

    def create_draggable_items():
        answer = answers[current_question_index]
        current_options = get_current_options()

        if current_options[0].strip().endswith('.'):
            current_options = current_options[1:]

        item_width = 100  # Adjust the width as needed to fit the text
        total_width = (len(current_options) - 1) * ANSWER_ITEM_SPACING + len(current_options) * item_width
        start_x = (WIDTH - total_width) // 2  # Center the options
        drag_items = []
        for i, text in enumerate(current_options):
            if text == answer:
                drag_items.append(
                    DraggableItem(text, start_x + i * (item_width + ANSWER_ITEM_SPACING), ANSWER_BANK_Y, item_width, 50,
                                  smallfont, True))
            else:
                drag_items.append(
                    DraggableItem(text, start_x + i * (item_width + ANSWER_ITEM_SPACING), ANSWER_BANK_Y, item_width, 50,
                                  smallfont, False))
        return drag_items


    # Initial display setup
    question_description_text = get_question_text()
    question_number_text = get_question_number_text()
    items = create_draggable_items()

    blanks = [
         pygame.Rect(LEFT_MARGIN, BLANKS_Y, BLANK_WIDTH, BLANK_HEIGHT),
         # Add more Rects for blanks if needed
    ]


    def pause_game():
        path = "pausemenu.py"
        subprocess.run([sys.executable, path])
        pygame.quit()

    def quit():
        path = "landingPage.py"
        subprocess.run([sys.executable,path])
        pygame.quit()

    def saveGame():
        # skip line until empty line is found
        with open('progress.txt', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line == '\n':
                    break
        # write current users name to progress.txt
        with open('progress.txt', 'a') as f:
            f.write(username + '\n')
        # write current question number to progress.txt
        with open('progress.txt', 'a') as f:
            f.write(str(current_question_index) + '\n')


    # New Function to Draw Pause Menu
    def draw_pause_menu():
        """
        Draws and handles the pause menu, allowing the game to be paused, resumed, or exited.
        """
        WIN.blit(BG, (0, 0))
        # draw a title on screen
        title_font = pygame.font.SysFont('Arial', 80)
        text = title_font.render("GAME PAUSED", True, black)
        WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, 100))

        # Increased button dimensions for better visibility and interaction
        button_width = 300  # Increased width
        button_height = 100  # Increased height
        spacing = 120  # Space between buttons

        # Calculating the starting Y position so that buttons are centered vertically
        start_y = HEIGHT / 2 - (button_height * 3 + spacing * 2) / 2

        # Defining buttons with larger sizes
        resume_button = Button(grey, WIDTH / 2 - button_width / 2, start_y, button_width, button_height, 'RESUME')
        save_game_button = Button(grey, WIDTH / 2 - button_width / 2, start_y + button_height + spacing, button_width, button_height, 'SAVE GAME')
        exit_button = Button(grey, WIDTH / 2 - button_width / 2, start_y + 2 * (button_height + spacing), button_width,button_height, 'EXIT GAME')

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    text
                    if resume_button.is_over(pygame.mouse.get_pos()):
                        return  # Exit the pause menu and go back to training mode

                    if save_game_button.is_over(pygame.mouse.get_pos()):
                        saveGame()
                        # Display a message that the game has been saved
                        font = pygame.font.Font(None, 32)
                        text = font.render('Game has been saved', True, (0, 0, 0))
                        WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2 + 70))
                        pygame.display.update()
                        # remove the text after 2 seconds
                        pygame.time.delay(2000)
                        # remove the text
                        WIN.blit(BG, (0, 0))
                        pygame.display.update()

                    if exit_button.is_over(pygame.mouse.get_pos()):
                        quit()

            resume_button.draw(WIN, black)
            save_game_button.draw(WIN)
            exit_button.draw(WIN)
            pygame.display.update()

    run = True
    while run:

        answer = answers[current_question_index]

        WIN.blit(BG, (0, 0))
        WIN.blit(question_number_text, (LEFT_MARGIN, TOP_MARGIN))
        # Get the width and height of the question text
        text_width = question_description_text.get_width()
        text_height = question_description_text.get_height()
        WIN.blit(question_description_text, ((WIDTH - text_width) // 2, (HEIGHT - text_height) // 2))
        next_question_button.draw(WIN, black)
        # Create a Font object
        font = pygame.font.Font(None, 32)
        # Render the text into a Surface object
        text = font.render('P to pause', True, (0, 0, 0))
        # Get the width of the text
        text_width = text.get_width()
        # Blit the text Surface onto the window
        WIN.blit(text, (WIDTH - text_width - 10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Toggle pause menu
                    game_state = "paused" if game_state == "training" else "training"
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break

            if game_state == "training":
                pass
            elif game_state == "paused":
                draw_pause_menu()
                game_state = "training"


            for item in items:
                item.handle_event(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    if item.check_collision_with_ans() and item.is_ans():
                        feedback_update = True
                        feedback_text = "Correct"
                    elif item.check_collision_with_ans() and not item.is_ans():
                        feedback_update = False
                        feedback_text = "Wrong"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_question_button.is_over(pygame.mouse.get_pos()) and feedback_update:
                    current_question_index = (current_question_index + 1) % len(questions)
                    question_description_text = get_question_text()
                    question_number_text = get_question_number_text()
                    items = create_draggable_items()
                    feedback_update = False
                    feedback_text=""

        for item in items:
            item.draw(WIN)

        for blank in blanks:
            pygame.draw.rect(WIN, black, (SOL_BOX_X, SOL_BOX_Y, 100, 50), outline_thickness)

        if feedback_text != "":
            if feedback_update:
                feedback_message = font.render("Correct", True,(0, 255, 0))
            else:
                feedback_message = font.render("Wrong", True, red)
            WIN.blit(feedback_message, (WIDTH // 2 - feedback_message.get_width() // 2, (HEIGHT // 2) + 150))


        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
