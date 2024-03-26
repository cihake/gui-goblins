from django.shortcuts import render

def monopoly_view(request):
    return render(request, 'monopoly.html')
