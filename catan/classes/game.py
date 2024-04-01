"""
Game overhead. It stores the players, along with flags for turn progression
and multi-step interaction.
"""
class Game:
    def __init__(self):
        self.number_players = 1
        self.turn = 1
        self.build_attempt = "null"
    
    """to_dict is used for session variable saving"""
    def to_dict(self):
        return {
            'number_players': self.number_players,
            'turn': self.turn,
            'build_attempt': self.build_attempt,
        }