from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User, Profile, Company
from .serializers import UserSerializer,ProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        company_name = data.get('company')


        company, _ = Company.objects.get_or_create(name=company_name.lower())


        user = User.objects.create_user(email=email, password=password, company=company)
       
        Profile.objects.create(
            user=user, 
            full_name=data.get('full_name'), 
            role=data.get('role'), 
            company=company
        )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        
        return Response(
            {
                "message": "User registered successfully!",
                "access": access_token,
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED
        )

class LoginAPIView(TokenObtainPairView):
    pass



class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    

    def get_object(self):
        return self.request.user.profile
    
    def update(self, request, *args,**kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
