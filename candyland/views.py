from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def candyland_view(request):
    # AJAX requests
    if (request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        try:
            input = request.POST.get('input')
            print(input)
            return JsonResponse({'value': input})
        except Exception as e:
            print("Error processing AJAX request:", e)
            return JsonResponse({'error': 'An error occurred while processing your request'}, status=500)
    
    # Initial HTTP request; setup, page render
    else:
        return render(request, 'candyland.html')