
from django.contrib import admin
from django.urls import path, include  
from django.conf import settings
from django.conf.urls.static import static
from personal.views import (home_screen_view, credits_view)
from candyland.views import (candyland_view)
from monopoly.views import (monopoly_view)
from catan.views import (catan_view)


from account.views import (
    registration_view,
    logout_view, 
    login_view,
    account_view,
    coin_balance_view,
    leaderboard_view,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name ="home"),
    path('register/', registration_view, name ="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('account/', account_view, name="account"),
    path('credits/', credits_view, name='credits'),
    path('coins/', coin_balance_view, name = 'coins'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('candyland/', candyland_view, name='candyland'),
    path('monopoly/', monopoly_view, name='monopoly'),
    path('catan/', catan_view, name='catan'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

