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
            {'index': 1, 'type': "property", 'name': 'Mediterranean Avenue'},
            {'index': 2, 'type': "card_event", 'name': 'Community Chest'},
            {'index': 3, 'type': "property", 'name': 'Baltic Avenue'},
            {'index': 4, 'type': "tax", 'name': 'Income Tax'},
            {'index': 5, 'type': "property", 'name': 'Reading Railroad'},
            {'index': 6, 'type': "property", 'name': 'Oriental Avenue'},
            {'index': 7, 'type': "card_event", 'name': 'Chance'},
            {'index': 8, 'type': "property", 'name': 'Vermont Avenue'},
            {'index': 9, 'type': "property", 'name': 'Connecticut Avenue'},
            {'index': 10, 'type': "jail", 'name': 'Jail'},
            {'index': 11, 'type': "property", 'name': 'St. Charles Place'},
            {'index': 12, 'type': "tax", 'name': 'Electric Company'},
            {'index': 13, 'type': "property", 'name': 'States Avenue'},
            {'index': 14, 'type': "property", 'name': 'Virginia Avenue'},
            {'index': 15, 'type': "property", 'name': 'Pennsylvania Railroad'},
            {'index': 16, 'type': "property", 'name': 'St. James Place'},
            {'index': 17, 'type': "card_event", 'name': 'Community Chest'},
            {'index': 18, 'type': "property", 'name': 'Tennessee Avenue'},
            {'index': 19, 'type': "property", 'name': 'New York Avenue'},
            {'index': 20, 'type': "free_parking", 'name': 'Free Parking'},
            {'index': 21, 'type': "property", 'name': 'Kentucky Avenue'},
            {'index': 22, 'type': "card_event", 'name': 'Chance'},
            {'index': 23, 'type': "property", 'name': 'Indiana Avenue'},
            {'index': 24, 'type': "property", 'name': 'Illinois Avenue'},
            {'index': 25, 'type': "property", 'name': 'B. & O. Railroad'},
            {'index': 26, 'type': "property", 'name': 'Atlantic Avenue'},
            {'index': 27, 'type': "property", 'name': 'Ventnor Avenue'},
            {'index': 28, 'type': "tax", 'name': 'Water Works'},
            {'index': 29, 'type': "property", 'name': 'Marvin Gardens'},
            {'index': 30, 'type': "go_to_jail", 'name': 'Go To Jail'},
            {'index': 31, 'type': "property", 'name': 'Pacific Avenue'},
            {'index': 32, 'type': "property", 'name': 'North Carolina Avenue'},
            {'index': 33, 'type': "card_event", 'name': 'Community Chest'},
            {'index': 34, 'type': "property", 'name': 'Pennsylvania Avenue'},
            {'index': 35, 'type': "property", 'name': 'Short Line'},
            {'index': 36, 'type': "card_event", 'name': 'Chance'},
            {'index': 37, 'type': "property", 'name': 'Park Place'},
            {'index': 38, 'type': "tax", 'name': 'Luxury Tax'},
            {'index': 39, 'type': "property", 'name': 'Boardwalk'},
        ]

        # Create space instances and add them to the board
        for space_data in space_definitions:
            space = Space.objects.create(**space_data)
            board.spaces.add(space)

        return board
    
    # Method to get a space at a given index
    def get_space(self, index):
        return self.spaces.get(index=index)