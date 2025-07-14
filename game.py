import arcade

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        
        # Position des Symbols
        self.player_x = 400
        self.player_y = 300
        
        # Bewegungsgeschwindigkeit
        self.speed = 30
        
    def setup(self):
        pass
        
    def on_draw(self):
        self.clear()
        
        # Weißen Kreis als Symbol zeichnen
        arcade.draw_circle_filled(self.player_x, self.player_y, 20, arcade.color.WHITE)
        
    def on_update(self, delta_time):
        pass
        
    def on_key_press(self, key, modifiers):
        # Pfeiltasten abfragen
        if key == arcade.key.UP:
            self.player_y += self.speed
        elif key == arcade.key.DOWN:
            self.player_y -= self.speed
        elif key == arcade.key.LEFT:
            self.player_x -= self.speed
        elif key == arcade.key.RIGHT:
            self.player_x += self.speed

def main():
    game = MyGame(800, 600, "Symbol bewegen")
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()