from django.shortcuts import render
from django.http import JsonResponse
from .models.game import Game
#from .models import Game, Board, Corner, Tile
"""from django.core.serializers.json import DjangoJSONEncoder
import json
from .classes.game import Game
from .classes.board import Board
from .classes.corner import Corner
from .classes.tile import Tile"""

def catan_view(request):
    """# Initialize game data if not already in session
    if 'game_data' not in request.session:
        game = Game()
        board = Board(Board.initialize_corners(15, 8), Board.initialize_tiles(7, 7))
        # Serialize and save the data to session
        game_data = {
            'game': game.to_dict(),
            'board': board.to_dict(board.corners, board.tiles),
        }
        request.session['game_data'] = json.dumps(game_data, cls=DjangoJSONEncoder)
    else: # Load data from session
        game_data = json.loads(request.session['game_data'])
        game = Game(**game_data['game'])
        board = Board.from_dict(game_data['board'])"""

    #*************************************************************************************
    # AJAX POST request; active response
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Get input, initialize response
        input = request.POST.get('input')
        print(input)
        response = {}

        """# Handle different AJAX requests
        if input == "clear_data":
            # Clear the session cache
            request.session.clear()
        
        elif input == "reset":
            # Reset the game data and store it in the session
            board = Board.initialize(15, 8, 7, 7)
            request.session['board_id'] = board.id
        
        elif input == "corner":
            # Handle corner interaction
            # Example: increment building count
            corner_id = int(request.POST.get('corner_id'))
            corner = Corner.objects.get(pk=corner_id)
            corner.building += 1
            corner.save()
            response['message'] = "Corner building count incremented."
        
        elif input == "tile":
            # Handle tile interaction
            # Example: log terrain
            tile_id = int(request.POST.get('tile_id'))
            tile = Tile.objects.get(pk=tile_id)
            response['terrain'] = tile.terrain
        else:
            response['error'] = "Invalid input."

        return JsonResponse(response)

        if input == "clear_data":
            # Clear the session cache
            response = JsonResponse(response)
            response_sent = response.content  # This forces the response to be fully rendered
            request.session.flush()
            return response

        if input == "reset":
            game.__init__()
            board.initialize_corners(15, 8)
            board.initialize_tiles(7, 7)

        if input == "corner":
            yindex = int(request.POST.get('yindex'))
            xindex = int(request.POST.get('xindex'))
            print(board.corners[yindex][xindex].building)
            board.corners[yindex][xindex].building += 1
            print(board.corners[yindex][xindex].building)

        if input == "tile":
            yindex = int(request.POST.get('yindex'))
            xindex = int(request.POST.get('xindex'))
            tile_to_check = board.tiles[yindex][xindex]
            print (tile_to_check.terrain)

        # Sava game data, return response
            
        game_data['game'] = game.to_dict()
        game_data['board'] = board.to_dict(board.corners, board.tiles)
        request.session['game_data'] = json.dumps(game_data, cls=DjangoJSONEncoder)"""
        return JsonResponse(response)
    
    # Initial HTTP request, page render
    else:
        return render(request, 'catan.html')

#*************************************************************************************
"""The corner is buildable if it isn't build, its corner neighbors aren't built,
and at least one of its neighbors is a land tile"""
"""def build_attempt(board, yindex, xindex):
    board.corners[yindex][xindex].building += 1
    corner_to_build = board.corners[yindex][xindex]
    if corner_to_build.building == 1:
        return "That corner already has a building on it."
    
    neighbor_tiles = board.get_neighbor_tiles(corner_to_build)
    touching_land = False
    for i in neighbor_tiles:
        terrain = neighbor_tiles[i].terrain
        print(terrain)
        if (terrain == "forest" or terrain == "pasture" or terrain == "fields"
        or terrain == "hills" or terrain == "mountains"):
            touching_land = True
    if touching_land == False:
        return "The building must be near land."
    
    neighbor_corners = board.get_neighbor_corners(corner_to_build)
    for i in neighbor_corners:
        if neighbor_corners[i].building != 0:
            return ("You must build at least two intersections away from another building,"
            "as per the neighbor rule.")
    
    return "Built successfully"""
