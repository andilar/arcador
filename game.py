import arcade

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
        
        # Raumschiff (weißes Dreieck) zeichnen
        arcade.draw_triangle_filled(self.player_x, self.player_y + 15,  # Spitze oben
                                   self.player_x - 15, self.player_y - 15,  # Unten links
                                   self.player_x + 15, self.player_y - 15,  # Unten rechts
                                   arcade.color.WHITE)
        
        # Laser-Schüsse zeichnen
        for laser in self.lasers:
            arcade.draw_circle_filled(laser['x'], laser['y'], 3, arcade.color.RED)
        
    def on_update(self, delta_time):
        # Kontinuierliche Bewegung basierend auf gedrückten Tasten
        if self.keys_pressed['up']:
            self.player_y += self.speed
        if self.keys_pressed['down']:
            self.player_y -= self.speed
        if self.keys_pressed['left']:
            self.player_x -= self.speed
        if self.keys_pressed['right']:
            self.player_x += self.speed
        
        # Laser-Schüsse bewegen
        for laser in self.lasers[:]:  # Kopie der Liste zum sicheren Entfernen
            laser['y'] += self.laser_speed
            
            # Laser entfernen, wenn sie den Bildschirm verlassen
            if laser['y'] > 600:
                self.lasers.remove(laser)
        
    def on_key_press(self, key, modifiers):
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
    
    def on_key_release(self, key, modifiers):
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
    arcade.run()

if __name__ == "__main__":
    main()