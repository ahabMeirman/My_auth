from django.urls import path
from main.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', index, name='index_url'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('log/', MyLoginView.as_view(), name = 'log_url'),
    path('logout/', myLogout, name = 'logout_url'),
    path('addres/', login_required(AddresView.as_view()), name='addres_url'),
]