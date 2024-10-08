import pygame
import sys
import os

def main():
    pygame.init()

    WIDTH, HEIGHT = 1000, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Instructor Mode")

    clock = pygame.time.Clock()

    BG = pygame.transform.scale(pygame.image.load("backgrounds/bg_offwhite.jpg"),(WIDTH, HEIGHT))
    font = pygame.font.SysFont("arial", 45)
    smallfont = pygame.font.SysFont("arial", 20)
    black = (10, 10, 10)
    grey = (112, 128, 144)
    red = (255, 0, 0)
    outline_thickness = 2

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
    SOL_BOX_Y = 200
    SOL_BOX_X = 375

    current_question_index = 0

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
        return smallfont.render(questions[current_question_index], True, black)

    def get_question_number_text():
        return font.render(f"Question Number: {current_question_index + 1}", True, black)

    def get_current_options():
        return options[current_question_index]

    def get_current_answer():
        return options[current_question_index]

    class Button:
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
                font = pygame.font.SysFont('arial', 20)
                text = font.render(self.text, 1, (0, 0, 0))
                win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        def is_over(self, pos):
            # Pos is the mouse position or a tuple of (x,y) coordinates
            if self.x < pos[0] < self.x + self.width:
                if self.y < pos[1] < self.y + self.height:
                    return True
            return False

    class DraggableItem:
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

    next_question_button = Button(grey, WIDTH -200, HEIGHT - 160, 160, 40, 'Next Question')
    prev_question_button = Button(grey, WIDTH -400, HEIGHT - 160, 160, 40, 'Prev Question')
    add_question_button = Button(grey, WIDTH -950, HEIGHT - 160, 160, 40, 'Add Question')
    see_answer_button = Button(grey, WIDTH -600, HEIGHT - 160, 160, 40, 'See Answer')


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

    def run_script(file_name):
        try:
            os.system(f'python {file_name}')
        except Exception as e:
            print(f"Failed to run the script: {e}")

    show_answer = False


    run = True
    # Inside the game loop
    while run:

        answer = answers[current_question_index]

        WIN.blit(BG, (0, 0))
        WIN.blit(question_number_text, (LEFT_MARGIN, TOP_MARGIN))
        WIN.blit(question_description_text, (LEFT_MARGIN, TOP_MARGIN + 60))

        # Draw the  buttons
        next_question_button.draw(WIN, black)
        prev_question_button.draw(WIN, black)
        add_question_button.draw(WIN, black)
        see_answer_button.draw(WIN,black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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
                mouse_pos = pygame.mouse.get_pos()
                if add_question_button.is_over(pygame.mouse.get_pos()):
                    run_script('addQuestion.py')
                if next_question_button.is_over(mouse_pos):
                    current_question_index = (current_question_index + 1) % len(questions)
                    question_description_text = get_question_text()
                    question_number_text = get_question_number_text()
                    items = create_draggable_items()
                    feedback_update = False
                    feedback_text = ""

                if prev_question_button.is_over(mouse_pos):  # Check if 'Prev Question' button is clicked
                    current_question_index = (current_question_index - 1) % len(questions)
                    question_description_text = get_question_text()
                    question_number_text = get_question_number_text()
                    items = create_draggable_items()
                if see_answer_button.is_over(mouse_pos):
                    show_answer = not show_answer

        for item in items:
            item.draw(WIN)

        for blank in blanks:
            pygame.draw.rect(WIN, black, (SOL_BOX_X, SOL_BOX_Y, 100, 50), outline_thickness)

        if feedback_text != "":
            if feedback_update:
                feedback_message = font.render("Correct", True,(0, 255, 0))
            else:
                feedback_message = font.render("Wrong", True, red)
            WIN.blit(feedback_message, (WIDTH // 2 - feedback_message.get_width() // 2, HEIGHT // 2))

        if show_answer:
            answer_text = smallfont.render(f"Answer: {answers[current_question_index]}", True, black)
            WIN.blit(answer_text, (LEFT_MARGIN, ANSWER_BANK_Y-150))



        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
