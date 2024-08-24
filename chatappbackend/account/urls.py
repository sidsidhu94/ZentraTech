from django.urls import path
from .views import  LoginView, RegisterView, VerifyEmailView,LogoutView

urlpatterns = [
    
    path("login/", LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),

    path('logout/',LogoutView.as_view()),
]
