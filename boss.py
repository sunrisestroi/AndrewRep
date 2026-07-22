import pygame
from pygame.sprite import Sprite


class Boss(Sprite):
    """Класс, представляющий одного босса 👾."""

    def __init__(self, ai_game):
        """Инициализирует босса и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загрузка изображения босса
        self.image = pygame.image.load('images/boss.bmp')  # Убедись, что картинка лежит по этому пути
        self.rect = self.image.get_rect()

        # Позиционирование по центру вверху
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.top
        self.x = float(self.rect.x)

        # Здоровье и скорость из настроек
        self.hp = self.settings.boss_hp
        self.speed = self.settings.boss_speed

    def update(self):
        """Перемещает босса влево или вправо."""
        screen_rect = self.screen.get_rect()

        # Если задели край экрана — меняем направление
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            self.speed *= -1

        self.x += self.speed
        self.rect.x = self.x