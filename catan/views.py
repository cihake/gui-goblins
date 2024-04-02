from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from .classes.game import Game
from .classes.board import Board
from .classes.corner import Corner
from .classes.tile import Tile

def catan_view(request):
    # Initialize game data if not already in session
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
        board = Board.from_dict(game_data['board'])

    #*************************************************************************************
    # AJAX POST request; active response
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Get input, initialize response
        input = request.POST.get('input')
        print(input)
        response = {}

        if input == "reset":
            game.__init__()
            board.initialize_corners(15, 8)
            board.initialize_tiles(7, 7)
        
        if input == "clear_data":
            # Clear the session cache
            response = JsonResponse(response)
            response_sent = response.content  # This forces the response to be fully rendered
            request.session.flush()
            return response

        if input == "corner":
            yindex = int(request.POST.get('yindex'))
            xindex = int(request.POST.get('xindex'))
            corner_to_build = board.corners[yindex][xindex]
            neighbor_corners = board.get_neighbor_corners(corner_to_build)
            neighbor_tiles = board.get_neighbor_tiles(corner_to_build)

        # Sava game data, return response
            
        game_data['game'] = game.to_dict()
        game_data['board'] = board.to_dict(board.corners, board.tiles)
        request.session['game_data'] = json.dumps(game_data, cls=DjangoJSONEncoder)
        return JsonResponse(response)
    
    #*************************************************************************************
    # Initial HTTP request, page render
    else:
        return render(request, 'catan.html')


"""if input == 'corner':
            xindex = request.POST.get('xindex')
            yindex = request.POST.get('yindex')
            corner_to_build = Board.corners
            print("x: " + corner_to_build.xindex + ", y: " + corner_to_build.yindex)
            if corner_to_build.building == 0:
                corner_to_build.building = 1
                Game.build_attempt = "Success!"
                response['build_attempt'] = Game.build_attempt
            else:
                Game.build_attempt = "Something is already built there."
                response['build_attempt'] = Game.build_attempt"""