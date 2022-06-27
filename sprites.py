import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(filename), (width, height))
        self.rect = self.image.get_rect(center=(x, y))


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font):
        pygame.sprite.Sprite.__init__(self)
        self.text_surf, self.text_rect = font.render(text, (0, 0, 0))
        self.image = pygame.Surface((self.text_rect.width*1.5, self.text_rect.height*1.5))
        self.image.fill((242, 165, 22))
        self.blit_text()

        self.rect = self.image.get_rect(center=(x, y))

    def blit_text(self):
        self.image.blit(
            self.text_surf,
            (
                (self.image.get_rect().w - self.text_rect.w) / 2,
                (self.image.get_rect().h - self.text_rect.h) / 2,
            ),
        )

    def be_inside(self, x, y):
        if self.rect.x < x < self.rect.right and self.rect.y < y < self.rect.bottom:
            return True
        else:
            return False

    def update(self, mouse_x, mouse_y):
        if self.be_inside(mouse_x, mouse_y):
            self.image.fill((222, 125, 18))
            self.blit_text()
        else:
            self.image.fill((242, 165, 22))
            self.blit_text()
