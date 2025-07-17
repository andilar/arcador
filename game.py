import arcade
import random
from enemy import EnemyManager
from loot import LootManager, LaserUpgrade

laser_sound = arcade.load_sound("Laser.mp3")
background_music = arcade.load_sound("background.wav")

# Sterne-Einstellungen
STAR_COUNT = 100
STAR_SPEED_MIN = 1.0
STAR_SPEED_MAX = 3.0

class Star:
    def __init__(self):
        self.reset_position()
        self.speed = random.uniform(STAR_SPEED_MIN, STAR_SPEED_MAX)
        self.color = random.choice([
            arcade.color.WHITE,
            arcade.color.YELLOW,
            arcade.color.CYAN,
            arcade.color.LIGHT_BLUE,
            arcade.color.LIGHT_GRAY
        ])
        self.size = max(2, int(self.speed))
        if self.size > 4:
            self.size = 4
    
    def reset_position(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
    
    def update(self):
        self.y -= self.speed
        if self.y < -5:
            self.y = 800 + 5
            self.x = random.randint(0, 800)
    
    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color)
        if self.size >= 2:
            arcade.draw_circle_filled(self.x-2, self.y, 1, self.color)
            arcade.draw_circle_filled(self.x+2, self.y, 1, self.color)
            arcade.draw_circle_filled(self.x, self.y-2, 1, self.color)
            arcade.draw_circle_filled(self.x, self.y+2, 1, self.color)

