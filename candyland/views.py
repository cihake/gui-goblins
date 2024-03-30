from django.shortcuts import render
from django.http import JsonResponse

def candyland_view(request):
    # Check if player1_space is present in session
    if 'player1_space' not in request.session:
        # Reset game attributes
        request.session['player1_space'] = 1  # Initialize player1 space attribute

    # Retrieve player1 space attribute from session
    player1_space = request.session['player1_space']
    
    # AJAX POST request; active response
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        input_value = request.POST.get('input')

        request.session['player1_space'] = player1_space  # Update player1 space attribute
        data = {
            'echo': input_value
        }

        return JsonResponse(data)
    
    # Initial page render
    else:
        return render(request, 'candyland.html')