import arcade
import random
import math

class TitleScreen(arcade.View):
    def __init__(self):
        super().__init__()
        
        # Start-Screen Animation
        self.title_flash_timer = 0
        self.demo_ship_x = 100
        self.demo_ship_direction = 1
        
        # Sterne für Hintergrund
        self.stars = []
        self.create_background_stars()
        
    def create_background_stars(self):
        """Erstellt Hintergrundsterne für das Menü"""
        for _ in range(50):
            star = {
                'x': random.randint(0, 800),
                'y': random.randint(0, 600),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.5, 1.5),
                'color': random.choice([
                    arcade.color.WHITE,
                    arcade.color.LIGHT_BLUE,
                    arcade.color.LIGHT_GRAY
                ])
            }
            self.stars.append(star)
    
    def on_show_view(self):
        """Called when this view is shown"""
        arcade.set_background_color(arcade.color.BLACK)
        
    def on_draw(self):
        """Render the screen."""
        self.clear()
        
        # Hintergrundsterne zeichnen
        for star in self.stars:
            arcade.draw_circle_filled(star['x'], star['y'], star['size'], star['color'])
        
        # Titel mit Flash-Effekt
        title_color = arcade.color.CYAN if self.title_flash_timer < 30 else arcade.color.WHITE
        arcade.draw_text("SPACE DEFENDER", 180, 450, title_color, 48, font_name="Kenney Blocks")
        
        # Untertitel
        arcade.draw_text("8-Bit Retro Edition", 280, 400, arcade.color.YELLOW, 20, font_name="Kenney Blocks")
        
        # Demo-Raumschiff animiert
        arcade.draw_triangle_filled(
            self.demo_ship_x, 320,      # Spitze oben
            self.demo_ship_x - 15, 290, # Unten links
            self.demo_ship_x + 15, 290, # Unten rechts
            arcade.color.WHITE
        )
        
        # Demo-Gegner
        arcade.draw_triangle_filled(
            600, 350,      # Spitze unten
            600 - 12, 374, # Oben links
            600 + 12, 374, # Oben rechts
            arcade.color.RED
        )
        
        # Grüner Demo-Gegner
        arcade.draw_circle_filled(650, 380, 12, arcade.color.GREEN)
        arcade.draw_circle_filled(650, 380, 2, arcade.color.LIGHT_GREEN)
        
        # Gelber Demo-Gegner mit Health-Balken
        arcade.draw_circle_filled(700, 320, 15, arcade.color.YELLOW)
        arcade.draw_circle_filled(700, 320, 4, arcade.color.LIGHT_YELLOW)
        # Health-Balken
        for i in range(3):
            bar_x = 700 - 10 + (i * 7)
            bar_y = 340
            arcade.draw_circle_filled(bar_x, bar_y, 2, arcade.color.GREEN)
            
        # Blauer Loot-Stern (vereinfacht)
        star_points = []
        for i in range(8):
            angle = math.radians(i * 45)
            radius = 8 if i % 2 == 0 else 4
            point_x = 150 + radius * math.cos(angle)
            point_y = 250 + radius * math.sin(angle)
            star_points.append((point_x, point_y))
        arcade.draw_polygon_filled(star_points, arcade.color.BLUE)
        
        # Anweisungen
        arcade.draw_text("STEUERUNG:", 50, 200, arcade.color.WHITE, 16, font_name="Kenney Blocks")
        arcade.draw_text("Pfeiltasten - Bewegung", 50, 180, arcade.color.LIGHT_GRAY, 14, font_name="Kenney Blocks")
        arcade.draw_text("Leertaste - Schießen", 50, 160, arcade.color.LIGHT_GRAY, 14, font_name="Kenney Blocks")
        
        arcade.draw_text("GEGNER:", 400, 200, arcade.color.WHITE, 16, font_name="Kenney Blocks")
        arcade.draw_text("Rot: 10 Punkte", 400, 180, arcade.color.RED, 14, font_name="Kenney Blocks")
        arcade.draw_text("Grün: 30 Punkte (ab 200)", 400, 160, arcade.color.GREEN, 14, font_name="Kenney Blocks")
        arcade.draw_text("Gelb: 160 Punkte (ab 2000)", 400, 140, arcade.color.YELLOW, 14, font_name="Kenney Blocks")
        
        arcade.draw_text("FEATURES:", 50, 120, arcade.color.WHITE, 16, font_name="Kenney Blocks")
        arcade.draw_text("• Sammle blaue Sterne für Laser-Upgrades", 50, 100, arcade.color.CYAN, 12, font_name="Kenney Blocks")
        arcade.draw_text("• Schwierigkeit steigt ab 1000 Punkten", 50, 85, arcade.color.CYAN, 12, font_name="Kenney Blocks")
        arcade.draw_text("• Gelbe Gegner respawnen wenn nicht besiegt", 50, 70, arcade.color.CYAN, 12, font_name="Kenney Blocks")
        
        # Start-Anweisung (blinkend)
        if self.title_flash_timer < 45:
            arcade.draw_text("DRÜCKE SPACE ZUM STARTEN", 220, 30, arcade.color.GREEN, 20, font_name="Kenney Blocks")
    
    def on_update(self, delta_time):
        """Update animations"""
        # Hintergrundsterne bewegen
        for star in self.stars:
            star['y'] -= star['speed']
            if star['y'] < -5:
                star['y'] = 605
                star['x'] = random.randint(0, 800)
        
        # Titel-Flash Animation
        self.title_flash_timer += 1
        if self.title_flash_timer >= 60:  # 1 Sekunde bei 60 FPS
            self.title_flash_timer = 0
            
        # Demo-Raumschiff Animation
        self.demo_ship_x += self.demo_ship_direction * 2
        if self.demo_ship_x >= 300 or self.demo_ship_x <= 100:
            self.demo_ship_direction *= -1
    
    def on_key_press(self, key, modifiers):
        """Handle key presses"""
        if key == arcade.key.SPACE:
            # Wechsle zur GameView
            from game import GameView  # Import hier um zirkuläre Imports zu vermeiden
            game_view = GameView()
            self.window.show_view(game_view)


