from pathlib import Path
import json

class GameStats:
    #Отслеживает статистику
    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Загружаем сохраненные рекорды при старте
        self.high_scores = self.load_high_scores()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_scores(self):
        """Загружает список рекордов из файла или создает пустой."""
        try:
            with open("high_scores.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_high_scores(self):
        """Сохраняет список рекордов в файл."""
        with open("high_scores.json", "w") as file:
            json.dump(self.high_scores, file, indent=4)

    def add_high_score(self, name, score):
        """Добавляет новый результат, сортирует и оставляет топ-5."""
        new_record = {"name": name, "score": score}
        self.high_scores.append(new_record)

        # Сортируем от большего к меньшему
        self.high_scores.sort(key=lambda item: item["score"], reverse=True)

        # Оставляем только 5 лучших результатов
        self.high_scores = self.high_scores[:5]

        self.save_high_scores()