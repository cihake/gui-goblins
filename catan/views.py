from django.shortcuts import render
from django.http import JsonResponse
import uuid # unique key for games
import random, json
from .models.game import Game
from .models.player import Player
from .models.board import Board
from .models.corner import Corner
from .models.tile import Tile
from .view_methods import build_attempt, gather_resources, handle_setup, can_afford, handle_road_build, city_attempt, move_attempt, steal_resource

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
        game = Game.initialize(game_key, 1, 2)
        board = Board.initialize(game_key, True)
        current_player = game.players.get(ordinal=1)
        game.save()
        board.save()
    else: # Load game objects
        game = Game.objects.get(game_key=game_key)
        board = Board.objects.get(game_key=game_key)
        current_ordinal = (game.turn - 1) % game.number_players + 1
        previous_ordinal = (game.turn - 2) % game.number_players + 1
        current_player = game.players.get(ordinal=current_ordinal)
        previous_player = game.players.get(ordinal=previous_ordinal)
        game.current_player = current_ordinal; game.previous_player = previous_ordinal; game.save()

    #*************************************************************************************
    # AJAX POST request; active response
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Get input, initialize response
        input = request.POST.get('input')
        print("input: " + input)
        # In addition to announcements and game data, the response has several flags:
        # build_success, build_type
        response = {}
        response['announcement'] = ""
        response['build_success'] = 0
        send_start_flags(game, response)

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

        # Cancel button, for several actions
        elif input == "cancel":
            game.build_flag = 0
        
        # Build buttons; each checks for sufficient resources
        # Build settlement button
        elif input == "build_settlement":
            if True:#can_afford(current_player, input, response):
                game.build_flag = 1
                response['can_afford'] = True
                response['announcement'] = "Build where?\n"
            else:
                response['can_afford'] = False
                response['announcement'] = ("Not enough resources.\n"
                + "A settlement costs one each of brick, lumber, wool, and grain.")
        # Build road button
        elif input == "build_road":
            if True:#can_afford(current_player, input, response):
                game.build_flag = 2 # Road start
                response['can_afford'] = True
                response['announcement'] = "Build where?\n"
            else:
                response['can_afford'] = False
                response['announcement'] = ("Not enough resources.\n"
                + "A road costs one unit of brick and lumber.")
        elif input == "build_city":
            if True:#can_afford(current_player, input, response):
                game.build_flag = 4
                response['can_afford'] = True
                response['announcement'] = "Build where?\n"
            else:
                response['can_afford'] = False
                response['announcement'] = ("Not enough resources.\n"
                + "A city costs three ore and two grain.")
        

        # Corner clicked
        elif input == "corner":
            yindex = request.POST.get('yindex')
            xindex = request.POST.get('xindex')
            # Setup phase
            if game.setup_flag != 0:
                handle_setup(game, board, current_player, yindex, xindex, response)
            # Settlement building mode; costs resources; price checked at "build" button
            if game.build_flag == 1:
                response['build_type'] = "settlement"
                build_attempt(game, board, current_player, yindex, xindex, response)
                if response['build_success'] == 1:
                    current_player.wool -= 1; current_player.grain -= 1; current_player.lumber -= 1; current_player.brick -= 1
                    current_player.save()
                    game.build_flag = 0
                    # Victory condition: 10 buildings
                    response['number_buildings'] = 0
                    for Corner in board.corners.all():
                        if Corner.building > 0:
                            response['number_buildings'] += 1
            # Road building mode; two-step process
            elif game.build_flag == 2 or game.build_flag == 3:
                handle_road_build(game, board, current_player, yindex, xindex, response)
            # City building mode; rather simple
            elif game.build_flag == 4:
                response['build_type'] = "city"
                city_attempt(board, current_player, yindex, xindex, response)
                if response['build_success'] == 1:
                    current_player.grain -= 2; current_player.ore -= 3; current_player.save()
                
        

        # Tile clicked
        elif input == "tile":
            yindex = request.POST.get('yindex')
            xindex = request.POST.get('xindex')
            
            if game.setup_flag != 0:
                response['announcement'] += "Remaining settlements: " + str(current_player.starting_settlements) + "\n"

            # Move the robber, if the game is in that phase, and advance the turn
            if game.robber_flag == 1:
                move_attempt(game, board, yindex, xindex, response)
                # Steal from other players, if successfully moved
                if response['move_success'] == 1:
                    steal_resource(game, board, current_player, yindex, xindex, response)
                    


        # End turn, gather resources
        elif input == "end_turn":
            game.build_flag = 0
            dice_value = random.randint(1, 6) + random.randint(1, 6)
            response['announcement'] += "Dice roll: " + str(dice_value) + "\n"
            # Regular gather response
            if dice_value != 7:
                game.turn += 1
                gather_resources(game, board, dice_value, response)
            # Special robber case
            else:
                game.robber_flag = 1
                response['announcement'] += ("The robber moves! Choose which tile to move the robber to.\n")
        

        # Sava game data, return response
        send_inventories(game, response)
        send_flags(game, response)
        game.save()
        board.save()
        update_turn_display(game, response)
        print(response['announcement'])
        return JsonResponse(response)
    
    #*************************************************************************************
    # Initial HTTP request, page render; pass drawing variables
    else:
        draw_data = {}
        
        send_tiles(board, draw_data)
        
        return render(request, 'catan.html', {'draw_data': json.dumps(draw_data)})

#*************************************************************************************
def send_tiles(board, draw_data):
    # Pass terrains as colors
    tile_colors = []
    for y in range(7):
        color_row = []
        for x in range(7):
            terrain = board.tiles.get(yindex=y, xindex=x).terrain
            color = ""
            if terrain == "empty": color = "none"
            elif terrain == "water": color = "darkturquoise"
            elif terrain == "desert": color = "yellow"
            elif terrain == "pasture": color = "chartreuse"
            elif terrain == "fields": color = "gold"
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

def send_inventories(game, response):
    players_data = [{
        'ordinal': player.ordinal,
        'wool': player.wool,
        'grain': player.grain,
        'lumber': player.lumber,
        'brick': player.brick,
        'ore': player.ore,
    } for player in game.players.all()]

    response['players_data'] = players_data

def send_flags(game, response):
    response['setup_flag'] = game.setup_flag
    response['build_flag'] = game.build_flag
    response['robber_flag'] = game.robber_flag
    response['current_player'] = game.current_player
    response['previous_player'] = game.previous_player

def send_start_flags(game, response):
    response['robber_flag_start'] = game.robber_flag

def update_turn_display(game, response):
    current_ordinal = (game.turn - 1) % game.number_players + 1
    player_string = "Player " + str(current_ordinal) + "\n"
    if game.setup_flag == 0:
        announcement = player_string + "Turn: " + str(game.turn) + "\n" + response['announcement']
        response['announcement'] = announcement
    elif response['build_success'] != 1:
        announcement = player_string + response['announcement']
        response['announcement'] = announcement
