from django.shortcuts import render

def catan_view(request):
    return render(request, 'catan.html')
