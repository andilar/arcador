import arcade
import random


ship_explosion = arcade.load_sound("ship_explosion.mp3")


class EnemySpaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(1, 3)  # Zufällige Geschwindigkeit
        self.size = 12
        self.alive = True
        
        
    def update(self):
        """Gegner bewegt sich nach unten"""
        if self.alive:
            self.y -= self.speed
            
    def draw(self):
        """Gegnerisches Raumschiff zeichnen (rotes umgedrehtes Dreieck)"""
        if self.alive:
            arcade.draw_triangle_filled(
                self.x, self.y - self.size,      # Spitze unten
                self.x - self.size, self.y + self.size,  # Oben links
                self.x + self.size, self.y + self.size,  # Oben rechts
                arcade.color.RED
            )
            
    def is_off_screen(self):
        """Prüft ob Gegner den Bildschirm verlassen hat"""
        return self.y < -20
        
    def check_collision(self, laser_x, laser_y, laser_radius=3):
        """Prüft Kollision mit Laser"""
        if not self.alive:
            return False
            
        distance = ((self.x - laser_x) ** 2 + (self.y - laser_y) ** 2) ** 0.5
        return distance < (self.size + laser_radius)
        
    def explode(self):
        """Gegner explodiert"""
        self.alive = False


class GreenEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed_x = random.choice([-2, 2])  # Bewegt sich links oder rechts
        self.speed_y = 0.5  # Langsam nach unten
        self.size = 12
        self.alive = True
        self.direction_change_timer = 0
        
    def update(self):
        """Grüner Gegner bewegt sich horizontal und langsam nach unten"""
        if self.alive:
            # Horizontale Bewegung
            self.x += self.speed_x
            
            # Vertikale Bewegung (langsam nach unten)
            self.y -= self.speed_y
            
            # An Bildschirmrändern abprallen
            if self.x <= 15 or self.x >= 785:
                self.speed_x *= -1
            
            # Gelegentlich Richtung wechseln für unvorhersehbare Bewegung
            self.direction_change_timer += 1
            if self.direction_change_timer >= random.randint(120, 240):  # 2-4 Sekunden
                self.speed_x *= -1
                self.direction_change_timer = 0
                
    def draw(self):
        """Grünes Raumschiff zeichnen (grünes Rechteck mit Details)"""
        if self.alive:
            # Hauptkörper (grünes Rechteck) - verwende draw_circle_filled als Ersatz
            arcade.draw_circle_filled(self.x, self.y, self.size, arcade.color.GREEN)
            
            # Flügel als kleinere Kreise
            arcade.draw_circle_filled(self.x - self.size, self.y + 6, 3, arcade.color.DARK_GREEN)
            arcade.draw_circle_filled(self.x + self.size, self.y + 6, 3, arcade.color.DARK_GREEN)
            arcade.draw_circle_filled(self.x - self.size, self.y - 6, 3, arcade.color.DARK_GREEN)
            arcade.draw_circle_filled(self.x + self.size, self.y - 6, 3, arcade.color.DARK_GREEN)
            
            # Cockpit/Details
            arcade.draw_circle_filled(self.x, self.y, 2, arcade.color.LIGHT_GREEN)
            
    def is_off_screen(self):
        """Prüft ob grüner Gegner den Bildschirm verlassen hat"""
        return self.y < -20
        
    def check_collision(self, laser_x, laser_y, laser_radius=3):
        """Prüft Kollision mit Laser"""
        if not self.alive:
            return False
            
        distance = ((self.x - laser_x) ** 2 + (self.y - laser_y) ** 2) ** 0.5
        return distance < (self.size + laser_radius)
        
    def explode(self):
        """Grüner Gegner explodiert"""
        self.alive = False


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        self.lifetime = 30  # Frames
        
        # Erstelle Explosionspartikel
        for _ in range(12):
            particle = {
                'x': x,
                'y': y,
                'speed_x': random.uniform(-4, 4),
                'speed_y': random.uniform(-4, 4),
                'color': random.choice([
                    arcade.color.ORANGE,
                    arcade.color.YELLOW,
                    arcade.color.RED,
                    arcade.color.WHITE
                ]),
                'size': random.uniform(2, 6)
            }
            self.particles.append(particle)
    
    def update(self):
        """Explosionspartikel bewegen und altern lassen"""
        self.lifetime -= 1
        
        for particle in self.particles:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            particle['size'] *= 0.95  # Partikel werden kleiner
            
    def draw(self):
        """Explosionspartikel zeichnen"""
        for particle in self.particles:
            if particle['size'] > 0.5:
                arcade.draw_circle_filled(
                    particle['x'], 
                    particle['y'], 
                    particle['size'], 
                    particle['color']
                )
    
    def is_finished(self):
        """Prüft ob Explosion beendet ist"""
        return self.lifetime <= 0


class EnemyManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemies = []
        self.green_enemies = []  # Liste für grüne Gegner
        self.explosions = []
        self.spawn_timer = 0
        self.spawn_delay = 60  # Frames zwischen Spawns
        
        # Grüne Gegner Einstellungen
        self.enable_green_enemies = False
        self.green_enemy_timer = 0
        self.green_enemy_spawn_rate = 180  # Alle 3 Sekunden bei 60 FPS
        
    def update(self):
        """Alle Gegner und Explosionen updaten"""
        # Rote Gegner spawnen
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_enemy()
            self.spawn_timer = 0
            
        # Grüne Gegner spawnen (wenn aktiviert)
        if self.enable_green_enemies:
            self.green_enemy_timer += 1
            if self.green_enemy_timer >= self.green_enemy_spawn_rate:
                self.spawn_green_enemy()
                self.green_enemy_timer = 0
            
        # Rote Gegner updaten
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.is_off_screen() or not enemy.alive:
                self.enemies.remove(enemy)
                
        # Grüne Gegner updaten
        for enemy in self.green_enemies[:]:
            enemy.update()
            if enemy.is_off_screen() or not enemy.alive:
                self.green_enemies.remove(enemy)
                
        # Explosionen updaten
        for explosion in self.explosions[:]:
            explosion.update()
            
            if explosion.is_finished():
                self.explosions.remove(explosion)
                
    def spawn_enemy(self):
        """Neuen roten Gegner spawnen"""
        x = random.randint(20, self.screen_width - 20)
        y = self.screen_height + 10
        enemy = EnemySpaceship(x, y)
        self.enemies.append(enemy)
        
    def spawn_green_enemy(self):
        """Neuen grünen Gegner spawnen"""
        x = random.randint(50, self.screen_width - 50)
        y = self.screen_height + 10
        green_enemy = GreenEnemy(x, y)
        self.green_enemies.append(green_enemy)
        
    def draw(self):
        """Alle Gegner und Explosionen zeichnen"""
        for enemy in self.enemies:
            enemy.draw()
            
        for enemy in self.green_enemies:
            enemy.draw()
            
        for explosion in self.explosions:
            explosion.draw()
            
    def check_laser_collisions(self, lasers):
        """Prüft Kollisionen zwischen Lasern und Gegnern"""
        hits = []
        
        # Kollisionen mit roten Gegnern prüfen
        for laser in lasers[:]:
            for enemy in self.enemies:
                if enemy.check_collision(laser['x'], laser['y']):
                    # Explosion erstellen
                    explosion = Explosion(enemy.x, enemy.y)
                    self.explosions.append(explosion)
                    
                    # Gegner explodieren lassen
                    enemy.explode()
                    arcade.play_sound(ship_explosion)
                    
                    # Laser für Entfernung markieren mit Punktewert
                    hits.append({'laser': laser, 'points': 10})  # Rote Gegner = 10 Punkte
                    break
                    
        # Kollisionen mit grünen Gegnern prüfen
        for laser in lasers[:]:
            for enemy in self.green_enemies:
                if enemy.check_collision(laser['x'], laser['y']):
                    # Explosion erstellen
                    explosion = Explosion(enemy.x, enemy.y)
                    self.explosions.append(explosion)
                    
                    # Grüner Gegner explodiert
                    enemy.explode()
                    arcade.play_sound(ship_explosion)
                    
                    # Laser für Entfernung markieren mit höherem Punktewert
                    # Prüfen ob dieser Laser nicht schon markiert wurde
                    already_hit = any(hit['laser'] == laser for hit in hits)
                    if not already_hit:
                        hits.append({'laser': laser, 'points': 30})  # Grüne Gegner = 30 Punkte
                    break
                    
        return hits  # Gibt getroffene Laser mit Punktewerten zurück
    