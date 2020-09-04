import random
import os
import pygame

# Initialise pygame font, for making labels
pygame.font.init()

# LOAD ASSETS----------------------------------------------------------------------------------------------------------------------------------------------
# ships
RED_SHIP = pygame.image.load(os.path.join("assets",
                                          "pixel_ship_red_small.png"
                                          ))
GREEN_SHIP = pygame.image.load(os.path.join("assets",
                                            "pixel_ship_green_small.png"
                                            ))
BLUE_SHIP = pygame.image.load(os.path.join("assets",
                                           "pixel_ship_blue_small.png"
                                           ))
# player
YELLOW_SHIP = pygame.image.load(os.path.join("assets",
                                             "pixel_ship_yellow.png"
                                             ))
# lasers
RED_LASER = pygame.image.load(os.path.join("assets",
                                           "pixel_laser_red.png"
                                           ))
GREEN_LASER = pygame.image.load(os.path.join("assets",
                                             "pixel_laser_green.png"
                                             ))
BLUE_LASER = pygame.image.load(os.path.join("assets",
                                            "pixel_laser_blue.png"
                                            ))
YELLOW_LASER = pygame.image.load(os.path.join("assets",
                                              "pixel_laser_yellow.png"
                                              ))
# Background
BG = pygame.image.load(os.path.join("assets",
                                    "background-space.png"
                                    ))

# CLASSES-------------------------------------------------------------------------------------------------------------------------------------------------


class Laser():
    """Lasers shot by both the player and by enemy ships"""

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        # img (surface) is given by either the enemy or the player when the laser object is instantiated
        self.img = img
        # mask defined for collisions
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        """Returns wether the laser if off screen"""

        return not(self.y < height and self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)


class Ship():
    """Class to be inherited by both Enemy and Player"""

    # Define cooldown so that ships can't shoot more than once every 0.5 seconds (at 60fps)
    COOLDOWN = 30

    # Default value for health given but if you want to change this, leave it as a multiple of 10
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        # ship and laser images are given by the Player and Enemy classes
        self.ship_img = None
        self.laser_img = None
        self.cooldown_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def shoot(self, lasers):
        """Makes an instance of the laser class which will be stored in a list, but only if the cooldown is 0"""
        if self.cooldown_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            lasers.append(laser)
            # start the cooldown
            self.cooldown_counter = 1


class Player(Ship):
    """Defines the player_ship object. Inherits from Ship"""

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LASER
        # Mask defined for collisions
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        """Health bar for the player, achived via a red label under a green label which shrinks in size with player health"""

        # Red rectangle
        pygame.draw.rect(window, (255, 0, 0), (self.x,
                                               self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_height(), 10
                                               ))

        # Green rectangle
        pygame.draw.rect(window, (0, 255, 0), (self.x,
                                               round(
                                                   self.y + self.ship_img.get_height() + 10),
                                               round(self.ship_img.get_height(
                                               ) * (self.health / self.max_health)),
                                               10
                                               ))


class Enemy(Ship):
    """Defines all enemy ships spawned, inherits from Ship"""

    # Colour map defined so that enemies can vary in ship and laser colour, given when an enemy is instantiated
    COLOUR_MAP = {
        "red": (RED_SHIP, RED_LASER),
        "blue": (BLUE_SHIP, BLUE_LASER),
        "green": (GREEN_SHIP, GREEN_LASER)
    }

    def __init__(self, x, y, colour, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOUR_MAP[colour]
        # Mask defined for collisions
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self, enemy_lasers):
        # Offset given because lasers will be spawned on the x of the enemy, but some enemy ships are wide so the laser would shoot
        # from the left side of the enemy ship, so the offset helps to bring it more centre for most ships
        offset = self.get_width() // 2 - self.laser_img.get_width() // 2
        if self.cooldown_counter == 0:
            laser = Laser(self.x + offset, self.y, self.laser_img)
            enemy_lasers.append(laser)
            self.cooldown_counter = 1


# FUNCTIONS------------------------------------------------------------------------------------------------------------------------------------------

def collide(obj1, obj2):
    """Returns boolean value based on wether the masks of 2 objects overlap, done using the overlap function from pygame.mask"""

    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # Could just return the expression without not xxx is None but this allows for easier use outside of
    # this function in an if statement, i.e. if collide(): then despawn objects
    return not obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is None


# Functions for moving lasers defined outside of the classes because to make the lasers independent from the enemy objects,
# they had to be stored in lists
def move_enemy_lasers(enemy_lasers, vel, height, player_ship):
    for laser in enemy_lasers:
        laser.move(vel)
        # Despawns laser if it is off the screen
        if laser.off_screen(height):
            enemy_lasers.remove(laser)
        # Despawns the laser and removes player health if they collided
        elif laser.collision(player_ship):
            player_ship.health -= 10
            enemy_lasers.remove(laser)


