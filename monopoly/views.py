from django.shortcuts import render
from django.http import JsonResponse
import uuid # unique key for games
from .models.game import Game

def monopoly_view(request):
    # Load game key, or create one if none in session and valueless
    game_key = "no key"
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
        game.save()
    else: # Load game objects
        game = Game.objects.get(game_key=game_key)
    
    # AJAX POST request; active response
    if (request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        input = request.POST.get('input')
        print(input)

        # Reset data
        if input == "clear_data":
            request.session.clear()
        elif input == "clear_database":
            Game.objects.all().delete()
        elif input == "reload":
            request.session['game_key'] = "no key"
            game.turn = 1

        return JsonResponse({'echo': input})
    
    # Initial HTTP request; setup, page render
    else:
        return render(request, 'monopoly.html')
