class Settings:
    """Класс для хранения всех настроек"""
    def __init__(self):
        """Инициализирует настройки"""
        #Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Параметры снаряда
        self.bullet_speed = 10.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 4

        #Настройки корабля
        self.ship_speed = 3.0

        #Настройка пришелица
        self.aliens_speed = 2.0
        self.fleet_drop_speed = 10
        #fleet_direction = 1 Обозночает движение вправо, а -1 влево
        self.fleet_direction = 1