def move_player_lasers(player_lasers, vel, height, player_ship, enemies):
    for laser in player_lasers:
        laser.move(vel)

        # Despawns laser if it is off the screen
        if laser.off_screen(height):
            player_lasers.remove(laser)
        else:
            # Check for collision with every enemy object
            for enemy in enemies:
                if laser.collision(enemy):
                    enemies.remove(enemy)
                    if laser in player_lasers:
                        player_lasers.remove(laser)


# MAIN-----------------------------------------------------------------------------------------------------------------------------------------------
def game_loop(window, width, height):
    run = True
    lost = False
    lost_count = 0
    # Changes to the fps will drastically affect the speeds of objects
    FPS = 60
    level = 0
    # How many enemies can reach the bottom of the screen before the game ends
    lives = 5
    # How many pixels the player moves per frame
    player_vel = 5
    # How many pixels each laser moves per frame
    laser_vel = 7

    main_font = pygame.font.SysFont("arial", 30)
    lost_font = pygame.font.SysFont("arial", 50)

    # To contain all enemy objects
    enemies = []
    # Defines how many enemies spwan each round, increased when all enemies are killed each round
    wave_length = 0
    # How many pixels each enemy moves per frame
    enemy_vel = 1

    # Instantiate player character
    player_ship = Player(300, 630)

    # To contain all lasers fired by the player
    player_lasers = []
    # To contain all lasers fired by the enemies
    enemy_lasers = []

    # Clock used to force the program to run at given fps, otherwise the program would run at different speeds
    # based on each computers processing speed
    clock = pygame.time.Clock()

    def redraw_window(window):
        """Called every frame to redraw objects"""

        # Show background
        window.blit(BG, (0, 0))
        # Draw text labels
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        window.blit(lives_label, (10, 10))
        window.blit(level_label, (width - 10 - level_label.get_width(), 10))

        # Draw enemies
        for enemy in enemies:
            enemy.draw(window)

        # Draw player ship
        player_ship.draw(window)

        # Draw enemy and player lasers
        for laser in enemy_lasers:
            laser.draw(window)

        for laser in player_lasers:
            laser.draw(window)

        # Displays lost label
        if lost:
            lost_label = lost_font.render("You lost!", 1, (255, 255, 255))

            window.blit(lost_label,
                        (width // 2 - lost_label.get_width() // 2, 350)
                        )

        # Updates the window so all changes are shown
        pygame.display.update()

    while run:
        # Forces loop to run FPS times per second
        clock.tick(FPS)
        redraw_window(window)

        # Player loses if health or lives reach 0
        if lives <= 0 or player_ship.health <= 0:
            lost = True
            lost_count += 1

        # Gives small pause after having lost before ending the loop, so lost label can display
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        # Goes to next level and increases how many enemies spawn each round after all enmies are killed
        if len(enemies) == 0:
            level += 1
            # Additional enemies to spawn next wave
            wave_length += 3
            for i in range(wave_length):
                # Spawns enemy at random x and y values, and with a random colour, so there are no patterns to be followed
                enemy = Enemy(random.randrange(
                    50, width - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # Allows program to be exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        # Movement, player moves with WASD
        if keys[pygame.K_a] and player_ship.x - player_vel > 0:  # left
            player_ship.x -= player_vel
        if keys[pygame.K_d] and player_ship.x + player_vel + player_ship.get_width() < width:  # right
            player_ship.x += player_vel
        if keys[pygame.K_w] and player_ship.y - player_vel > 0:  # up
            player_ship.y -= player_vel
        if keys[pygame.K_s] and player_ship.y + player_vel + player_ship.get_height() + 20 < height:  # down
            player_ship.y += player_vel
        if keys[pygame.K_SPACE]:
            player_ship.shoot(player_lasers)

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.cooldown()

            # Random chance for the enemy to shoot if the cooldown is 0
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot(enemy_lasers)

            # Despawns enemy if it collided with the player, but also removes 10 health from player
            if collide(enemy, player_ship):
                player_ship.health -= 10
                enemies.remove(enemy)

            # Removes 1 life from player if enemy reaches the bottom of the screen, then despawns the enemy
            if enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)

        player_ship.cooldown()

        # Move lasers
        move_enemy_lasers(enemy_lasers, laser_vel, height, player_ship)
        move_player_lasers(player_lasers, -laser_vel,
                           height, player_ship, enemies)
