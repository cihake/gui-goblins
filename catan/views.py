from django.shortcuts import render
from django.http import JsonResponse

def catan_view(request):
    # AJAX POST request; active response
    if (request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        input = request.POST.get('input')
        print(input)

        return JsonResponse({'echo': input})
    
    # Initial HTTP request; setup, page render
    else:
        return render(request, 'catan.html')
