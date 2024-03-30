from django.shortcuts import render
from django.http import JsonResponse
from .models import Player

def candyland_view(request):
    # Initial setup
    player1 = Player(ordinal=1, space=1, skip=False)
    
    # AJAX POST request; active response
    if (request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        input = request.POST.get('input')
        player1.space += 1

        data = {
            'space': player1.space
        }

        return JsonResponse(data)
    
    # Initial page render
    else:
        return render(request, 'candyland.html')
