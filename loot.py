import arcade
import random
import math

class BlueStar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rotation = 0
        self.rotation_speed = 3  # Grad pro Frame
        self.size = 10
        self.alive = True
        self.float_offset = 0
        self.float_speed = 0.1
        
    def update(self):
        """Stern rotieren und leicht schweben lassen"""
        if self.alive:
            # Rotation für bessere Sichtbarkeit
            self.rotation += self.rotation_speed
            if self.rotation >= 360:
                self.rotation = 0
                
            # Leichtes Schweben auf und ab
            self.float_offset += self.float_speed
            
            # Langsam nach unten bewegen
            self.y -= 0.5
            
    def draw(self):
        """Blauen rotierenden Stern zeichnen"""
        if self.alive:
            # Schwebe-Effekt
            draw_y = self.y + math.sin(self.float_offset) * 2
            
            # Stern als 8-zackiger Stern zeichnen
            self.draw_star(self.x, draw_y, self.size, self.rotation)
            
    def draw_star(self, x, y, size, rotation):
        """Zeichnet einen 8-zackigen Stern"""
        points = []
        num_points = 8
        
        for i in range(num_points * 2):  # Doppelt so viele Punkte für Zacken
            angle = (i * 180 / num_points) + rotation
            angle_rad = math.radians(angle)
            
            # Abwechselnd äußere und innere Punkte
            if i % 2 == 0:
                # Äußere Punkte
                radius = size
            else:
                # Innere Punkte (kleiner)
                radius = size * 0.5
                
            point_x = x + radius * math.cos(angle_rad)
            point_y = y + radius * math.sin(angle_rad)
            points.append((point_x, point_y))  # Als Tupel hinzufügen
            
        # Stern zeichnen
        arcade.draw_polygon_filled(points, arcade.color.BLUE)
        
        # Leuchteffekt (heller blauer Kreis in der Mitte)
        arcade.draw_circle_filled(x, y, size * 0.3, arcade.color.LIGHT_BLUE)
        
    def is_off_screen(self):
        """Prüft ob Stern den Bildschirm verlassen hat"""
        return self.y < -20
        
    def check_collision(self, player_x, player_y, player_radius=15):
        """Prüft Kollision mit Spieler"""
        if not self.alive:
            return False
            
        distance = ((self.x - player_x) ** 2 + (self.y - player_y) ** 2) ** 0.5
        return distance < (self.size + player_radius)
        
    def collect(self):
        """Stern wird eingesammelt"""
        self.alive = False


class LootManager:
    def __init__(self):
        self.blue_stars = []
        self.enemies_killed = 0
        self.stars_per_enemies = 3  # Alle 3 getöteten Gegner ein Stern
        
    def enemy_killed(self, x, y):
        """Wird aufgerufen wenn ein Gegner stirbt"""
        self.enemies_killed += 1
        
        # Alle 3 Gegner einen blauen Stern spawnen
        if self.enemies_killed % self.stars_per_enemies == 0:
            self.spawn_blue_star(x, y)
            
    def spawn_blue_star(self, x, y):
        """Spawnt einen blauen Stern an der Position"""
        # Leichte zufällige Verschiebung damit Stern nicht direkt auf Explosion spawnt
        star_x = x + random.randint(-20, 20)
        star_y = y + random.randint(-10, 10)
        
        # Stelle sicher dass Stern im Bildschirm ist
        star_x = max(20, min(780, star_x))
        star_y = max(20, min(580, star_y))
        
        blue_star = BlueStar(star_x, star_y)
        self.blue_stars.append(blue_star)
        
    def update(self):
        """Alle blauen Sterne updaten"""
        for star in self.blue_stars[:]:
            star.update()
            
            # Entferne Sterne die den Bildschirm verlassen haben
            if star.is_off_screen() or not star.alive:
                self.blue_stars.remove(star)
                
    def draw(self):
        """Alle blauen Sterne zeichnen"""
        for star in self.blue_stars:
            star.draw()
            
    def check_player_collisions(self, player_x, player_y):
        """Prüft Kollisionen zwischen Spieler und blauen Sternen"""
        collected_stars = []
        
        for star in self.blue_stars:
            if star.check_collision(player_x, player_y):
                star.collect()
                collected_stars.append(star)
                
        # Entferne eingesammelte Sterne
        for star in collected_stars:
            if star in self.blue_stars:
                self.blue_stars.remove(star)
                
        return len(collected_stars)  # Anzahl eingesammelter Sterne
        
    def reset(self):
        """Loot-Manager zurücksetzen"""
        self.blue_stars = []
        self.enemies_killed = 0


class LaserUpgrade:
    def __init__(self):
        self.laser_count = 1  # Startet mit 1 Laser
        self.max_lasers = 5   # Maximum 5 Laser gleichzeitig
        
    def upgrade(self):
        """Erhöht die Anzahl der Laser"""
        if self.laser_count < self.max_lasers:
            self.laser_count += 1
            return True  # Upgrade erfolgreich
        return False  # Bereits Maximum erreicht
        
    def create_lasers(self, player_x, player_y):
        """Erstellt mehrere Laser basierend auf aktuellem Level"""
        lasers = []
        
        if self.laser_count == 1:
            # Ein Laser in der Mitte
            lasers.append({'x': player_x, 'y': player_y + 15})
        elif self.laser_count == 2:
            # Zwei Laser leicht versetzt
            lasers.append({'x': player_x - 5, 'y': player_y + 15})
            lasers.append({'x': player_x + 5, 'y': player_y + 15})
        elif self.laser_count == 3:
            # Drei Laser: Mitte und zwei Seiten
            lasers.append({'x': player_x, 'y': player_y + 15})
            lasers.append({'x': player_x - 8, 'y': player_y + 12})
            lasers.append({'x': player_x + 8, 'y': player_y + 12})
        elif self.laser_count == 4:
            # Vier Laser in Reihe
            lasers.append({'x': player_x - 12, 'y': player_y + 15})
            lasers.append({'x': player_x - 4, 'y': player_y + 15})
            lasers.append({'x': player_x + 4, 'y': player_y + 15})
            lasers.append({'x': player_x + 12, 'y': player_y + 15})
        elif self.laser_count >= 5:
            # Fünf Laser: Maximum
            lasers.append({'x': player_x, 'y': player_y + 15})
            lasers.append({'x': player_x - 8, 'y': player_y + 12})
            lasers.append({'x': player_x + 8, 'y': player_y + 12})
            lasers.append({'x': player_x - 16, 'y': player_y + 10})
            lasers.append({'x': player_x + 16, 'y': player_y + 10})
            
        return lasers
        
    def reset(self):
        """Laser-Upgrade zurücksetzen"""
        self.laser_count = 1
        