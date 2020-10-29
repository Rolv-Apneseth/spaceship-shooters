import pygame


class Button:
    """Used to make buttons to put on display for pygame. A function must be defined for each button"""

    def __init__(
        self, colour1, colour2, x, y, width, height, function, text, outline=None
    ):
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
            pygame.draw.rect(
                win,
                self.outline,
                (
                    self.x - extra_x,
                    self.y - extra_y,
                    self.width + extra_x * 2,
                    self.height + extra_y * 2,
                ),
                0,
            )

        # If statement so that text and background colour for the button can alternate,
        # depending on whether the mouse is hovering over the button
        if self.is_selected(xpos, ypos):
            pygame.draw.rect(
                win, self.colour2, (self.x, self.y, self.width, self.height), 0
            )
            text = font.render(self.text, 1, self.colour1)
            win.blit(
                text,
                (
                    self.x + self.width // 2 - text.get_width() // 2,
                    self.y + self.height // 2 - text.get_height() // 2,
                ),
            )
        else:
            pygame.draw.rect(
                win, self.colour1, (self.x, self.y, self.width, self.height), 0
            )
            text = font.render(self.text, 1, self.colour2)
            win.blit(
                text,
                (
                    self.x + self.width // 2 - text.get_width() // 2,
                    self.y + self.height // 2 - text.get_height() // 2,
                ),
            )

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
        """Calls the function given when the button was instantiated."""
        self.function()
