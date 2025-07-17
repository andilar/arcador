import arcade
import random
from enemy import EnemyManager  # Importiere die neue Klasse

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
        # Hellere 8-Bit Farben für bessere Sichtbarkeit
        self.color = random.choice([
            arcade.color.WHITE,
            arcade.color.YELLOW,
            arcade.color.CYAN,
            arcade.color.LIGHT_BLUE,
            arcade.color.LIGHT_GRAY
        ])
        # Größere Sterne für bessere Sichtbarkeit
        self.size = max(2, int(self.speed))
        if self.size > 4:
            self.size = 4
    
    def reset_position(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
    
    def update(self):
        # Sterne bewegen sich nach unten
        self.y -= self.speed
        
        # Wenn Stern den Bildschirm verlässt, neu positionieren
        if self.y < -5:
            self.y = 800 + 5
            self.x = random.randint(0, 800)
    
    def draw(self):
        # 8-Bit Style: Verwende draw_circle_filled für bessere Kompatibilität
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color)
        
        # Für alle Sterne: Kreuz-Effekt für 8-Bit Look
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

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        
        # Position des Raumschiffs
        self.player_x = 400
        self.player_y = 30
        
        # Bewegungsgeschwindigkeit
        self.speed = 5
        
        # Liste für Laser-Schüsse
        self.lasers = []
        
        # Laser-Geschwindigkeit
        self.laser_speed = 8
        
        # Sternenhintergrund
        self.starfield = StarField()
        
        # Gegner-Manager
        self.enemy_manager = EnemyManager(800, 600)
        
        # Punktezähler
        self.score = 0
        self.points_per_enemy = 10
        
        # Spiel-Status
        self.game_over = False
        self.player_explosion = None
        self.game_over_timer = 0
        
        # Tastenstatus für kontinuierliche Bewegung
        self.keys_pressed = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        
    def setup(self):
        pass
        
    def on_draw(self):
        self.clear()
        
        # Sternenhintergrund zeichnen (zuerst, damit er im Hintergrund ist)
        self.starfield.draw()
        
        # Punktestand anzeigen (oben links)
        arcade.draw_text(f"PUNKTE: {self.score}", 20, 570, arcade.color.WHITE, 20, font_name="Kenney Blocks")
        
        if not self.game_over:
            # Raumschiff (weißes Dreieck) zeichnen
            arcade.draw_triangle_filled(self.player_x, self.player_y + 15,  # Spitze oben
                                       self.player_x - 15, self.player_y - 15,  # Unten links
                                       self.player_x + 15, self.player_y - 15,  # Unten rechts
                                       arcade.color.WHITE)
        
        # Laser-Schüsse zeichnen
        for laser in self.lasers:
            arcade.draw_circle_filled(laser['x'], laser['y'], 3, arcade.color.RED)
            
        # Gegner und Explosionen zeichnen
        self.enemy_manager.draw()
        
        # Spieler-Explosion zeichnen
        if self.player_explosion:
            self.player_explosion.draw()
            
        # Game Over Text
        if self.game_over:
            arcade.draw_text("GAME OVER", 130, 350, arcade.color.RED, 64, font_name="Kenney Blocks")
            arcade.draw_text(f"ENDPUNKTESTAND: {self.score}", 200, 300, arcade.color.YELLOW, 24, font_name="Kenney Blocks")
            arcade.draw_text("Drücke R zum Neustarten", 220, 250, arcade.color.WHITE, 24, font_name="Kenney Blocks")
        
    def on_update(self, delta_time):
        # Sternenhintergrund immer aktualisieren
        self.starfield.update()
        
        if not self.game_over:
            # Kontinuierliche Bewegung basierend auf gedrückten Tasten
            if self.keys_pressed['up']:
                self.player_y += self.speed
            if self.keys_pressed['down']:
                self.player_y -= self.speed
            if self.keys_pressed['left']:
                self.player_x -= self.speed
            if self.keys_pressed['right']:
                self.player_x += self.speed
            
            # Bildschirmgrenzen für das Raumschiff
            # Berücksichtigt die Dreiecksgröße (15 Pixel)
            if self.player_x < 15:
                self.player_x = 15
            elif self.player_x > 800 - 15:
                self.player_x = 800 - 15
                
            if self.player_y < 15:
                self.player_y = 15
            elif self.player_y > 600 - 15:
                self.player_y = 600 - 15
            
            # Laser-Schüsse bewegen
            for laser in self.lasers[:]:  # Kopie der Liste zum sicheren Entfernen
                laser['y'] += self.laser_speed
                
                # Laser entfernen, wenn sie den Bildschirm verlassen
                if laser['y'] > 600:
                    self.lasers.remove(laser)
                    
            # Gegner updaten
            self.enemy_manager.update()
            
            # Grüne Gegner ab 200 Punkten aktivieren
            if self.score >= 200:
                self.enemy_manager.enable_green_enemies = True
            
            # Kollisionen prüfen und Punkte vergeben
            hit_results = self.enemy_manager.check_laser_collisions(self.lasers)
            for hit in hit_results:
                # Prüfe ob es das neue Format (mit Punkten) oder alte Format ist
                if isinstance(hit, dict) and 'laser' in hit:
                    # Neues Format mit Punkten
                    laser = hit['laser']
                    points = hit['points']
                else:
                    # Altes Format - nur Laser, Standard-Punkte verwenden
                    laser = hit
                    points = self.points_per_enemy
                    
                if laser in self.lasers:
                    self.lasers.remove(laser)
                    # Punkte basierend auf Gegnertyp hinzufügen
                    self.score += points
                    
            # Prüfe Kollision zwischen Spieler und roten Gegnern
            for enemy in self.enemy_manager.enemies:
                if enemy.alive and self.check_player_collision(enemy):
                    self.player_dies()
                    break
                    
            # Prüfe Kollision zwischen Spieler und grünen Gegnern (sicher)
            if hasattr(self.enemy_manager, 'green_enemies'):
                for enemy in self.enemy_manager.green_enemies:
                    if enemy.alive and self.check_player_collision(enemy):
                        self.player_dies()
                        break
        else:
            # Game Over - nur Explosionen updaten
            self.game_over_timer += 1
            if self.player_explosion:
                self.player_explosion.update()
                if self.player_explosion.is_finished():
                    self.player_explosion = None
    
    def check_player_collision(self, enemy):
        """Prüft Kollision zwischen Spieler und Gegner"""
        distance = ((self.player_x - enemy.x) ** 2 + (self.player_y - enemy.y) ** 2) ** 0.5
        return distance < 20  # Kollisionsradius
    
    def player_dies(self):
        """Spieler stirbt - Explosion und Game Over"""
        from enemy import Explosion
        self.player_explosion = Explosion(self.player_x, self.player_y)
        self.game_over = True
        self.game_over_timer = 0
        
    def restart_game(self):
        """Spiel neu starten"""
        self.player_x = 400
        self.player_y = 30
        self.lasers = []
        self.starfield = StarField()  # Neuen Sternenhintergrund erstellen
        self.enemy_manager = EnemyManager(800, 600)
        self.score = 0  # Punktestand zurücksetzen
        self.game_over = False
        self.player_explosion = None
        self.game_over_timer = 0
        self.keys_pressed = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        
    def on_key_press(self, key, modifiers):
        if not self.game_over:
            # Pfeiltasten für Raumschiff-Bewegung
            if key == arcade.key.UP:
                self.keys_pressed['up'] = True
            elif key == arcade.key.DOWN:
                self.keys_pressed['down'] = True
            elif key == arcade.key.LEFT:
                self.keys_pressed['left'] = True
            elif key == arcade.key.RIGHT:
                self.keys_pressed['right'] = True
            
            # Leertaste für Laser-Schuss
            elif key == arcade.key.SPACE:
                # Neuen Laser an der Spitze des Raumschiffs erstellen
                new_laser = {
                    'x': self.player_x,
                    'y': self.player_y + 15  # Startet an der Spitze des Dreiecks
                }
                self.lasers.append(new_laser)
                arcade.play_sound(laser_sound)
        else:
            # Game Over - R zum Neustarten
            if key == arcade.key.R:
                self.restart_game()
    
    def on_key_release(self, key, modifiers):
        if not self.game_over:
            # Tastenstatus zurücksetzen wenn Taste losgelassen wird
            if key == arcade.key.UP:
                self.keys_pressed['up'] = False
            elif key == arcade.key.DOWN:
                self.keys_pressed['down'] = False
            elif key == arcade.key.LEFT:
                self.keys_pressed['left'] = False
            elif key == arcade.key.RIGHT:
                self.keys_pressed['right'] = False

def main():
    game = MyGame(800, 600, "Raumschiff mit Laser")
    game.setup()
    arcade.play_sound(background_music, volume=0.9, loop=True)
    arcade.run()

if __name__ == "__main__":
    main()
    