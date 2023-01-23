import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """管理游戏资源和文件的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        #self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        pygame.display.set_caption('Alien Invasion')
    
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._create_fleet()
            self._update_screen()
    
    def _check_events(self):
        """监视键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                    
    def _check_keyup_events(self, event):
        """响应按键"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            
    def _check_keydown_events(self, event):
        """响应松开"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _fire_bullet(self):
        """创建新子弹并加入编组bullets中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= self.screen.get_rect().top:
                self.bullets.remove(bullet)
                
    def _create_alien(self, alien_number, row_number):
        # 创建一个外星人并放在当前行
        alien = Alien(self)
        alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
        alien.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)
        
    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算一行可容纳多少外星人
        # 外星人间距为外星人宽度
        new_alien = Alien(self)
        self.aliens.add(new_alien)
        alien_width = new_alien.rect.width
        alien_height = new_alien.rect.height
        
        available_space_x = self.settings.screen_width - (2 * alien_width)
        available_space_y = self.settings.screen_height - (3 * alien_height) - self.ship.rect.height
        
        numbers_alien_x = available_space_x // (2 * alien_width)
        numbers_alien_y = available_space_y // (2 * alien_height)
        
        # 创建外星人群
        for row_number in range(numbers_alien_y):
            # 创建第row_number行外星人
            for alien_number in range(numbers_alien_x):
                self._create_alien(alien_number, row_number)
            
    def _update_screen(self):
        """每次循环都重绘屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # 最近绘制的屏幕可见
        pygame.display.flip()
        
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()