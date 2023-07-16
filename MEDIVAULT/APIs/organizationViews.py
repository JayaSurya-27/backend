import jwt
from .serializers import *
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

JWT_SECRET_KEY = 'secret'
ACCESS_TOKEN_EXPIRATION_MINUTES = 15
REFRESH_TOKEN_EXPIRATION_DAYS = 60


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        try:
            serializer = OrganizationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                serializer.save()
                return Response({'action': "Add New Organization", 'message': "Organization Added Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({'action': "Add Organization", 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'action': "Add User", 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    try:
        email = request.data['email']
        password = request.data['password']
        org = get_object_or_404(Organization, email=email)

        if check_password(password, org.password):
            access_token_payload = {
                'email': org.email,
                'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES),
                'iat': datetime.utcnow()
            }
            access_token = jwt.encode(access_token_payload, JWT_SECRET_KEY, algorithm='HS256')

            # Generate the refresh token
            refresh_token_payload = {
                'email': org.email,
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
                    'id': org.id,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'action': "Login", 'message': "Incorrect Password"}, status=status.HTTP_401_UNAUTHORIZED)

    except Http404:
        return Response({'action': "Get Login", 'message': 'Organization Not Found'},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'action': "Get Login", 'message': str(e)},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_file(request):
    if request.method == 'POST':
        try:
            serializer = FileRequestSerializer(data=request.data)
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
            org = get_object_or_404(Organization, id=file_id)
            file_data = FileRequest.objects.filter(organization=org)
            serializer = GetFileRequestSerializer(file_data, many=True)
            return Response({'action': 'Get Files', 'message': 'Data Found', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        except Organization.DoesNotExist:
            return Response({'action': 'Get Files', 'message': 'Organization Not Found'},
                            status=status.HTTP_404_NOT_FOUND)
        except FileRequest.DoesNotExist:
            return Response({'action': 'Get Files', 'message': 'No Files Found'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'action': 'Get Files', 'message': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def check_user(request):
    try:
        owner = request.GET.get('owner')
        user = get_object_or_404(Individual, id=owner)
        if user:
            return Response({'exists': True}, status=status.HTTP_200_OK)
        else:
            return Response({'exists': False}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'exists': False}, status=status.HTTP_404_NOT_FOUND)



