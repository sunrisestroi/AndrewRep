class Settings:
    """Класс для хранения всех настроек"""
    def __init__(self):
        """Инициализирует статические настройки"""
        #Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (50, 70, 100)

        #Параметры снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (220, 220, 220)
        self.bullets_allowed = 4

        #Настройки корабля
        self.ship_limit = 3

        #Настройка пришелица
        self.fleet_drop_speed = 35

        #Темп ускорения игры
        self.speedup_scale = 1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 4.0
        self.bullet_speed = 20.0
        self.aliens_speed = 2.0
        #fleet_direction = 1 Обозночает движение вправо, а -1 влево
        self.fleet_direction = 1

    def increase_speed(self):
        #Увеличивает настройки скорости
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.aliens_speed *= self.speedup_scale