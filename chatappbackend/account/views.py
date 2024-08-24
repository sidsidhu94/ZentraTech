from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserCreateSerializer 
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from .models import UserAccount
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError



    


class RegisterView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

         
        email = request.data.get('email')
        username = request.data.get('username')

        if UserAccount.objects.filter(email=email).exists():
            return Response({"error": "An account with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if UserAccount.objects.filter(username=username).exists():
            return Response({"error": "An account with this username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            user = serializer.save()
            
            user.save()

          
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = request.build_absolute_uri(
                reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
            )

            
            send_mail(
                'Verify your email',
                f'Click the link to verify your email: {verification_link}',
                'no-reply@myapp.com',
                [user.email],
            )

            return Response({"message": "Registration successful. Please check your email to verify your account."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserAccount.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserAccount.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
           
            return render(request,"activatesuccess.html")

            
        else:
            return Response(
                {"error": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    



class LoginView(APIView):
    

    def post(self,request):
        
        if request.method =="POST":
            email =request.data['email']
            
            password = request.data['password']

            print(email,password)

            user = UserAccount.objects.filter(email = email).first()
            print(user)

            if user is not None and user.is_active == False:
                return Response({"message":"Please check your mail and verify"})

            if user is None or user.delete == True :
                return Response({"message":"Not a registered user please  register "})
            
            if not user.check_password(password):
                return Response({"message":"Incorrect Password"})
            

        refresh = RefreshToken.for_user(user)

        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': "login successful",
            "name": user.name,  
            "user_id": user.id
        }

        return Response(response_data, status=status.HTTP_200_OK)
    




class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(data = {"message": "error  "}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message": "Something went wrong, please try again"}, status=status.HTTP_400_BAD_REQUEST)
