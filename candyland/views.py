from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from account.models import Coin, Account, Leaderboard
from django.urls import reverse

def candyland_view(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the user has enough coins
        try:
            coin_balance = Coin.objects.get(user=request.user).amount
            if coin_balance < 10:
                return redirect('store')  # Redirect to a page indicating insufficient coins
        except Coin.DoesNotExist:
            return redirect('register')  # Redirect to register page if user doesn't have a Coin object
    else:
        return redirect('register')  # Redirect unauthenticated users to register page

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

        if request.session['position'] >= 132:
            # Add 15 coins for winning
            coin_balance += 15
            # Update the coin balance
            Coin.objects.filter(user=request.user).update(amount=coin_balance)
            # Redirect to the home screen after winning
            return JsonResponse({'redirect': reverse('home')})

        return JsonResponse({'echo': input_data})

    # Initial HTTP request
    else:
        # Deduct 10 coins from the user's balance
        coin_balance -= 10
        Coin.objects.filter(user=request.user).update(amount=coin_balance)
        return render(request, 'candyland.html')
