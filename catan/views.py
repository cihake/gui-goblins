from django.shortcuts import render
from django.http import JsonResponse
import uuid # unique key for games
from .models.game import Game
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
        game.save()
        board.save()
    else: # Load game objects
        game = Game.objects.get(game_key=game_key)
        board = Board.objects.get(game_key=game_key)

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
            Board.objects.all().delete()
            Corner.objects.all().delete()
            Tile.objects.all().delete()
        elif input == "unload":
            request.session['game_key'] = "no key"
            game.turn = 1
        
        # Corner clicked
        elif input == "corner":
            yindex = request.POST.get('yindex')
            xindex = request.POST.get('xindex')
            build_attempt(board, yindex, xindex, response)
            print(response['build_response'])
            if response['build_success'] == 1: game.turn += 1
            """corner = board.corners.get(yindex=yindex, xindex=xindex)
            print ("corner building = " + str(corner.building))
            neighbor_corners = board.get_neighbor_corners(corner)
            y0 = str(neighbor_corners[0].yindex) + ","
            x0 = str(neighbor_corners[0].xindex) + " "
            y1 = str(neighbor_corners[1].yindex) + ","
            x1 = str(neighbor_corners[1].xindex) + " "
            y2 = str(neighbor_corners[2].yindex) + ","
            x2 = str(neighbor_corners[2].xindex) + " "
            print("Corner 0: " + y0 + x0 + "Corner 1: " + y1 + x1 + "Corner 2: " + y2 + x2)
            neighbor_tiles = board.get_neighbor_tiles(corner)
            y0 = str(neighbor_tiles[0].yindex) + ","
            x0 = str(neighbor_tiles[0].xindex) + " "
            terrain0 = "Terrain 0: " + neighbor_tiles[0].terrain + ", "
            y1 = str(neighbor_tiles[1].yindex) + ","
            x1 = str(neighbor_tiles[1].xindex) + " "
            terrain1 = "Terrain 1: " + neighbor_tiles[1].terrain + ", "
            y2 = str(neighbor_tiles[2].yindex) + ","
            x2 = str(neighbor_tiles[2].xindex) + " "
            terrain2 = "Terrain 2: " + neighbor_tiles[2].terrain + ", "
            print("Tile 0: " + y0 + x0 + terrain0 + "Tile 1: " + y1 + x1 + terrain1 + "Tile 2: " + y2 + x2 + terrain2)
            if corner.building == 0:
                corner.building += 1
                corner.save()
                print("Building placed.")
            else:
                print("That corner is occupied.")
            
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
        print ("End of move: turn = " + str(game.turn))
        game.save()
        board.save()
        return JsonResponse(response)
    
    # Initial HTTP request, page render
    else:
        return render(request, 'catan.html')

#*************************************************************************************
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
