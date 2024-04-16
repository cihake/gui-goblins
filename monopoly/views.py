from django.shortcuts import render
from django.http import JsonResponse
import uuid # unique key for games
import math, random
from .models.game import Game
from .models.player import Player
from .models.board import Board
from .models.space import Space
from .models.property_deck import PropertyDeck
from .models.property import Property

def monopoly_view(request):
    # Load game key, or create one if none in session and valueless
    game_key = "no key" # variable, not saved value
    if 'game_key' not in request.session:
        request.session['game_key'] = "no key"
    try: # Game key properly stored as a uuid
        game_key = uuid.UUID(request.session['game_key'])  # Convert string to UUID
    except ValueError: # Game key is not a uuid
        request.session['game_key'] = str(uuid.uuid4())
        game_key = uuid.UUID(request.session['game_key'])
    
    # Create game objects if none match the key
    if not Game.objects.filter(game_key=game_key).exists():
        game = Game.objects.create(game_key=game_key)
        player1 = Player.objects.create(game_key=game_key, ordinal=1)
        board = Board.initialize(game_key)
        property_deck = PropertyDeck.initialize(game_key)
        game.save()
        player1.save()
        board.save()
        property_deck.save()
    else: # Load game objects
        game = Game.objects.get(game_key=game_key)
        player1 = Player.objects.get(game_key=game_key, ordinal=1)
        board = Board.objects.get(game_key=game_key)
        property_deck = PropertyDeck.objects.get(game_key=game_key)
    
    #*************************************************************************************
    # AJAX POST request; active response
    if (request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        input = request.POST.get('input')
        print("input: " + input)
        response = {}

        # Reset data
        if input == "clear_data":
            request.session.clear()
        elif input == "clear_database":
            Game.objects.all().delete()
        elif input == "unload":
            request.session['game_key'] = "no key"

        # Move the player
        elif input == "dice_roll":
            dice_value = random.randint(1, 6) + random.randint(1, 6)
            print("Dice value: " + str(dice_value))
            player1.space += dice_value
            
            # loop back around, pass GO
            if player1.space >= 39:
                player1.space -= 39
                player1.money += 200
            
            # Respond to the landed space
            response['space_type'] = "No type"
            response['announcement'] = "No message"
            respond_to_space(game, board, property_deck, player1, response)
            print(response['announcement'])

            response['player1_space'] = player1.space
            response['player1_money'] = player1.money
            print("Space: " + str(player1.space))
            print("Money: " + str(player1.money))
            player1.save()
            for Property in property_deck.properties.filter(player=player1.ordinal):
                print(Property.name)
                

        game.save()
        board.save()
        property_deck.save()
        return JsonResponse(response)
    
    # Initial HTTP request; setup, page render
    else:
        return render(request, 'monopoly.html')

#*************************************************************************************
"""Event handler for space landing"""
def respond_to_space(game, board, property_deck, player, response):
    space = board.get_space(player.space)
    
    if space.type == "tax":
        response['space_type'] = "tax"
        tax_player(player, space, response)
    elif space.type == "property":
        
        landed_property = property_deck.properties.get(name=space.name)
        respond_to_property(game, landed_property, player, response)
        landed_property.save()


"""Charge a tax to the player"""
def tax_player(player, space, response):
    tax = 0
    if space.name == "Income Tax": tax = 200
    elif space.name == "Luxury Tax": tax = 100
    player.money -= tax
    response['announcement'] = space.name + ": pay $" + str(tax)


"""Either offer to buy the property or charge rent"""
def respond_to_property(game, landed_property, player, response):
    if landed_property.player != player.ordinal:
        buy_price = int(landed_property.prices.split(',')[0])
        player.money -= buy_price
        landed_property.player = player.ordinal
        landed_property.save()
    else:
        rent_price = int(landed_property.rents.split(',')[0])
        player.money += rent_price