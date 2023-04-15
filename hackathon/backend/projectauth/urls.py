from django.urls import path
from projectauth.views import UserRegistrationViews,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView

urlpatterns = [
    path('register/',UserRegistrationViews.as_view(),name = 'register'),
    path('login/',UserLoginView.as_view(),name = 'login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changePassword/',UserChangePasswordView.as_view(),name = 'changePassword'),
    path('send-reset-password-email/',SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset-password')
] 