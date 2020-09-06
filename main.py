import pygame

import spaceship_shooters

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

# Button class --------------------------------------------------------------------------------------------------------------------


class Button():
    """Used to make buttons to put on display for pygame. A function must be defined for each button"""

    def __init__(self, colour1, colour2, x, y, width, height, function, text, outline=None):
        # Two colous since the colours alternate depending on whether the mouse
        # is hovering over the button or not
        self.colour1 = colour1
        self.colour2 = colour2
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        # Function to be called when button.on_clicked() is called
        self.function = function
        # Colour of the outline of the button, if None then no outline will appear
        self.outline = outline

    def draw(self, win, font, xpos, ypos):
        """Used to draw buttons onto the display each frame"""

        # Draws an outline boax first if a colour was given
        if self.outline:
            extra_x = self.width // 40
            extra_y = self.height // 20
            pygame.draw.rect(win, self.outline,
                             (self.x - extra_x, self.y - extra_y,
                              self.width + extra_x * 2, self.height + extra_y * 2),
                             0
                             )

        # If statement so that text and background colour for the button can alternate,
        # depending on whether the mouse is hovering over the button
        if self.is_selected(xpos, ypos):
            pygame.draw.rect(win, self.colour2,
                             (self.x, self.y, self.width, self.height),
                             0
                             )
            text = font.render(self.text, 1, self.colour1)
            win.blit(text, (self.x + self.width // 2 - text.get_width() // 2,
                            self.y + self.height // 2 - text.get_height() // 2
                            ))
        else:
            pygame.draw.rect(win, self.colour1,
                             (self.x, self.y, self.width, self.height),
                             0
                             )
            text = font.render(self.text, 1, self.colour2)
            win.blit(text, (self.x + self.width // 2 - text.get_width() // 2,
                            self.y + self.height // 2 - text.get_height() // 2
                            ))

    def is_selected(self, xpos, ypos):
        """
        Must be given the x and y positions of the mouse. Use pygame.mouse.get_pos().
        Returns True if the mouse is hovering over the button.
        """
        if self.x < xpos < self.x + self.width:
            if self.y < ypos < self.y + self.height:
                return True
        return False

    def on_clicked(self):
        """Calls the function given when the button was instantiated"""
        self.function()


# Specific button functions ------------------------------------------------------------------------------------------------------------------
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

    # Contains the buttons, so they can be looped through in a for loop
    buttons = []

    # Define the buttons
    game_button = Button(BLACK,
                         WHITE,
                         WIDTH // 2 - WIDTH // 8,  # Removing half the width so it's in the middle
                         HEIGHT * 3 // 10,
                         WIDTH // 4,
                         HEIGHT // 15,
                         open_game_loop,
                         text='Start Game',
                         outline=SILVER
                         )
    buttons.append(game_button)

    op_button = Button(BLACK,
                       WHITE,
                       WIDTH // 2 - WIDTH // 6,  # Removing half the width so it's in the middle
                       HEIGHT * 4 // 10,
                       WIDTH // 3,
                       HEIGHT // 15,
                       open_op_game_loop,
                       text='Play in OP mode',
                       outline=SILVER
                       )
    buttons.append(op_button)

    while run:
        clock.tick(FPS)

        # Display background image asset loaded in spaceship_shooters.py
        WIN.blit(spaceship_shooters.BG, (0, 0))

        # Display title label
        title_label = title_font.render("Welcome to Spaceship Shooters!",
                                        1,
                                        TEXT_COLOUR
                                        )
        WIN.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2,  # So that the label is placed in the middle of the screen
                               HEIGHT // 15
                               ))

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
