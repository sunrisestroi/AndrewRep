import sys
from time import sleep
import pygame


from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullets import Bullets
from alien import Alien
from button import Button
from scoreboard import Scoreboard
from boss import Boss

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        #Создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.boss_group = pygame.sprite.Group()
        self._create_fleet()

        #Игра запускается в активном состоянии
        self.game_active = True
        self.game_active = False
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Запускает основной цикл игры"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Обрабатывает события клавиатуры и мышки"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #Сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            #Сброс игровой статистики
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            #Очистка групп Aliens и bullets
            self.bullets.empty()
            self.aliens.empty()
            #Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()
            #Указатель мыши скрывается
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False

    def _fire_bullet(self):
        """Создает снаряд и добавляет его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullets(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        # Удаление снарядов улетевших за экран
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # 1. Попадания в обычных пришельцев 👾
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.aliens_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # 2. Попадания в босса 👹
        boss_collisions = pygame.sprite.groupcollide(self.bullets, self.boss_group, True, False)
        if boss_collisions:
            for bosses in boss_collisions.values():
                for boss in bosses:
                    boss.hp -= 1
                    if boss.hp <= 0:
                        boss.kill()

        # 3. Проверка: победили ли мы всех врагов? 🏆
        if not self.aliens and not self.boss_group:
            self.bullets.empty()
            self.stats.level += 1
            self.sb.prep_level()  # Обновляем отображение уровня
            self.settings.increase_speed()  # Увеличиваем скорость и очки! 🚀

            # Спавним босса на 10-м уровне или обычную армаду
            if self.stats.level == 10:
                self._create_boss()
            else:
                self._create_fleet()



    def _update_aliens(self):
        #Проверяет, достиг ли флот конца экрана
        self._check_fleet_edges()
        self.aliens.update()

        #Проверка коллизий пришелец - корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Сталкиваются ли пришельцы с нижним краем экрана
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Создает флот пришельцев"""
        #Создание пришельца и добавление других, пока остается место
        #Интервал между соседями пришельцами равен ширине пришельца
        #Интервал между соседями пришельцами равен высоте пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self.create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_boss(self):
        """Создаёт одного босса и добавляет его в группу."""
        boss = Boss(self)
        self.boss_group.add(boss)

    def create_alien(self, x_position, y_position):
        #Создает пришельца и размещает его во флот
            new_alien = Alien(self)
            new_alien.x = x_position
            new_alien.rect.x = x_position
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)
    def _check_fleet_edges(self):
        #Реагирует на достижение пришельцем края экрана
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        #Опускает флот вниз и меняет его направление
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ships_left > 0:
            #уменьшение ships_left и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Очистка групп aliens bullets
            self.aliens.empty()
            self.bullets.empty()
            #Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()
            #Пауза
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        #Проверяет добрались ли пришельцы до нижнего края экрана
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _update_screen(self):
            """При каждом проходе цикла перерисовывается экран"""
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()
            self.aliens.draw(self.screen)
            self.boss_group.draw(self.screen)
            self.boss_group.update()

            #Выводит информацию о счете
            self.sb.show_score()

            #Кнопка Play отображается в том случае, если игра не активна
            if not self.game_active:
                self.play_button.draw_button()

            pygame.display.flip()

if __name__ == '__main__':
    #Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()