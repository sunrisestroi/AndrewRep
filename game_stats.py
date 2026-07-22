from pathlib import Path

class GameStats:
    #Отслеживает статистику
    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = self._get_saved_high_score()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _get_saved_high_score(self):
        """Считывает рекорд из файла, если он существует."""
        path = Path('high_score.txt')
        if path.exists():
            try:
                return int(path.read_text())
            except ValueError:
                return 0
        return 0