class StarField:
    def __init__(self):
        self.stars = []
        for _ in range(STAR_COUNT):
            self.stars.append(Star())
    
    def update(self):
        for star in self.stars:
            star.update()
    
    def draw(self):
        for star in self.stars:
            star.draw()

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.setup_game()
        
    def setup_game(self):
        """Initialisiert/resettet alle Spielkomponenten"""
        # Spieler
        self.player_x = 400
        self.player_y = 30
        self.speed = 5
        
        # Laser
        self.lasers = []
        self.laser_speed = 8
        
        # Spielwelt
        self.starfield = StarField()
        self.enemy_manager = EnemyManager(800, 600)
        
        # Progression
        self.score = 0
        self.points_per_enemy = 10
        self.enemies_killed_count = 0
        
        # Loot-System
        self.loot_manager = LootManager()
        self.laser_upgrade = LaserUpgrade()
        
        # Loot-Manager mit Enemy-Manager verbinden
        if hasattr(self.enemy_manager, 'set_loot_manager'):
            self.enemy_manager.set_loot_manager(self.loot_manager)
        
        # Spiel-Status
        self.game_over = False
        self.player_explosion = None
        self.game_over_timer = 0
        
        # Eingabe
        self.keys_pressed = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        
    def on_draw(self):
        self.clear()
        
        # Hintergrund
        self.starfield.draw()
        
        # UI
        arcade.draw_text(f"PUNKTE: {self.score}", 20, 570, arcade.color.WHITE, 20, font_name="Kenney Blocks")
        arcade.draw_text(f"LASER: {self.laser_upgrade.laser_count}", 650, 570, arcade.color.CYAN, 20, font_name="Kenney Blocks")
        
        # Spieler
        if not self.game_over:
            arcade.draw_triangle_filled(
                self.player_x, self.player_y + 15,
                self.player_x - 15, self.player_y - 15,
                self.player_x + 15, self.player_y - 15,
                arcade.color.WHITE
            )
        
        # Laser
        for laser in self.lasers:
            arcade.draw_circle_filled(laser['x'], laser['y'], 3, arcade.color.RED)
            
        # Spielwelt
        self.enemy_manager.draw()
        self.loot_manager.draw()
        
        # Effekte
        if self.player_explosion:
            self.player_explosion.draw()
    
    def on_update(self, delta_time):
        # Immer aktualisieren
        self.starfield.update()
        self.loot_manager.update()
        
        if not self.game_over:
            self.update_player()
            self.update_lasers()
            self.update_enemies()
            self.check_collisions()
        else:
            self.update_game_over()
    
    def update_player(self):
        """Spieler-Update"""
        # Bewegung
        if self.keys_pressed['up']:
            self.player_y += self.speed
        if self.keys_pressed['down']:
            self.player_y -= self.speed
        if self.keys_pressed['left']:
            self.player_x -= self.speed
        if self.keys_pressed['right']:
            self.player_x += self.speed
        
        # Bildschirmgrenzen
        self.player_x = max(15, min(785, self.player_x))
        self.player_y = max(15, min(585, self.player_y))
    
    def update_lasers(self):
        """Laser-Update"""
        for laser in self.lasers[:]:
            laser['y'] += self.laser_speed
            if laser['y'] > 600:
                self.lasers.remove(laser)
    
    def update_enemies(self):
        """Gegner-Update"""
        self.enemy_manager.update()
        self.enemy_manager.set_score(self.score)
        
        # Gegnertypen aktivieren
        if self.score >= 200:
            self.enemy_manager.enable_green_enemies = True
        if self.score >= 2000:
            self.enemy_manager.enable_yellow_enemies = True
    
    def check_collisions(self):
        """Alle Kollisionen prüfen"""
        # Laser vs Gegner
        hit_results = self.enemy_manager.check_laser_collisions(self.lasers)
        for hit in hit_results:
            laser = hit.get('laser', hit)
            points = hit.get('points', self.points_per_enemy)
            
            if laser in self.lasers:
                self.lasers.remove(laser)
                self.score += points
                self.enemies_killed_count += 1
                
                # Loot spawnen
                if self.enemies_killed_count % 3 == 0:
                    self.spawn_loot(laser['x'], laser['y'])
        
        # Spieler vs Loot
        collected_stars = self.loot_manager.check_player_collisions(self.player_x, self.player_y)
        for _ in range(collected_stars):
            if self.laser_upgrade.upgrade():
                print(f"Laser-Upgrade! Jetzt {self.laser_upgrade.laser_count} Laser!")
        
        # Spieler vs Gegner
        self.check_player_enemy_collisions()
    
    def check_player_enemy_collisions(self):
        """Prüft Kollisionen zwischen Spieler und allen Gegnertypen"""
        enemy_lists = [
            self.enemy_manager.enemies,
            getattr(self.enemy_manager, 'green_enemies', []),
            getattr(self.enemy_manager, 'yellow_enemies', [])
        ]
        
        for enemy_list in enemy_lists:
            for enemy in enemy_list:
                if enemy.alive and self.check_player_collision(enemy):
                    self.player_dies()
                    return
    
    def spawn_loot(self, x, y):
        """Spawnt Loot an gegebener Position"""
        star_x = max(20, min(780, x + random.randint(-30, 30)))
        star_y = max(50, min(550, y + random.randint(-20, 20)))
        self.loot_manager.spawn_blue_star(star_x, star_y)
        print(f"Blauer Stern gespawnt! (Gegner #{self.enemies_killed_count})")
    
    def check_player_collision(self, enemy):
        """Prüft Kollision zwischen Spieler und Gegner"""
        distance = ((self.player_x - enemy.x) ** 2 + (self.player_y - enemy.y) ** 2) ** 0.5
        return distance < 20
    
    def player_dies(self):
        """Spieler stirbt"""
        from enemy import Explosion
        self.player_explosion = Explosion(self.player_x, self.player_y)
        self.game_over = True
        self.game_over_timer = 0
        
        # Nach kurzer Verzögerung zu Game Over Screen wechseln
        def show_game_over(delta_time):  # arcade.schedule übergibt delta_time
            from title import GameOverScreen
            game_over_view = GameOverScreen(self.score, self.laser_upgrade.laser_count)
            self.window.show_view(game_over_view)
            # Schedule nur einmal ausführen
            arcade.unschedule(show_game_over)
        
        # 2 Sekunden warten damit Explosion sichtbar ist
        arcade.schedule(show_game_over, 2.0)
    
    def update_game_over(self):
        """Game Over Update"""
        self.game_over_timer += 1
        if self.player_explosion:
            self.player_explosion.update()
            if self.player_explosion.is_finished():
                self.player_explosion = None
    
    def on_key_press(self, key, modifiers):
        if not self.game_over:
            # Bewegung
            if key == arcade.key.UP:
                self.keys_pressed['up'] = True
            elif key == arcade.key.DOWN:
                self.keys_pressed['down'] = True
            elif key == arcade.key.LEFT:
                self.keys_pressed['left'] = True
            elif key == arcade.key.RIGHT:
                self.keys_pressed['right'] = True
            # Schießen
            elif key == arcade.key.SPACE:
                new_lasers = self.laser_upgrade.create_lasers(self.player_x, self.player_y)
                self.lasers.extend(new_lasers)
                arcade.play_sound(laser_sound)
    
    def on_key_release(self, key, modifiers):
        if not self.game_over:
            if key == arcade.key.UP:
                self.keys_pressed['up'] = False
            elif key == arcade.key.DOWN:
                self.keys_pressed['down'] = False
            elif key == arcade.key.LEFT:
                self.keys_pressed['left'] = False
            elif key == arcade.key.RIGHT:
                self.keys_pressed['right'] = False

def main():
    """Hauptfunktion - startet das Spiel mit Title Screen"""
    window = arcade.Window(800, 600, "Space Defender - 8-Bit Retro Edition")
    
    # Title Screen laden und anzeigen
    from title import TitleScreen
    title_view = TitleScreen()
    window.show_view(title_view)
    
    # Hintergrundmusik starten
    arcade.play_sound(background_music, volume=0.9, loop=True)
    
    arcade.run()

if __name__ == "__main__":
    main()
    