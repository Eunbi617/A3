"""
A3 BounceGame by Eunbi Lim
Creative Element:
- Background color changes depending on player's life.
- Green when life is high, red when life is low.
- Provides visual feedback of health status.
"""

import pygame, sys, random

class Sprite:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, other_sprite):
        offset_x = other_sprite.rect.x - self.rect.x
        offset_y = other_sprite.rect.y - self.rect.y
        return self.mask.overlap(other_sprite.mask, (offset_x, offset_y)) is not None

class Player(Sprite):
    def __init__(self, image):
        super().__init__(image)

    def set_position(self, pos):
        self.rect.center = pos

# Random positioning, random speed, bounce off the screen wall
class Enemy(Sprite):
    def __init__(self, image, screen_width, screen_height):
        super().__init__(image)
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        self.speed = [random.choice([-3, 3]), random.choice([-3, 3])]

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def bounce(self, screen_width, screen_height):
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.speed[1] = -self.speed[1]

# Random screen appearing, don't move
class PowerUp(Sprite):
    def __init__(self, image, screen_width, screen_height):
        x = random.randint(50, screen_width - 50)
        y = random.randint(50, screen_height - 50)
        super().__init__(image)
        self.rect.center = (x, y)

class PlatformEnemy(Enemy):
    def __init__(self, image, screen_width, screen_height):
        super().__init__(image, screen_width, screen_height)
        self.speed[1] = 0

class RotatingPowerUp(PowerUp):
    def __init__(self, image_file, screen_width, screen_height):
        super().__init__(image_file, screen_width, screen_height)
        self.angle = 0
        self.original_image = self.image

    def draw(self, screen):
        self.angle += 5
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.image = rotated_image
        self.rect = self.image.get_rect(center=old_center)
        self.mask = pygame.mask.from_surface(self.image)
        super().draw(screen)


def main():
    # Setup pygame
    pygame.init()

    # Define the screen
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Avoider Game A4 - Eunbi Lim")

    myfont = pygame.font.SysFont('monospace', 24)

    # Load image assets
    enemy_image = pygame.image.load("enemy.png").convert_alpha()
    enemy_image = pygame.transform.smoothscale(enemy_image, (50, 50))

    # This is the character you control. Choose your image.
    player_image = pygame.image.load("wizard.png").convert_alpha()
    player_sprite = Player(player_image)

    # This is the powerup image. Choose your image.
    heart_image = pygame.image.load("heart.png").convert_alpha()
    heart_image = pygame.transform.smoothscale(heart_image, (50, 50))
    # Start with an empty list of powerups and add them as the game runs.
    powerups = [PowerUp(heart_image, width, height), RotatingPowerUp(heart_image, width, height)]

    enemy_sprites = [Enemy(enemy_image, width, height) for _ in range(5)]
    enemy_sprites.append(PlatformEnemy(enemy_image, width, height))

    life = 3
    clock = pygame.time.Clock()
    is_playing = True

    # while loop
    while is_playing:# while is_playing is True, repeat
    # Modify the loop to stop when life is <= to 0.

        # Check for events
        for event in pygame.event.get():
            # Stop loop if click on window close button
            if event.type == pygame.QUIT:
                is_playing = False

        player_sprite.set_position(pygame.mouse.get_pos())

        for powerup in powerups:
            if player_sprite.check_collision(powerup):
                life = min(life + 1, 3)

        powerups = [p for p in powerups if not player_sprite.check_collision(p)]

        if random.randint(1, 100) == 1:
            if random.random() < 0.5:
                powerups.append(PowerUp(heart_image, width, height))
            else:
                powerups.append(RotatingPowerUp(heart_image, width, height))

        for enemy in enemy_sprites:
            enemy.move()
            enemy.bounce(width, height)

            if player_sprite.check_collision(enemy):
                life -= 0.1
                if life <= 0:
                    life = 0
                    is_playing = False

        # My creative element
        life_clamped = max(0, min(3, life))
        red = int((1 - (life_clamped / 3)) * 150)
        green = int((life_clamped / 3) * 150)
        blue = 50
        background_color = (red, green, blue)

        screen.fill(background_color)


        # Draw the characters
        for enemy in enemy_sprites:
            enemy.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)

        player_sprite.draw(screen)

        # Write the life to the screen.
        text = f"Life: {life:.1f}"
        life_banner = myfont.render(text, True, (255, 255, 0))
        screen.blit(life_banner, (20, 20))

        # Bring all the changes to the screen into view
        pygame.display.update()
        # Pause for a few milliseconds
        clock.tick(60)

    # Once the game loop is done, pause, close the window and quit.
    # Pause for a few seconds
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
