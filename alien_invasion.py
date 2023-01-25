import sys
from time import sleep

import pygame
import json

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和文件的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.rect = self.screen.get_rect()
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_height = self.screen.get_rect().height
        # self.settings.screen_width = self.screen.get_rect().width
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, 'Play')
        # 从文本文件读取最高分
        self.read_high_score()
        # 初始化得分板
        self.sb = Scoreboard(self)

        # 音乐初始化
        self.fire_sound = pygame.mixer.Sound('./audio/bulletflyby.mp3')
        self.explosion_sound = pygame.mixer.Sound('./audio/explosion.mp3')
        pygame.mixer.music.load('./audio/battle.wav')

        # 显示标题
        pygame.display.set_caption('Alien Invasion')

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def read_high_score(self):
        try:
            with open('high_score.json') as f:
                self.stats.high_score = json.load(f)
        except FileNotFoundError:
            pass

    def save_high_score(self):
        with open('high_score.json', 'w') as f:
            json.dump(self.stats.high_score, f)

    def _check_events(self):
        """监视键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """玩家单击Play按钮后开始游戏"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            # 重置游戏数据
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.settings.initialize_dynamic_settings()

            # 激活游戏
            self.stats.game_active = True

            # 清空编组
            self.aliens.empty()
            self.bullets.empty()

            # 创建外星人舰队和飞船
            self._create_fleet()
            self.ship.center_ship()

            # 显示鼠标
            pygame.mouse.set_visible(False)

            # 循环播放背景音效
            pygame.mixer.music.play(-1)

    def _check_keyup_events(self, event):
        """响应按键松开"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _check_keydown_events(self, event):
        """响应按键按下"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            self.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """创建新子弹并加入编组bullets中"""
        if self.stats.game_active and len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.fire_sound.play()

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= self.screen.get_rect().top:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """处理碰撞"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            # 每个外星人只会被一颗子弹击中
            for aliens_list in collisions.values():
                self.stats.score += len(aliens_list) * self.settings.alien_score
                self.sb.prep_score()
                self.sb.check_high_score()
                self.explosion_sound.play()

        # 消灭后创建新的外星人舰队
        if not self.aliens:
            self.start_new_level()

    def start_new_level(self):
        """消灭后创建新的外星人舰队"""
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()

    def _update_aliens(self):
        """更新外星群中所有外星人的位置"""
        self._check_fleet_edge()
        self.aliens.update()
        self._check_alien_ship_collisions()
        self._check_aliens_hit_bottom()

    def _check_alien_ship_collisions(self):
        """外星人与飞船相撞"""
        collisions = pygame.sprite.spritecollideany(self.ship, self.aliens)
        if collisions:
            self._ship_hit()

    def _check_aliens_hit_bottom(self):
        """外星人碰到屏幕底端"""
        for alien in self.aliens:
            if alien.rect.bottom >= self.rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ship_left > 0:
            # 飞船数量减少1
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # 清空子弹和外星人
            self.bullets.empty()
            self.aliens.empty()

            # 初始化外星人舰队和飞船
            self._create_fleet()
            self.ship.center_ship()

            # 画面暂停0.5s
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mixer.music.stop()
            pygame.mouse.set_visible(True)

    def _check_fleet_edge(self):
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens:
            alien.y += self.settings.fleet_drop_speed
            alien.rect.y = alien.y
        self.settings.fleet_direction *= -1

    def _create_alien(self, alien_number, row_number):
        # 创建一个外星人并放在当前行
        alien = Alien(self)
        alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
        alien.y = alien.rect.height + 2 * alien.rect.height * row_number - 7 * alien.rect.height
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算一行可容纳多少外星人
        # 外星人间距为外星人宽度
        new_alien = Alien(self)
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
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if self.stats.game_active:
            # 子弹没有 image 不能用精灵绘制
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
        else:
            self.play_button.draw_button()
        # 最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
