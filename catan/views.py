from django.shortcuts import render
from django.http import JsonResponse
import uuid # unique key for games
import random
from .models.game import Game
from .models.player import Player
from .models.board import Board
from .models.corner import Corner
from .models.tile import Tile
from .view_methods import build_attempt, gather_resources

def catan_view(request):
    # Load game key, or create one if none in session and valueless
    game_key = "no key" # variable, not saved value
    if 'game_key' not in request.session:
        request.session['game_key'] = "no key"
    try: # Game key properly stored as a uuid
        game_key = uuid.UUID(request.session['game_key'])  # Convert string to UUID
    except ValueError: # Game key is not a uuid
        request.session['game_key'] = str(uuid.uuid4())
        game_key = uuid.UUID(request.session['game_key'])
        print(str(game_key))
    
    # Create game objects if none match the key
    if not Game.objects.filter(game_key=game_key).exists():
        game = Game.objects.create(game_key=game_key)
        board = Board.initialize(game_key)
        player1 = Player.objects.create(game_key=game_key, ordinal=1)
        game.save()
        board.save()
        player1.save()
    else: # Load game objects
        game = Game.objects.get(game_key=game_key)
        board = Board.objects.get(game_key=game_key)
        player1 = Player.objects.get(game_key=game_key)

    #*************************************************************************************
    # AJAX POST request; active response
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Get input, initialize response
        input = request.POST.get('input')
        print("input: " + input)
        response = {}
        response['announcement'] = ""

        # Reset data
        if input == "clear_data":
            request.session.clear()
        elif input == "clear_database":
            Game.objects.all().delete()
            Player.objects.all().delete()
            Board.objects.all().delete()
            Corner.objects.all().delete()
            Tile.objects.all().delete()
        elif input == "unload":
            request.session['game_key'] = "no key"
        
        # Corner clicked
        elif input == "corner":
            yindex = request.POST.get('yindex')
            xindex = request.POST.get('xindex')
            build_attempt(board, yindex, xindex, response)
        
        elif input == "end_turn":
            dice_value = random.randint(1, 6) + random.randint(1, 6)
            print("Dice value: " + str(dice_value))
            response['announcement'] += "Dice roll: " + str(dice_value) + "\n"
            gather_resources(board, player1, dice_value, response)
            player1.save()
            game.turn += 1
            
        # Sava game data, return response
        send_inventories(player1, response)
        game.save()
        board.save()
        print(response['announcement'])
        return JsonResponse(response)
    
    # Initial HTTP request, page render
    else:
        return render(request, 'catan.html')

#*************************************************************************************
def send_inventories(player, response):
    players = [player]
    players_data = [{
        'ordinal': player.ordinal,
        'wool': player.wool,
        'grain': player.grain,
        'lumber': player.lumber,
        'brick': player.brick,
        'ore': player.ore,
    } for player in players]

    response['players_data'] = players_data