from django.shortcuts import render
from django.http import JsonResponse

def candyland_view(request):
    # Initialize variables
    if 'position' not in request.session:
        request.session['position'] = 1

    # Handle AJAX POST request
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        input_data = request.POST.get('input')
        
        # Reset the game variables
        if input_data == 'reset':
            request.session['position'] = 1  # Reset position
            return JsonResponse({'status': 'reset'})

        request.session['position'] += 1  # Increment position
        return JsonResponse({'echo': input_data})

    # Initial HTTP request
    else:
        return render(request, 'candyland.html')