from django.shortcuts import render

# Create your views here.
def candyland_view(request):
    return render(request, 'candyland.html')