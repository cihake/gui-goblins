from django.shortcuts import render
from django.http import JsonResponse
import uuid # unique key for games
import random
from .models.game import Game
from .models.player import Player
from .models.board import Board
from .models.corner import Corner
from .models.tile import Tile

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
    
    # Create game objects if none match the key
    if not Game.objects.filter(game_key=game_key).exists():
        game = Game.objects.create(game_key=game_key)
        board = Board.initialize(game_key, 15, 8, 7, 7)
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
            print(response['build_response'])
        
        elif input == "end_turn":
            gather_resources(board, player1, response)
            player1.save()
            game.turn += 1
            
        # Sava game data, return response
        send_inventories(player1, response)
        game.save()
        board.save()
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


"""The corner is buildable if it isn't build, its corner neighbors aren't built,
and at least one of its neighbors is a land tile"""
def build_attempt(board, yindex, xindex, response):
    corner_to_build = board.corners.get(yindex=yindex, xindex=xindex)
    
    # Check if already built
    if corner_to_build.building == 1:
        response['build_success'] = 0
        response['build_response'] = "That corner already has a building on it."
        return
    
    # Land check
    neighbor_tiles = board.get_neighbor_tiles(corner_to_build)
    touching_land = False
    for Tile in neighbor_tiles:
        terrain = Tile.terrain
        if (terrain == "forest" or terrain == "pasture" or terrain == "fields"
        or terrain == "hills" or terrain == "mountains"):
            touching_land = True
    if touching_land == False:
        response['build_success'] = 0
        response['build_response'] = "The building must be near land."
        return
    
    # Neighbors check
    neighbor_corners = board.get_neighbor_corners(corner_to_build)
    for Corner in neighbor_corners:
        building = Corner.building
        if building != 0:
            response['build_success'] = 0
            response['build_response'] = ("You must build at least two intersections"
            "away from another building, as per the neighbor rule.")
            return
    
    # Successful build
    corner_to_build.building = 1
    corner_to_build.save()
    response['build_success'] = 1
    response['build_response'] = "Built successfully"
    return


"""At the start of a turn, for every corner that is built, check the adjacent tiles.
If the tile's dice value matches the dice roll, add the corresponding terrain resource
to the corresponding player."""
def gather_resources(board, player, response):
    dice_value = random.randint(1, 6) + random.randint(1, 6)
    print("Dice value: " + str(dice_value))

    for Corner in board.corners.all():
        if Corner.building > 0:
            for Tile in board.get_neighbor_tiles(Corner):
                if Tile.dice == dice_value:
                    terrain = Tile.terrain
                    if terrain == "pasture":
                        player.wool += 1
                        print("Wool gathered")
                    elif terrain == "fields":
                        player.grain += 1
                        print("Grain gathered")
                    elif terrain == "forest":
                        player.lumber += 1
                        print("Lumber gathered")
                    elif terrain == "hills":
                        player.brick += 1
                        print("Brick gathered")
                    elif terrain == "mountains":
                        player.ore += 1
                        print("Ore gathered")
    print(player.__str__())