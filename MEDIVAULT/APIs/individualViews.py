import jwt
from .serializers import *
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Set the secret key for JWT token encoding and decoding
JWT_SECRET_KEY = 'secret'

# Set the token expiration time for access token (e.g., 15 minutes)
ACCESS_TOKEN_EXPIRATION_MINUTES = 15

# Set the token expiration time for refresh token (e.g., 30 days)
REFRESH_TOKEN_EXPIRATION_DAYS = 60

# Create your views here.


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        try:
            serializer = IndividualSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                serializer.save()
                return Response({'action': "Add New User", 'message': "User Added Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({'action': "Add User", 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'action': "Add User", 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    try:
        email = request.data['email']
        password = request.data['password']
        user = get_object_or_404(Individual, email=email)

        if check_password(password, user.password):
            # Generate the access token
            access_token_payload = {
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES),
                'iat': datetime.utcnow()
            }
            access_token = jwt.encode(access_token_payload, JWT_SECRET_KEY, algorithm='HS256')

            # Generate the refresh token
            refresh_token_payload = {
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS),
                'iat': datetime.utcnow()
            }
            refresh_token = jwt.encode(refresh_token_payload, JWT_SECRET_KEY, algorithm='HS256')

            return Response({
                'action': "Login",
                'message': "Login Successful",
                'data': {
                    'refresh_token': refresh_token,
                    'access_token': access_token
                }
            }, status=status.HTTP_200_OK)


        else:
            return Response({'action': "Login", 'message': "Incorrect Password"}, status=status.HTTP_401_UNAUTHORIZED)

    except Http404:
        return Response({'action': "Get Login", 'message': 'User Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'action': "Get Login", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def refresh_token(request):
    try:
        refresh_token = request.data['refreshToken']

        # Verify the refresh token
        refresh_token_payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=['HS256'])

        # Check if the refresh token is expired
        if datetime.utcnow() > datetime.fromtimestamp(refresh_token_payload['exp']):
            return Response({'message': 'Refresh token expired'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate a new access token
        access_token_payload = {
            'email': refresh_token_payload['email'],
            'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES),
            'iat': datetime.utcnow()
        }
        access_token = jwt.encode(access_token_payload, JWT_SECRET_KEY, algorithm='HS256')

        return Response({'accessToken': access_token}, status=status.HTTP_200_OK)

    except jwt.ExpiredSignatureError:
        return Response({'message': 'Refresh token expired'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({'message': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
    except KeyError:
        return Response({'message': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)