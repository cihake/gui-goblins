from django.shortcuts import render, redirect  # Importing render and redirect functions for rendering templates and redirecting requests
from django.contrib.auth import login, authenticate, logout  # Importing login, authenticate, and logout functions for user authentication
from django.contrib import messages  # Importing messages module for displaying error messages
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm  # Importing custom forms for user registration, authentication, and account update
from .models import Account, Coin, Leaderboard  # Importing Coin and Leaderboard models from the current app's models
from .utils import add_coins, add_score  # Importing custom utility functions for adding coins and score to user's account
from django.http import JsonResponse
import json

# View for user registration.
def registration_view(request):
    context = {}  # Initialize context dictionary for passing data to template
    if request.method == 'POST':  # Check if form is submitted via POST method
        form = RegistrationForm(request.POST)  # Instantiate RegistrationForm with POST data
        if form.is_valid():  # Check if form data is valid
            form.save()  # Save user registration data to database
            email = form.cleaned_data.get('email')  # Extract cleaned email data from form
            raw_password = form.cleaned_data.get('password1')  # Extract cleaned password data from form
            account = authenticate(email=email, password=raw_password)  # Authenticate user
            if account is not None:  # If authentication is successful
                login(request, account)  # Log in the user
                # Adds a baseline of 100 coins to every user who registers an account.
                add_coins(account, 100)  # Add coins to the user's account
                add_score(account, 0)  # Add score to the user's account
                return redirect('home')  # Redirect to home page
            else:
                # Authentication failed
                messages.error(request, "Authentication failed. Please check your email and password.")
        else:
            context['registration_form'] = form  # Pass invalid form data to context for rendering
    else:
        form = RegistrationForm()  # Instantiate empty RegistrationForm for rendering
        context['registration_form'] = form  # Pass empty form to context for rendering
    return render(request, 'account/register.html', context)  # Render registration page with context data


# View for user logout.
def logout_view(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to home page


# View for user login.
def login_view(request):
    context = {}  # Initialize context dictionary for passing data to template

    user = request.user  # Get the current user
    if user.is_authenticated:  # If user is already authenticated
        return redirect('home')  # Redirect to home page

    if request.POST:  # If form is submitted via POST method
        form = AccountAuthenticationForm(request.POST)  # Instantiate AccountAuthenticationForm with POST data
        if form.is_valid():  # Check if form data is valid
            email = request.POST['email']  # Extract email from POST data
            password = request.POST['password']  # Extract password from POST data
            user = authenticate(email=email, password=password)  # Authenticate user
            if user:  # If user authentication is successful
                login(request, user)  # Log in the user
                return redirect('home')  # Redirect to home page
    else:
        form = AccountAuthenticationForm()  # Instantiate empty AccountAuthenticationForm for rendering

    context['login_form'] = form  # Pass form data to context for rendering
    return render(request, 'account/login.html', context)  # Render login page with context data


# View for user account details.
def account_view(request):
    if not request.user.is_authenticated:  # If user is not authenticated
        return redirect("login")  # Redirect to login page

    context = {}  # Initialize context dictionary for passing data to template

    if request.POST:  # If form is submitted via POST method
        form = AccountUpdateForm(request.POST, instance=request.user)  # Instantiate AccountUpdateForm with POST data
        if form.is_valid():  # Check if form data is valid
            form.save()  # Save updated account details to database
    else:
        # Populate form with initial data from user's account
        form = AccountUpdateForm(initial={"email": request.user.email, "username": request.user.username})

    context['account_form'] = form  # Pass form data to context for rendering
    return render(request, 'account/account.html', context)  # Render account page with context data


# View for displaying user's coin balance.
def coin_balance_view(request):
    if not request.user.is_authenticated:  # If user is not authenticated
        return redirect("login")  # Redirect to login page
        
    coin = Coin.objects.get_or_create(user=request.user)[0]  # Get or create Coin object for the user
    return render(request, 'account/coin_balance.html', {'coin': coin})  # Render coin balance page with coin object


# View for displaying leaderboard.
def leaderboard_view(request):
    leaderboard = Leaderboard.objects.order_by('-wins')[:10]  # Get top 10 leaderboard entries
    return render(request, 'account/leaderboard.html', {'leaderboard': leaderboard})  # Render leaderboard page with leaderboard data

def store_view(request):
    coin_prices = {
        'gold': 100.00,
        'silver': 50.00,
        'bronze': 10.00
    }

    if request.method == 'POST':
        data = json.loads(request.body)  # Parse the request body JSON data
        coin_id = data.get('coin_id')  # Get the coin ID from the request body
        
        coin_price = coin_prices.get(coin_id)
        if coin_price is None:
            return JsonResponse({'success': False, 'error': 'Invalid coin ID'})

        try:
            coin_balance = Coin.objects.get(user=request.user).amount
            Coin.objects.filter(user=request.user).update(amount=coin_balance + coin_price)
            return JsonResponse({'success': True})  # Return success response
        except Coin.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'No coins found for the user'})  # Return error response

    # Render the store page if it's a GET request
    context = {
        'gold_price': coin_prices['gold'],
        'silver_price': coin_prices['silver'],
        'bronze_price': coin_prices['bronze']
    }
    return render(request, 'account/store.html', context)
