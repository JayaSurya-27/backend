import jwt
from .serializers import *
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# # Create your views here.
#
#
# @api_view(['POST'])
# def signup(request):
#     if request.method == 'POST':
#         try:
#             serializer = IndividualSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
#                 serializer.save()
#                 return Response({'action': "Add New User", 'message': "User Added Successfully"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'action': "Add User", 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'action': "Add User", 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['POST'])
# def login(request):
#     try:
#         email = request.data['email']
#         password = request.data['password']
#         user = get_object_or_404(Individual, email=email)
#
#         if check_password(password, user.password):
#             payload = {
#                 'id': user.id,
#                 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
#                 'iat': datetime.datetime.utcnow()
#             }
#
#             token = jwt.encode(payload, 'secret', algorithm='HS256')
#
#             response = Response({'action': "Login", 'message': "Login Successful"}, status=status.HTTP_200_OK)
#             response.set_cookie(key='jwt', value=token, httponly=True)
#             response.data = {'jwt': token}
#             return response
#         else:
#             return Response({'action': "Login", 'message': "Incorrect Password"}, status=status.HTTP_401_UNAUTHORIZED)
#
#     except Http404:
#         return Response({'action': "Get Login", 'message': 'User Not Found'},
#                         status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({'action': "Get Login", 'message': str(e)},
#                         status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET'])
# def userView(request):
#     token = request.COOKIES.get('jwt')
#
#     if not token:
#         return Response({'action': "Get User", 'message': "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
#
#     try:
#         payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         user = Individual.objects.filter(id=payload['id']).first()
#         serializer = IndividualSerializer(user)
#         return Response(serializer.data)
#
#     except jwt.ExpiredSignatureError:
#         return Response({'action': "Get User", 'message': "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)
#



# Set the secret key for JWT token encoding and decoding
JWT_SECRET_KEY = 'secret'

# Set the token expiration time for access token (e.g., 15 minutes)
ACCESS_TOKEN_EXPIRATION_MINUTES = 15

# Set the token expiration time for refresh token (e.g., 30 days)
REFRESH_TOKEN_EXPIRATION_DAYS = 60


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
                'id': user.id,
                'exp': datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRATION_MINUTES),  #change to minutes
                'iat': datetime.utcnow()
            }
            access_token = jwt.encode(access_token_payload, JWT_SECRET_KEY, algorithm='HS256')

            # Generate the refresh token
            refresh_token_payload = {
                'id': user.id,
                'exp': datetime.utcnow() + timedelta(seconds=REFRESH_TOKEN_EXPIRATION_DAYS), #change to days
                'iat': datetime.utcnow()
            }
            refresh_token = jwt.encode(refresh_token_payload, JWT_SECRET_KEY, algorithm='HS256')

            # Set the tokens in cookies
            response = Response({'action': "Login", 'message': "Login Successful"}, status=status.HTTP_200_OK)
            response.set_cookie(key='access_token', value=access_token, httponly=True)
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
            return response
        else:
            return Response({'action': "Login", 'message': "Incorrect Password"}, status=status.HTTP_401_UNAUTHORIZED)

    except Http404:
        return Response({'action': "Get Login", 'message': 'User Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'action': "Get Login", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def userView(request):
    access_token = request.COOKIES.get('access_token')

    if not access_token:
        return Response({'action': "Get User", 'message': "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        access_token_payload = jwt.decode(access_token, JWT_SECRET_KEY, algorithms=['HS256'])
        user = Individual.objects.filter(id=access_token_payload['id']).first()
        serializer = IndividualSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError:
        return Response({'action': "Get User", 'message': "Access token expired"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({'action': "Get User", 'message': "Invalid access token"}, status=status.HTTP_401_UNAUTHORIZED)

