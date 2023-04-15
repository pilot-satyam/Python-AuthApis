from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Genrating token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return{
        'refresh' : str(refresh),
        'access' : str(refresh.access_token), 
    }


from projectauth.renderers import UserRenderer

from projectauth.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendResendPasswordSerializer,UserPasswordResetSerializer

# Create your views here.

class UserRegistrationViews(APIView):

    renderer_classes = [UserRenderer]

    # all data from frontend will come from request
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token' : token,'msg' : 'Registration successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
                
#flow --> request send data to serializer then data will get serialized--> then authenticate-->if user present then login
#successful else Unsuccessful
    
class UserLoginView(APIView):

    renderer_classes = [UserRenderer]

    def post(self,request,format = None):
        seriaizer = UserLoginSerializer(data=request.data)
        if(seriaizer.is_valid(raise_exception=True)):
            email = seriaizer.data.get('email')
            password = seriaizer.data.get('password') 
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token' : token,'msg' : "Login Successful"},status=status.HTTP_200_OK)
            else:
                return Response({'errors' : {'non_field_errors' : ['Email or Password Incorrect']}},status=status.HTTP_401_UNAUTHORIZED)
            

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format = None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format = None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg' : "Password Changed Successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format = None):
        serializer = SendResendPasswordSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg' : "Password Reset Link Send Successfully. Please check your email "},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid,token,format = None):
        serializer = UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg' : "Password Reset Successfull"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




