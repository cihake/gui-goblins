from django.shortcuts import render
from django.http import JsonResponse
import uuid # unique key for games
import random, json
from .models.game import Game
from .models.player import Player
from .models.board import Board
from .models.corner import Corner
from .models.tile import Tile
from .view_methods import build_attempt, gather_resources, handle_setup, can_afford, handle_road_build

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
        game = Game.objects.create(game_key=game_key, number_players=1)
        board = Board.initialize(game_key)
        player1 = Player.objects.create(game_key=game_key, ordinal=1, starting_settlements=2)
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
        # In addition to announcements and game data, the response has several flags:
        # build_success, build_type
        response = {}
        response['announcement'] = "Player " + str(player1.ordinal) + "\n"
        if game.setup_flag == 0:
            response['announcement'] += "Turn: " + str(game.turn) + "\n"

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
        
        # Build buttons; each checks for sufficient resources
        # Build settlement button
        elif input == "build_settlement":
            if can_afford(player1, input, response):
                game.build_flag = 1
                response['announcement'] = "Build where?\n"
            else:
                response['announcement'] = ("Not enough resources.\n"
                + "A settlement costs one each of brick, lumber, wool, and grain.")
        # Build road button
        elif input == "build_road":
            if can_afford(player1, input, response):
                game.build_flag = 2 # Road start
                response['announcement'] = "Build where?\n"
            else:
                response['announcement'] = ("Not enough resources.\n"
                + "A road costs one unit of brick and lumber.")
        
        # Corner clicked
        elif input == "corner":
            yindex = request.POST.get('yindex')
            xindex = request.POST.get('xindex')
            # Setup phase
            if game.setup_flag != 0:
                handle_setup(game, board, player1, yindex, xindex, response)
            # Settlement building mode; costs resources; price checked at "build" button
            if game.build_flag == 1:
                response['build_type'] = "settlement"
                build_attempt(game, board, player1, yindex, xindex, response)
                if response['build_success'] == 1:
                    player1.wool -= 1; player1.grain -= 1; player1.lumber -= 1; player1.brick -= 1
                    player1.save()
                    game.build_flag = 0
                    # Victory condition: 10 buildings
                    response['number_buildings'] = 0
                    for Corner in board.corners.all():
                        if Corner.building > 0:
                            response['number_buildings'] += 1
            # Road building mode; two-step process
            elif game.build_flag == 2 or game.build_flag == 3:
                handle_road_build(game, board, player1, yindex, xindex, response)
                
        
        # Tile clicked
        elif input == "tile":
            if game.setup_flag != 0:
                response['announcement'] += "Remaining settlements: " + str(player1.starting_settlements) + "\n"

        # End turn, gather resources
        elif input == "end_turn":
            dice_value = random.randint(1, 6) + random.randint(1, 6)
            print("Dice value: " + str(dice_value))
            response['announcement'] += "Dice roll: " + str(dice_value) + "\n"
            gather_resources(board, player1, dice_value, response)
            player1.save()
            game.build_flag = 0
            game.turn += 1
            
        # Sava game data, return response
        send_inventories(player1, response)
        send_flags(game, response)
        game.save()
        board.save()
        print(response['announcement'])
        return JsonResponse(response)
    
    #*************************************************************************************
    # Initial HTTP request, page render; pass drawing variables
    else:
        draw_data = {}
        
        # Pass terrains as colors
        tile_colors = []
        for y in range(7):
            color_row = []
            for x in range(7):
                terrain = board.tiles.get(yindex=y, xindex=x).terrain
                color = ""
                if terrain == "empty": color = "none"
                elif terrain == "water": color = "darkturquoise"
                elif terrain == "desert": color = "gold"
                elif terrain == "pasture": color = "chartreuse"
                elif terrain == "fields": color = "goldenrod"
                elif terrain == "forest": color = "forestgreen"
                elif terrain == "hills": color = "sienna"
                elif terrain == "mountains": color = "lightslategrey"
                color_row.append(color)
            tile_colors.append(color_row)
        draw_data['tile_colors'] = tile_colors

        # Pass dice values
        tile_dice = []
        for y in range(7):
            dice_row = []
            for x in range(7):
                dice_row.append(board.tiles.get(yindex=y, xindex=x).dice)
            tile_dice.append(dice_row)
        draw_data['tile_dice'] = tile_dice
        
        return render(request, 'catan.html', {'draw_data': json.dumps(draw_data)})

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


def send_flags(game, response):
    response['setup_flag'] = game.setup_flag
    response['build_flag'] = game.build_flag