import pygame

import spaceship_shooters

pygame.font.init()

TEXT_COLOUR = (255, 255, 255)
WIDTH, HEIGHT = spaceship_shooters.WIDTH, spaceship_shooters.HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Spaceship Shooters!")


def main_menu():
    run = True
    title_font = pygame.font.SysFont("arial", 40)
    while run:
        WIN.blit(spaceship_shooters.BG, (0, 0))

        title_label = title_font.render(
            "Welcome to Spaceship Shooters!", 1, TEXT_COLOUR)
        middle = round(WIDTH / 2 - title_label.get_width() / 2)
        WIN.blit(title_label, (middle, 200))

        click_label = title_font.render(
            "To begin the game, simply left click.", 1, TEXT_COLOUR)
        middle = round(WIDTH / 2 - click_label.get_width() / 2)
        WIN.blit(click_label, (middle, 300))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                spaceship_shooters.game_loop(WIN)
    pygame.quit()


if __name__ == "__main__":
    main_menu()
