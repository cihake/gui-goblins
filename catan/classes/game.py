"""
Game overhead. It stores the players, along with flags for turn progression
and multi-step interaction.
"""
class Game:
    def __init__(self, number_players=1, turn=1, build_attempt="null"):
        self.number_players = number_players
        self.turn = turn
        self.build_attempt = build_attempt
    
    """to_dict is used for session variable saving"""
    def to_dict(self):
        return {
            'number_players': self.number_players,
            'turn': self.turn,
            'build_attempt': self.build_attempt,
        }