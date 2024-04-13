from django.shortcuts import render
from django.http import JsonResponse
import uuid # unique key for games
import math, random
from .models.game import Game
from .models.player import Player

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
        game.save()
        player1.save()
    else: # Load game objects
        game = Game.objects.get(game_key=game_key)
        player1 = Player.objects.get(game_key=game_key, ordinal=1)
    
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
            player1.space += dice_value
            
            # loop back around, pass GO
            if player1.space >= 39:
                player1.space -= 39
                player1.money += 200
            
            player1.save()
            response['player1_space'] = player1.space
            response['player1_money'] = player1.money
            print("Space: " + str(player1.space))
            print("Money: " + str(player1.money))
        
        game.save()
        return JsonResponse(response)
    
    # Initial HTTP request; setup, page render
    else:
        return render(request, 'monopoly.html')

#*************************************************************************************
