class Settings:
    """Класс для хранения всех настроек"""
    def __init__(self):
        """Инициализирует статические настройки"""
        #Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (150, 150, 150)

        #Параметры снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (220, 220, 220)
        self.bullets_allowed = 4

        #Настройки корабля
        self.ship_limit = 3

        #Настройка пришелица
        self.fleet_drop_speed = 30

        # Настройки босса
        self.boss_hp = 10
        self.boss_speed = 5.0
        
        #Темп ускорения игры
        self.speedup_scale = 1.1
        #Темп роста очков за пришельца
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 4.0
        self.bullet_speed = 20.0
        self.aliens_speed = 1.5
        #fleet_direction = 1 Обозночает движение вправо, а -1 влево
        self.fleet_direction = 1
        #Подсчет очков
        self.aliens_points = 50

    def increase_speed(self):
        #Увеличивает настройки скорости и стоймость пришельцев
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.aliens_speed *= self.speedup_scale
        self.aliens_points *= self.speedup_scale