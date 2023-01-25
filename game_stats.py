class GameStats:
    """跟踪游戏的统计信息"""
    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()
        # 游戏启动时处于活跃模式
        self.game_active = False
        self.high_score = 0
        self.level = 1


    def reset_stats(self):
        """重置统计信息"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
