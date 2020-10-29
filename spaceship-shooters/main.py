import pygame

from assets import spaceship_shooters
from assets.buttons import Button

pygame.font.init()

# For white text
# Different to white in case only text colour needs to be changed
TEXT_COLOUR = (255, 255, 255)
WHITE = (255, 255, 255)
SILVER = (192, 192, 192)
BLACK = (0, 0, 0)

# Constants for the window size
WIDTH, HEIGHT = 750, 750

# Define window for program
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Shooters!")

# FPS for the game, game will be limited to this many frames per second
FPS = 60

# Fonts
title_font = pygame.font.SysFont("arial", 40)
button_font = pygame.font.SysFont("arial", 30)

# Button functions ------------------------------------------------------------------------------------------------------------------


def open_game_loop():
    """Run main loop from spaceship_shooters.py in normal mode"""

    spaceship_shooters.game_loop(WIN, WIDTH, HEIGHT, FPS, "normal")


def open_op_game_loop():
    """Run main loop from spaceship_shooters.py in op mode"""

    spaceship_shooters.game_loop(WIN, WIDTH, HEIGHT, FPS, "op")


# Main Function, opens the game's main menu ---------------------------------------------------------------------------------------------


def main_menu():
    run = True
    # Clock used to force the program to run at given fps, otherwise the program would run at different speeds
    # based on each computers processing speed
    clock = pygame.time.Clock()

    # Variable to check if the left mouse button has been pressed
    clicked = False

    # Will contain all the buttons, so they can be looped through in a for loop
    buttons = []

    # DEFINE BUTTONS
    # starts game in normal mode
    game_button = Button(
        BLACK,
        WHITE,
        WIDTH // 2 - WIDTH // 8,  # Removing half the width so it's in the middle
        HEIGHT * 4 // 10,
        WIDTH // 4,
        HEIGHT // 15,
        open_game_loop,
        text="Start Game",
        outline=SILVER,
    )
    buttons.append(game_button)

    # starts the game in op mode
    op_button = Button(
        BLACK,
        WHITE,
        WIDTH // 2 - WIDTH // 6,  # Removing half the width so it's in the middle
        HEIGHT * 5 // 10,
        WIDTH // 3,
        HEIGHT // 15,
        open_op_game_loop,
        text="Play in OP mode",
        outline=SILVER,
    )
    buttons.append(op_button)

    # Exits the application
    quit_button = Button(
        BLACK,
        WHITE,
        WIDTH // 2 - WIDTH // 8,  # Removing half the width so it's in the middle
        HEIGHT * 6 // 10,
        WIDTH // 4,
        HEIGHT // 15,
        quit,
        text="Exit Game",
        outline=SILVER,
    )
    buttons.append(quit_button)

    # Main Menu Loop ---------------------------------------------------------------------------------------------------------------
    while run:
        clock.tick(FPS)

        # Display background image asset loaded in spaceship_shooters.py
        WIN.blit(spaceship_shooters.BG, (0, 0))

        # Display title label
        title_label = title_font.render(
            "Welcome to Spaceship Shooters!", 1, TEXT_COLOUR
        )
        WIN.blit(
            title_label,
            (
                WIDTH // 2
                - title_label.get_width()
                // 2,  # So that the label is placed in the middle of the screen
                HEIGHT // 15,
            ),
        )

        # BUTTONS
        xpos, ypos = pygame.mouse.get_pos()

        for button in buttons:
            button.draw(WIN, button_font, xpos, ypos)
            if button.is_selected(xpos, ypos):
                if clicked:
                    button.on_clicked()

        # Reset the clicked value
        clicked = False

        pygame.display.update()

        # Set events so that exiting the app closes the window and clicking the mouse begins the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

    pygame.quit()


if __name__ == "__main__":
    main_menu()
