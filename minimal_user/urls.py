from django.urls import path

from minimal_user.views import home_view, login_view, register_view, logout_view, user_lookup_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('lookup/', user_lookup_view, name='lookup'),
]
