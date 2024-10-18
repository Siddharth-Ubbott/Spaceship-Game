import pygame
import sys
import random

class Spaceship:
    def __init__(self, x, y, speed):  
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < screen_height:
            self.rect.y += self.speed

class Bullet:
    def __init__(self, x, y, bullet_image):  
        self.image = pygame.transform.scale(bullet_image, (10, 20))  
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Enemy:
    def __init__(self, screen_width, speed, use_image=True):  
        if use_image:
            self.image = pygame.image.load("enemy.png")
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0, screen_width - self.rect.width), 0)
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


def main():
    
    pygame.init()

    screen_width, screen_height = 1280, 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Spaceship Game")

   
    background_image = pygame.image.load("background.png")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    
    bullet_image = pygame.image.load("bullet.png")

    
    clock = pygame.time.Clock()

   
    font = pygame.font.Font(None, 36)
    game_over_font = pygame.font.Font(None, 72)

    def reset_game():
        
        spaceship_speed = 7
        spaceship = Spaceship(screen_width // 2, screen_height - 50, spaceship_speed)
        bullets = []
        enemies = [Enemy(screen_width, 2, use_image=True)]
        score = 0
        enemy_speed = 2
        return spaceship, bullets, enemies, score, enemy_speed, spaceship_speed

    spaceship, bullets, enemies, score, enemy_speed, spaceship_speed = reset_game()
    game_over = False

    background_y1 = 0
    background_y2 = -screen_height

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.KEYDOWN:
                spaceship, bullets, enemies, score, enemy_speed, spaceship_speed = reset_game()
                game_over = False
            if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.append(Bullet(spaceship.rect.centerx, spaceship.rect.top, bullet_image))

        if not game_over:
            keys = pygame.key.get_pressed()
            spaceship.move(keys, screen_width, screen_height)

            for bullet in bullets[:]:
                bullet.move()
                if bullet.rect.bottom < 0:
                    bullets.remove(bullet)

            for enemy in enemies[:]:
                enemy.move()
                if enemy.rect.top > screen_height:
                    game_over = True  
                if spaceship.rect.colliderect(enemy.rect):
                    game_over = True  
                for bullet in bullets:
                    if bullet.rect.colliderect(enemy.rect):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 1  
                        if score % 10 == 0:  
                            enemy_speed += 1
                            spaceship_speed += 1
                            spaceship.speed = spaceship_speed
                        break

            if random.random() < 0.01:  
                enemies.append(Enemy(screen_width, enemy_speed, use_image=True))

            background_y1 += 7
            background_y2 += 7

            if background_y1 >= screen_height:
                background_y1 = -screen_height
            if background_y2 >= screen_height:
                background_y2 = -screen_height

            screen.blit(background_image, (0, background_y1))
            screen.blit(background_image, (0, background_y2))

            spaceship.draw(screen)

            for bullet in bullets:
                bullet.draw(screen)

            for enemy in enemies:
                enemy.draw(screen)

            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

        else:
            
            game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))

            restart_text = font.render("Press any key to restart", True, (255, 255, 255))
            screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + game_over_text.get_height()))

       
        pygame.display.flip()

       
        clock.tick(60)

if __name__ == "__main__":  
    main()
