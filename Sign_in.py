import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("logic game")

clock = pygame.time.Clock()

BG = pygame.image.load("bg_offwhite.jpg")
font = pygame.font.SysFont("garamond", 45)
smallfont = pygame.font.SysFont("garamond", 20)
black = (10, 10, 10)
grey = (112, 128, 144)
blue = (0, 0, 255)


class TextInputBox:
    def __init__(self, x, y, width, height, font, text_color, inactive_color, active_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = inactive_color
        self.text = ''
        self.font = font
        self.text_color = text_color
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.active_color if self.active else self.inactive_color
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, win):
        txt_surface = self.font.render(self.text, True, self.text_color)
        width = max(self.rect.w, txt_surface.get_width()+10)
        self.rect.w = width
        win.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(win, self.color, self.rect, 2)


def create_button(msg, x, y, hc, dc, fc):
    button_width = 150
    button_height = 50

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

    if (x + button_width > mouse[0] > x and y + button_height > mouse[1] > y):
        pygame.draw.rect(WIN, hc, (x, y, button_width, button_height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(WIN, dc, (x, y, button_width, button_height))

    buttontext = smallfont.render(msg, True, fc)
    text_rect = buttontext.get_rect(center=(x + button_width / 2, y + button_height / 2))
    WIN.blit(buttontext, text_rect)


def login():
    login_text = font.render("Login Page", True, black)
    username_text = smallfont.render("Username: ", True, black)
    key_text = smallfont.render("Key(Optional): ", True, black)

    username_box = TextInputBox(200, 320, 140, 32, smallfont, black, grey, blue)
    key_box = TextInputBox(200, 420, 140, 32, smallfont, black, grey, blue)

    while True:
        WIN.blit(BG, (0, 0))
        WIN.blit(login_text, ((WIDTH - login_text.get_width()) / 2, 25))
        WIN.blit(username_text, (50, 325))
        WIN.blit(key_text, (50, 425))

        username_box.draw(WIN)
        key_box.draw(WIN)

        p_button = create_button("Proceed", WIDTH / 2 - 75, 500, grey, blue, black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            username_box.handle_event(event)
            key_box.handle_event(event)

        with open('usernames.txt', 'r') as file:
            with open ('keys.txt', 'r') as file2:
                content = file.read()
                content2 = file2.read()
                if username_box.text in content:
                    if p_button and key_box.text == '':
                        print("Proceed to main menu")
                        return True
                    elif p_button and key_box.text in content2:
                        print("Proceed to main menu as instructor/developer")
                        return True






        pygame.display.update()
        clock.tick(15)


def main():
    run = True
    while run:
        if login():
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit()


if __name__ == "__main__":
    main()
