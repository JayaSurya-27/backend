import jwt
from .serializers import *
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

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
                    'access_token': access_token,
                    'id': user.id,
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
def refresh_access_token(request):
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


@api_view(['POST'])
def is_authenticated(request):
    access_token = request.data['accessToken']

    try:
        # Verify the access token
        access_token_payload = jwt.decode(access_token, JWT_SECRET_KEY, algorithms=['HS256'])

        # Check if the access token is expired
        if datetime.utcnow() > datetime.fromtimestamp(access_token_payload['exp']):
            return Response({'message': 'Access token expired'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'message': 'User is authenticated'}, status=status.HTTP_200_OK)

    except jwt.ExpiredSignatureError:
        return Response({'message': 'Access token expired'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({'message': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)
    except KeyError:
        return Response({'message': 'Access token not provided'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_file(request):
    if request.method == 'POST':
        try:
            serializer = FileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'action': "Upload File", 'message': "File Uploaded Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({'action': "Upload File", 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'action': "Upload File", 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # If the request method is not POST
    return Response({'error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_files(request):
    if request.method == 'GET':
        try:
            file_id = request.GET.get('id')
            file_data = Files.objects.filter(owner=file_id)
            serializer = GetFileSerializer(file_data, many=True)
            return Response({'action': 'Get Files', 'message': 'Data Found', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        except Files.DoesNotExist:
            return Response({'action': 'Get Files', 'message': 'No Files Found'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'action': 'Get Files', 'message': 'Something went wrong'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def download_file(request, file_id):
    try:
        # Retrieve the file object from the database or file storage
        file_object = Files.objects.get(id=file_id)

        # Get the file path
        file_path = os.path.join(settings.MEDIA_ROOT, file_object.file.name)

        # Check if the file exists
        if os.path.exists(file_path):
            # Open the file in binary mode
            with open(file_path, 'rb') as f:
                # Create the HTTP response with the file content
                response = HttpResponse(f.read(), content_type='application/octet-stream')

                # Set the response headers for file download
                response['Content-Disposition'] = f'attachment; filename="{file_object.file.name}"'
                return response
        else:
            raise Http404("File does not exist.")

    except Files.DoesNotExist:
        raise Http404("File does not exist.")