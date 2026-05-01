from django.urls import path
from .views import RegisterView, LoginView, UserListView, UserStatusUpdateView, UserPasswordResetView, UserProfileView, ChangePasswordView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('list/', UserListView.as_view()),
    path('status/', UserStatusUpdateView.as_view()),
    path('password/', UserPasswordResetView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
]