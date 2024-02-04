
from django.urls import path
from . views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileUpdateView, profile

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('profile/', ProfileView.as_view(), name = 'profile'),
    path('profile/', profile, name = 'profile'),
    path('profile/edit', UserProfileUpdateView.as_view(), name = 'edit_profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]