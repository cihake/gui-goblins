from django.shortcuts import render  # Importing render function from Django for rendering templates
from account.models import Account  # Importing Account model from the account app's models
from django.templatetags.static import static  # Importing static function from Django for serving static files

# View function for the home screen
def home_screen_view(request):
    context = {}  # Initializing an empty context dictionary
    
    # Retrieving all accounts from the database
    accounts = Account.objects.all()
    
    # Adding the retrieved accounts to the context dictionary
    context['accounts'] = accounts

    # Rendering the home.html template with the context data and returning the rendered template
    return render(request, "personal/home.html", context)

# View function for the credits page
def credits_view(request):
    context = {}  # Initializing an empty context dictionary
    
    # Rendering the credits.html template with an empty context and returning the rendered template
    return render(request, 'personal/credits.html', context)
