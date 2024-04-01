from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from .classes.game import Game
from .classes.board import Board
from .classes.corner import Corner
from .classes.tile import Tile

def catan_view(request):
    # Initialize game data
    if 'game_data' not in request.session:
        game = Game()
        board = Board(15, 8, 7, 7)
        # Serialize and save the data to session
        game_data = {
            'game': game.to_dict(),
            'board': board.to_dict(),
            }
        request.session['game_data'] = json.dumps(game_data, cls=DjangoJSONEncoder)
    else: # Load data from session
        game_data = json.loads(request.session['game_data'])

    #*************************************************************************************
    # AJAX POST request; active response
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Get input, initialize response
        input = request.POST.get('input')
        #print(input)
        response = {}

        if input == "reset":
            # Clear the session cache
            request.session.flush()
            return JsonResponse(response)

        if input == "corner":
            yindex = int(request.POST.get('yindex'))
            xindex = int(request.POST.get('xindex'))
            corner_to_build = game_data['board']['corners'][yindex][xindex]
            corner_y = corner_to_build['yindex']
            corner_x = corner_to_build['xindex']

        # Sava game data, return response
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