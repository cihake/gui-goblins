from django.shortcuts import render
from django.http import JsonResponse

def candyland_view(request):
    # AJAX requests
    if (request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        input = request.POST.get('input')
        print(input)
        return JsonResponse({'value': input})
    
    # Initial HTTP request; setup, page render
    else:
        return render(request, 'candyland.html')