class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船设置
        self.ship_limit = 3
        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 50
        # 外星人设置
        self.fleet_drop_speed = 20
        # 加快游戏节奏
        self.speedup_scale = 1.1
        # 提高分数
        self.score_scale = 1.5
        # 初始化动态设置
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化游戏的动态设置"""
        self.ship_speed = 5.0
        self.bullet_speed = 5.0
        self.alien_speed = 1.0
        self.alien_score = 50
        # 1为右 -1为左
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_score = int(self.score_scale * self.alien_score)
