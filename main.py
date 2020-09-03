import pygame

import spaceship_shooters

pygame.font.init()

# For white text
TEXT_COLOUR = (255, 255, 255)

# Constants for the window size
WIDTH, HEIGHT = 750, 750

# Define window for program
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Shooters!")


def main_menu():
    run = True
    title_font = pygame.font.SysFont("arial", 40)

    while run:
        # Display background image asset loaded in spaceship_shooters.py
        WIN.blit(spaceship_shooters.BG, (0, 0))

        # Display title label
        title_label = title_font.render("Welcome to Spaceship Shooters!",
                                        1,
                                        TEXT_COLOUR
                                        )
        WIN.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2,  # So that the label is placed in the middle of the screen
                               200
                               ))

        # Display click instruction label
        click_label = title_font.render("To begin the game, simply left click.",
                                        1,
                                        TEXT_COLOUR
                                        )
        WIN.blit(click_label, (WIDTH // 2 - click_label.get_width() // 2, 300))

        pygame.display.update()

        # Set events so that exiting the app closes the window and clicking the mouse begins the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Run main loop from spaceship_shooters.py
                spaceship_shooters.game_loop(WIN, WIDTH, HEIGHT)

    pygame.quit()


if __name__ == "__main__":
    main_menu()
