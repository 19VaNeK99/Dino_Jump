import random
import pygame
import sprites


class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Dino Jump')

        self.high_score = 0
        self.big_font = pygame.freetype.Font('Font.ttf', 75)
        self.middle_font = pygame.freetype.Font('Font.ttf', 40)
        self.small_font = pygame.freetype.Font('Font.ttf', 25)
        self.on_ground = True
        self.speed = 0
        self.player = None
        self.menu()
        pygame.quit()

    def draw_menu_header(self):
        text_surface, rect = self.big_font.render('Dino Jump', (0, 0, 0))
        self.screen.blit(text_surface, (300, 200))

        text_surface, rect = self.small_font.render(f'Highscore: {self.high_score}', (0, 0, 0))
        self.screen.blit(
            text_surface,
            (
                (self.screen.get_rect().w - rect.w) / 2,
                300,
            ),
        )

    def draw_overlay(self):
        pygame.draw.rect(self.screen, (2, 94, 115), (0, 0, 150, 800), 0)
        pygame.draw.rect(self.screen, (2, 94, 115), (650, 0, 150, 800), 0)
        pygame.draw.rect(self.screen, (1, 31, 38), (0, 0, 150, 800), 10)
        pygame.draw.rect(self.screen, (1, 31, 38), (650, 0, 150, 800), 10)

    def menu(self):

        play_button = sprites.Button(400, 540, 'Play', self.middle_font)
        menu_run = True
        while menu_run:

            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.be_inside(pos[0], pos[1]):
                        menu_run = self.game()

            play_button.update(pos[0], pos[1])

            self.screen.fill((165, 166, 146))
            self.draw_overlay()
            self.draw_menu_header()
            self.screen.blit(play_button.image, play_button.rect)
            pygame.display.flip()

            self.clock.tick(20)

    def draw_result(self, score):
        text_surface, rect = self.small_font.render(f'Score: {score}', (0, 0, 0))
        self.screen.blit(text_surface, (20, 50))

    def boundaries(self, platforms):

        for platform in platforms.sprites():
            if (
                    self.player.rect.right >= platform.rect.left and
                    self.player.rect.left <= platform.rect.right and
                    platform.rect.bottom >= self.player.rect.bottom >= platform.rect.top
            ):
                if self.speed >= 0:
                    self.speed = 0
                    self.on_ground = True
        if not self.on_ground:
            self.speed += 1

    def game(self):

        game_run = True
        power = 10
        next_level = 10

        self.player = sprites.Sprite(400, 500, 50, 50, 'player.png')
        score = 0

        platforms = pygame.sprite.Group(
            [sprites.Sprite(random.randint(230, 550), (i * 100) + 100, 200, 20, 'platform.png') for i in range(10)]
        )
        upper_platform = platforms.sprites()[0]

        self.speed = 0
        self.on_ground = True
        fail = False

        while game_run:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.rect.x -= 5

            if keys[pygame.K_d]:
                self.player.rect.x += 5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_run = False

            if self.on_ground:
                self.speed = -power
                self.on_ground = False

            self.player.rect.y += self.speed

            if upper_platform.rect.y > power * 10:
                upper_platform = sprites.Sprite(random.randint(230, 550), 0, 200, 20, 'platform.png')
                platforms.add(upper_platform)

            for platform in platforms.sprites():
                if self.speed < 0:
                    if self.player.rect.y < 300:
                        platform.rect.y -= self.speed * 2
                    platform.rect.y -= self.speed
                if platform.rect.y >= 820:
                    platform.kill()
                    score += 1

            self.screen.fill((165, 166, 146))
            self.draw_overlay()
            self.draw_result(score)
            self.screen.blit(self.player.image, self.player.rect)
            platforms.draw(self.screen)
            self.boundaries(platforms)

            if self.player.rect.y >= 820:
                if score > self.high_score:
                    self.high_score = score
                game_run = False
                fail = True

            if score > next_level:
                next_level += 10
                power += 1

            pygame.display.flip()
            self.clock.tick(60)

        return fail


Game()
