import random
import os
import pygame

pygame.font.init()

# LOAD ASSETS----------------------------------------------------------------------------------------------------------------------------------------------
# ships
RED_SHIP = pygame.image.load(os.path.join(
    "assets", "pixel_ship_red_small.png"))
GREEN_SHIP = pygame.image.load(os.path.join(
    "assets", "pixel_ship_green_small.png"))
BLUE_SHIP = pygame.image.load(os.path.join(
    "assets", "pixel_ship_blue_small.png"))
# player
YELLOW_SHIP = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow.png"))
# lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))
# Background
BG = pygame.image.load(os.path.join("assets", "background-space.png"))


# CLASSES-------------------------------------------------------------------------------------------------------------------------------------------------
class Laser():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y < height and self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)


class Ship():
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
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
        if self.cooldown_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            lasers.append(laser)
            self.cooldown_counter = 1


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x,
                                               self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_height(), 10
                                               ))

        pygame.draw.rect(window, (0, 255, 0), (self.x,
                                               round(
                                                   self.y + self.ship_img.get_height() + 10),
                                               round(self.ship_img.get_height(
                                               ) * (self.health / self.max_health)),
                                               10
                                               ))


class Enemy(Ship):
    COLOUR_MAP = {
        "red": (RED_SHIP, RED_LASER),
        "blue": (BLUE_SHIP, BLUE_LASER),
        "green": (GREEN_SHIP, GREEN_LASER)
    }

    def __init__(self, x, y, colour, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOUR_MAP[colour]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self, enemy_lasers):
        OFFSET = 20
        if self.cooldown_counter == 0:
            laser = Laser(self.x - OFFSET, self.y, self.laser_img)
            enemy_lasers.append(laser)
            self.cooldown_counter = 1


# FUNCTIONS------------------------------------------------------------------------------------------------------------------------------------------
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return not obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is None


def move_enemy_lasers(enemy_lasers, vel, height, player_ship):
    for laser in enemy_lasers:
        laser.move(vel)
        if laser.off_screen(height):
            enemy_lasers.remove(laser)
        elif laser.collision(player_ship):
            player_ship.health -= 10
            enemy_lasers.remove(laser)


def move_player_lasers(player_lasers, vel, height, player_ship, enemies):
    for laser in player_lasers:
        laser.move(vel)

        if laser.off_screen(height):
            player_lasers.remove(laser)

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
    FPS = 60
    level = 0
    lives = 5
    player_vel = 5
    laser_vel = 7

    main_font = pygame.font.SysFont("arial", 30)
    lost_font = pygame.font.SysFont("arial", 50)

    enemies = []
    wave_length = 0
    enemy_vel = 1

    player_ship = Player(300, 630)

    player_lasers = []
    enemy_lasers = []

    clock = pygame.time.Clock()

    # Called every frame to redraw objects
    def redraw_window(window):
        window.blit(BG, (0, 0))
        # Draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        window.blit(lives_label, (10, 10))
        window.blit(level_label, (width - 10 - level_label.get_width(), 10))

        for enemy in enemies:
            enemy.draw(window)

        player_ship.draw(window)

        for laser in enemy_lasers:
            laser.draw(window)

        for laser in player_lasers:
            laser.draw(window)

        if lost:
            lost_label = lost_font.render("You lost!", 1, (255, 255, 255))

            window.blit(lost_label,
                        round(width / 2 - lost_label.get_width() / 2, 350)
                        )

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window(window)

        if lives <= 0 or player_ship.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 3
            for i in range(wave_length):
                enemy = Enemy(random.randrange(
                    50, width - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        # Movement
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

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot(enemy_lasers)

            if collide(enemy, player_ship):
                player_ship.health -= 10
                enemies.remove(enemy)

            if enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)

        player_ship.cooldown()

        move_enemy_lasers(enemy_lasers, laser_vel, height, player_ship)
        move_player_lasers(player_lasers, -laser_vel,
                           height, player_ship, enemies)
