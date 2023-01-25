import pygame.font


class Scoreboard:
    """显示得分信息的类"""
    def __init__(self, ai_game):
        """初始化得分涉及的属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (0, 60, 60)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """将得分转化为一幅渲染的图像"""
        rounded_score = round(self.stats.score, -1)
        score_str = 'SCORE ' + '{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转化为一幅渲染的图像"""
        rounded_score = round(self.stats.high_score, -1)
        high_score_str = 'HIGH SCORE ' + '{:,}'.format(rounded_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        # 在屏幕右上角显示得分
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转化为一幅渲染的图像"""
        level_str = 'LEVEL ' + '{:,}'.format(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        # 在屏幕右上角显示得分
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def check_high_score(self):
        """更新最高分"""
        if self.stats.score >= self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """显示得分板"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)