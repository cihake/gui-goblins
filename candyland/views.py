from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from account.models import Coin, Account, Leaderboard
from django.urls import reverse


def candyland_view(request):
    if request.user.is_authenticated:
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

        if request.session['position'] >= 132 and input_data == 'win':
            coin_balance += 300  # Add 15 coins for winning
            Coin.objects.filter(user=request.user).update(amount=coin_balance)

        return JsonResponse({'echo': input_data})
    # Initial HTTP request
    else:
        Coin.objects.filter(user=request.user).update(amount=coin_balance - 10)
        return render(request, 'candyland.html')
