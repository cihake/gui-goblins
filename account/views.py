from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from .models import Coin, Leaderboard
from .utils import add_coins, add_score

def registration_view(request):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1') 
            account = authenticate(email=email, password=raw_password)
            if account is not None:
                login(request, account)
                # Adds a baseline of 100 coins to every user who registers an account. 
                add_coins(account, 100)
                add_score(account, 0)
                return redirect('home')
            else:
                # Authentication failed
                messages.error(request, "Authentication failed. Please check your email and password.")
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)

def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context['account_form'] = form
    return render(request, 'account/account.html', context)

    # Retreives a Coin object associated with the current user. The Coin.get_or_create()
    # method retrieves or creates a new instance of coins for the user. The [0] retrieves
    # the first element (which is Coin) within the tuple returned by get_or_create().
    # This method returns a render (shortcut function used to render templates) of the
    # coin_balance.html file and passes 'coin' as an object for use in the template. 
def coin_balance_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
        
    coin = Coin.objects.get_or_create(user=request.user)[0]
    return render(request, 'account/coin_balance.html', {'coin': coin})


def leaderboard_view(request):
    leaderboard = Leaderboard.objects.order_by('-score')[:10]  # Get top 10 entries
    return render(request, 'account/leaderboard.html', {'leaderboard': leaderboard})