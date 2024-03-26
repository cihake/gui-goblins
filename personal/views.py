from django.shortcuts import render
from account.models import Account
from django.templatetags.static import static  



def home_screen_view(request):
    context = {}
    
    accounts = Account.objects.all()
    context['accounts'] = accounts

    

    return render(request, "personal/home.html", context)

def credits_view(request):
    context = {}
    return render(request, 'personal/credits.html', context)

