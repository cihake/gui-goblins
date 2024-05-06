from django.db import models
from .space import Space
"""
The board that the game is played on.
The spaces are divided into categories, and every space is unique.
"""
class Board(models.Model):
    game_key = models.UUIDField(unique=True)
    spaces = models.ManyToManyField('Space', related_name='board')

    """Initialization; spaces are manually defined"""
    @classmethod
    def initialize(cls, game_key):
        board = cls.objects.create(game_key=game_key)

        space_definitions = [
    {'index': 0, 'type': "GO", 'name': 'GO'},
    {'index': 1, 'type': "property", 'name': "Old Kent Road"},
    {'index': 2, 'type': "card_event", 'name': 'Community Chest'},
    {'index': 3, 'type': "property", 'name': "Whitechapel Road"},
    {'index': 4, 'type': "tax", 'name': 'Income Tax'},
    {'index': 5, 'type': "property", 'name': "Marylebone Station"},
    {'index': 6, 'type': "property", 'name': "The Angel, Islington"},
    {'index': 7, 'type': "card_event", 'name': 'Chance'},
    {'index': 8, 'type': "property", 'name': "Euston Road"},
    {'index': 9, 'type': "property", 'name': "Pentonville Road"},
    {'index': 10, 'type': "jail", 'name': 'Jail'},
    {'index': 11, 'type': "property", 'name': "Pall Mall"},
    {'index': 12, 'type': "property", 'name': "Electric Company"},
    {'index': 13, 'type': "property", 'name': "Whitechapel"},
    {'index': 14, 'type': "property", 'name': "Northumberland Avenue"},
    {'index': 15, 'type': "property", 'name': "Pennsylvania Railroad"},
    {'index': 16, 'type': "property", 'name': "Bow Street"},
    {'index': 17, 'type': "card_event", 'name': 'Community Chest'},
    {'index': 18, 'type': "property", 'name': "Marlborough Street"},
    {'index': 19, 'type': "property", 'name': "Vine Street"},
    {'index': 20, 'type': "free_parking", 'name': 'Free Parking'},
    {'index': 21, 'type': "property", 'name': "Strand"},
    {'index': 22, 'type': "card_event", 'name': 'Chance'},
    {'index': 23, 'type': "property", 'name': "Fleet Street"},
    {'index': 24, 'type': "property", 'name': "Trafalgar Square"},
    {'index': 25, 'type': "property", 'name': "Fenchurch St. Station"},
    {'index': 26, 'type': "property", 'name': "Leicester Square"},
    {'index': 27, 'type': "property", 'name': "Coventry Street"},
    {'index': 28, 'type': "property", 'name': "Water Works"},
    {'index': 29, 'type': "property", 'name': "Piccadilly"},
    {'index': 30, 'type': "go_to_jail", 'name': 'Go To Jail'},
    {'index': 31, 'type': "property", 'name': "Regent Street"},
    {'index': 32, 'type': "property", 'name': "Oxford Street"},
    {'index': 33, 'type': "card_event", 'name': 'Community Chest'},
    {'index': 34, 'type': "property", 'name': "Bond Street"},
    {'index': 35, 'type': "property", 'name': "Liverpool St. Station"},
    {'index': 36, 'type': "card_event", 'name': 'Chance'},
    {'index': 37, 'type': "property", 'name': "Park Lane"},
    {'index': 38, 'type': "tax", 'name': 'Luxury Tax'},
    {'index': 39, 'type': "property", 'name': "Mayfair"},
]

        # Create space instances and add them to the board
        for space_data in space_definitions:
            space = Space.objects.create(**space_data)
            board.spaces.add(space)

        return board
    
    # Method to get a space at a given index
    def get_space(self, index):
        return self.spaces.get(index=index)