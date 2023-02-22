from django.urls import path

from .views import starting_page, post_login, perform_logout

urlpatterns = [
    path('', starting_page, name="main-page"),
    path('login/', post_login, name="post-login"),
    path('logout/', perform_logout, name="post-logout"),
]
