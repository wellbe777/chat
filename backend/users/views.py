from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
from datetime import datetime, timezone, timedelta
from django.utils.http import urlsafe_base64_encode
import jwt

def remove_cookies(response):
    response.delete_cookie('jwt')
    response.delete_cookie('signature')

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'success'})

class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        payload = {
            'id': user.id,
            #'username': user.username,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=60)
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=False,
            samesite='None',
            secure=True, path = "/; Partitioned", max_age=3600)
        response.set_cookie(key='signature', value=urlsafe_base64_encode(user.username.encode("ascii")), httponly=False,
            samesite='None',
            secure=True, path = "/; Partitioned", max_age=3600)

        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.DecodeError:
            raise AuthenticationFailed('Unauthenticated!')
        response = Response()
        # if is_token_expired(token):
        #     remove_cookies(response)
        #     return response

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        response.data = serializer.data
        return response
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        remove_cookies(response)
        response.data = {
            'message': 'success'
        }
        return response