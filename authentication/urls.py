from django.urls import path
from authentication.views.user_registration import UserRegistration, UserDetailsView
from authentication.views.user_authentication import Login, Logout

urlpatterns = [
  path('signup/', UserRegistration.as_view(), name='user registration'),
  path('user/<int:pk>/', UserRegistration.as_view(), name='user profile'),
  path('users/', UserDetailsView.as_view(), name='user details'),
  path('login/', Login.as_view(), name='login'),
  path('logout/', Logout.as_view(), name='login'),
]
