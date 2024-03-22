from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def candyland_view(request):
    # AJAX requests
    if (request.is_ajax() and request.method == 'POST'):
        # Get the kind of button press from the listener
        button = request.POST.get('button')

        if (button == "draw_card"):
            winner = 1
        if (winner == 1):
            # Send the "winner" value to the responder
            return JsonResponse({'value': winner})
        
    else: # Initial HTTP request; setup, page render
        winner = 0
        return render(request, 'candyland.html')