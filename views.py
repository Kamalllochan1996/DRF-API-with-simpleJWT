from json import JSONDecodeError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.models import User
# from account.renderers import UserRenderer
from account.serializers  import UserLoginSerializer, UserProfileSerializer,UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Generate Token manualy
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

# Create your views here.
class UserRegistrationView(APIView):
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Registration Success'},status=status.HTTP_201_CREATED)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      email = serializer.data.get('email')
      password = serializer.data.get('password')
      user = authenticate(email=email, password=password)
      if user is not None:
        token = get_tokens_for_user(user)
        return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  # renderer_classes = [UserRenderer]
 permission_classes = [IsAuthenticated]
 def get(self, request, format=None):
  serializer = UserProfileSerializer(request.user)
  # if serializer.is_valid():
  return Response(serializer.data,status=status.HTTP_200_OK)
  
