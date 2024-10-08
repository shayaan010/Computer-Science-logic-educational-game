"""
Leaderboard Display for game.

This module provides functionality to display a leaderboard in a Pygame application.
It reads scores from a file, sorts them, and displays the top entries.

Author: Aryaman
Date: 31/3/2024
Version: 1.0
"""
import pygame
import subprocess
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Get the screen size
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h

    # Create the screen
    screen = pygame.display.set_mode((width, height))

    # Load background image
    bg = pygame.transform.scale(pygame.image.load("backgrounds/bg_offwhite.jpg"), (width, height))

    # Blit the background
    screen.blit(bg, (0, 0))

    # Create fonts
    text_font = pygame.font.SysFont(None, 50)
    bold_text_font = pygame.font.SysFont(None, 45, bold=True)

    def draw_text(text, font, color, x, y):
        """
        Draws text on the Pygame window.
        Args:
            text (str): The text to be drawn.
            font (pygame.font.Font): The font to be used for the text.
            color (tuple): RGB color value for the text.
            x, y (int): The x and y coordinates for the text's position.
        """

        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    def read_leaderboard(file_name):
        """
        Reads and parses the leaderboard file, sorts entries by score.
        Args:
            file_name (str): The file path of the leaderboard data.
        Returns:
            list[tuple]: A list of tuples (player name, score) sorted by score.
        """
        players = []
        try:
            with open(file_name, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]  # This removes any empty lines
                # Group lines into pairs (name, score) and convert score to int
                it = iter(lines)
                players = [(name, int(score)) for name, score in zip(it, it)]
        except FileNotFoundError:
            print(f"The file was not found: {file_name}")
            return [("None user", 0) for _ in range(5)]

        # Sort the list of players by score in descending order
        players.sort(key=lambda player: player[1], reverse=True)

        # If there are more than 5 players, keep only the top 5
        players = players[:5]

        # If there are less than 5 players, fill the remaining positions with "None user" and 0
        while len(players) < 5:
            players.append(("None user", 0))

        return players



    # Load leaderboard data
    leaderboard_data = read_leaderboard("scores.txt")

    button_width, button_height = 120, 50
    button_x, button_y = width - button_width - 30, 30

    def draw_button(x, y, width, height, text):
        """
        Draws a button on the Pygame window.
        Args:
            x, y (int): The x and y coordinates for the button's position.
            width, height (int): The width and height of the button.
            text (str): The text to be displayed on the button.
        """
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height))
        draw_text(text, text_font, (255, 255, 255), x + 20, y + 10)

    # Check for button click
    def button_clicked(pos, x, y, width, height):
        """
        Checks if a button is clicked.
        Args:
            pos (tuple): The mouse position.
            x, y (int): The x and y coordinates for the button's position.
            width, height (int): The width and height of the button.
        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        return x < pos[0] < x + width and y < pos[1] < y + height

    # Main game loop
    running = True
    while running:
        screen.blit(bg, (0, 0))

        # display headers
        draw_text("Position", bold_text_font, (0, 0, 0), 70, 60)
        draw_text("Player", bold_text_font, (0, 0, 0), 300, 60)
        draw_text("High Score", bold_text_font, (0, 0, 0), 620, 60)
        # Draw the return to main menu button
        draw_button(button_x, button_y, button_width, button_height, "Back")

        # display leaderboard entries
        for i, (player, score) in enumerate(leaderboard_data):
            # Display the position numbering text
            draw_text(f"Position {i + 1}", text_font, (0, 0, 0), 70, 100 + i * 100)
            # Display the player name
            draw_text(player, text_font, (0, 0, 0), 300, 100 + i * 100)
            # Display the player score
            draw_text(str(score), text_font, (0, 0, 0), 620, 100 + i * 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    # go to main menu
                    path = 'landingPage.py'
                    subprocess.run([sys.executable, path])

                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_clicked(event.pos, button_x, button_y, button_width, button_height):
                    pygame.quit()
                    path = 'landingPage.py'
                    subprocess.run([sys.executable, path])
                    running = False

        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
if __name__ == "__main__":
    main()
