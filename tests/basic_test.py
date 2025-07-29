
def test_simple_math():
    """Ein ganz einfacher Test um zu prüfen ob pytest funktioniert"""
    result = 2 + 2
    assert result == 4


def test_game_constants():
    """Test von Spiel-Konstanten (falls vorhanden)"""
    # Beispiel: Falls Sie Konstanten in Ihrem Spiel haben
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    assert SCREEN_WIDTH > 0
    assert SCREEN_HEIGHT > 0
    assert SCREEN_WIDTH >= SCREEN_HEIGHT  # Querformat


def test_player_health():
    """Einfacher Test für Spieler-Gesundheit"""
    # Simuliere eine einfache Player-Klasse
    class Player:
        def __init__(self):
            self.health = 100
            
        def take_damage(self, damage):
            self.health -= damage
            if self.health < 0:
                self.health = 0
    
    # Test
    player = Player()
    assert player.health == 100
    
    player.take_damage(25)
    assert player.health == 75
    
    player.take_damage(100)
    assert player.health == 0  # Gesundheit kann nicht unter 0 fallen
