from django.urls import path
from .views import HelloWorldView, LoginView, RegisterView, VerifyEmailView,LogoutView

urlpatterns = [
    path("hello/", HelloWorldView.as_view(), name="hello-world"),
    path("login/", LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    # path('userlogout/',UserLogoutView.as_view()),
    path('logout/',LogoutView.as_view()),
]
