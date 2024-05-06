from django.db import models
from .property import Property
"""
A deck for holding property cards.
"""
class PropertyDeck(models.Model):
    game_key = models.UUIDField(unique=True, null=True)
    properties = models.ManyToManyField('Property', related_name='property_decks')

    """Initialization; properties are manually defined"""
    @classmethod
    def initialize(cls, game_key):
        deck = cls.objects.create(game_key=game_key)

        property_definitions = [
            {'index': 0, 'group': "brown", 'name': "Old Kent Road", 'prices': "60,50,30", 'rents': "2,10,30,90,160,250"},
            {'index': 1, 'group': "brown", 'name': "Whitechapel Road", 'prices': "60,50,30", 'rents': "4,20,60,180,320,450"},
            {'index': 2, 'group': "light_blue", 'name': "The Angel, Islington", 'prices': "100,50,50", 'rents': "6,30,90,270,400,550"},
            {'index': 3, 'group': "light_blue", 'name': "Euston Road", 'prices': "100,50,50", 'rents': "6,30,90,270,400,550"},
            {'index': 4, 'group': "light_blue", 'name': "Pentonville Road", 'prices': "120,50,60", 'rents': "8,40,100,300,450,600"},
            {'index': 5, 'group': "pink", 'name': "Pall Mall", 'prices': "140,100,70", 'rents': "10,50,150,450,625,750"},
            {'index': 6, 'group': "pink", 'name': "Whitechapel", 'prices': "140,100,70", 'rents': "10,50,150,450,625,750"},
            {'index': 7, 'group': "pink", 'name': "Northumberland Avenue", 'prices': "160,100,80", 'rents': "12,60,180,500,700,900"},
            {'index': 8, 'group': "orange", 'name': "Bow Street", 'prices': "180,100,90", 'rents': "14,70,200,550,750,950"},
            {'index': 9, 'group': "orange", 'name': "Marlborough Street", 'prices': "180,100,90", 'rents': "14,70,200,550,750,950"},
            {'index': 10, 'group': "orange", 'name': "Vine Street", 'prices': "200,100,100", 'rents': "16,80,220,600,800,1000"},
            {'index': 11, 'group': "red", 'name': "Strand", 'prices': "220,150,110", 'rents': "18,90,250,700,875,1050"},
            {'index': 12, 'group': "red", 'name': "Fleet Street", 'prices': "220,150,110", 'rents': "18,90,250,700,875,1050"},
            {'index': 13, 'group': "red", 'name': "Trafalgar Square", 'prices': "240,150,120", 'rents': "20,100,300,750,925,1100"},
            {'index': 14, 'group': "yellow", 'name': "Leicester Square", 'prices': "260,150,130", 'rents': "22,110,330,800,975,1150"},
            {'index': 15, 'group': "yellow", 'name': "Coventry Street", 'prices': "260,150,130", 'rents': "22,110,330,800,975,1150"},
            {'index': 16, 'group': "yellow", 'name': "Piccadilly", 'prices': "280,150,140", 'rents': "24,120,360,850,1025,1200"},
            {'index': 17, 'group': "green", 'name': "Regent Street", 'prices': "300,200,150", 'rents': "26,130,390,900,1100,1275"},
            {'index': 18, 'group': "green", 'name': "Oxford Street", 'prices': "300,200,150", 'rents': "26,130,390,900,1100,1275"},
            {'index': 19, 'group': "green", 'name': "Bond Street", 'prices': "320,200,160", 'rents': "28,150,450,1000,1200,1400"},
            {'index': 20, 'group': "dark_blue", 'name': "Park Lane", 'prices': "350,200,175", 'rents': "35,175,500,1100,1300,1500"},
            {'index': 21, 'group': "dark_blue", 'name': "Mayfair", 'prices': "400,200,200", 'rents': "50,200,600,1400,1700,2000"},
            {'index': 22, 'group': "railroad", 'name': "Kings Cross Station", 'prices': "200,0,100", 'rents': "25,50,100,200"},
            {'index': 23, 'group': "railroad", 'name': "Marylebone Station", 'prices': "200,0,100", 'rents': "25,50,100,200"},
            {'index': 24, 'group': "railroad", 'name': "Fenchurch St. Station", 'prices': "200,0,100", 'rents': "25,50,100,200"},
            {'index': 25, 'group': "railroad", 'name': "Liverpool St. Station", 'prices': "200,0,100", 'rents': "25,50,100,200"},
            {'index': 26, 'group': "utility", 'name': "Electric Company", 'prices': "150,0,75", 'rents': "4,10"},
            {'index': 27, 'group': "utility", 'name': "Water Works", 'prices': "150,0,75", 'rents': "4,10"},
        ]

        # Create property instances and add them to the deck
        for property_data in property_definitions:
            property = Property.objects.create(**property_data)
            deck.properties.add(property)

        return deck