class GameOverScreen(arcade.View):
    def __init__(self, score, laser_count):
        super().__init__()
        self.score = score
        self.laser_count = laser_count
        
        # Sterne für Hintergrund
        self.stars = []
        self.create_background_stars()
        
    def create_background_stars(self):
        """Erstellt Hintergrundsterne für Game Over Screen"""
        for _ in range(30):
            star = {
                'x': random.randint(0, 800),
                'y': random.randint(0, 600),
                'size': random.randint(1, 2),
                'speed': random.uniform(0.3, 1.0),
                'color': random.choice([
                    arcade.color.DARK_GRAY,
                    arcade.color.GRAY
                ])
            }
            self.stars.append(star)
    
    def on_show_view(self):
        """Called when this view is shown"""
        arcade.set_background_color(arcade.color.BLACK)
        
    def on_draw(self):
        """Render the screen."""
        self.clear()
        
        # Hintergrundsterne zeichnen (gedimmt)
        for star in self.stars:
            arcade.draw_circle_filled(star['x'], star['y'], star['size'], star['color'])
        
        # Game Over Text
        arcade.draw_text("GAME OVER", 200, 400, arcade.color.RED, 64, font_name="Kenney Blocks")
        
        # Statistiken
        arcade.draw_text(f"ENDPUNKTESTAND: {self.score}", 220, 330, arcade.color.YELLOW, 24, font_name="Kenney Blocks")
        arcade.draw_text(f"LASER LEVEL: {self.laser_count}", 280, 300, arcade.color.CYAN, 20, font_name="Kenney Blocks")
        
        # Bewertung basierend auf Punktzahl
        if self.score < 500:
            rating = "ANFÄNGER"
            rating_color = arcade.color.LIGHT_GRAY
        elif self.score < 1500:
            rating = "SOLIDE LEISTUNG"
            rating_color = arcade.color.GREEN
        elif self.score < 3000:
            rating = "BEEINDRUCKEND!"
            rating_color = arcade.color.ORANGE
        elif self.score < 5000:
            rating = "SPACE ACE!"
            rating_color = arcade.color.PURPLE
        else:
            rating = "LEGENDARY!"
            rating_color = arcade.color.GOLD
            
        arcade.draw_text(rating, 300, 250, rating_color, 24, font_name="Kenney Blocks")
        
        # Optionen
        arcade.draw_text("R - Nochmal spielen", 280, 150, arcade.color.WHITE, 20, font_name="Kenney Blocks")
        arcade.draw_text("ESC - Hauptmenü", 290, 120, arcade.color.LIGHT_GRAY, 18, font_name="Kenney Blocks")
        arcade.draw_text("Q - Beenden", 330, 90, arcade.color.GRAY, 16, font_name="Kenney Blocks")
    
    def on_update(self, delta_time):
        """Update animations"""
        # Hintergrundsterne bewegen (langsam)
        for star in self.stars:
            star['y'] -= star['speed']
            if star['y'] < -5:
                star['y'] = 605
                star['x'] = random.randint(0, 800)
    
    def on_key_press(self, key, modifiers):
        """Handle key presses"""
        if key == arcade.key.R:
            # Neues Spiel starten
            from game import GameView  # Import hier um zirkuläre Imports zu vermeiden
            game_view = GameView()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            # Zurück zum Hauptmenü
            title_view = TitleScreen()
            self.window.show_view(title_view)
        elif key == arcade.key.Q:
            # Spiel beenden
            self.window.close()
            