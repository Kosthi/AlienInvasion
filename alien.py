import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图形并设置其rect属性
        self.image = pygame.image.load('./images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初出现在左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人精确水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.settings.fleet_direction * self.settings.alien_speed
        self.rect.x = self.x

    def check_edge(self):
        """如果外星人处于屏幕边缘，返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= screen_rect.left:
            return True
