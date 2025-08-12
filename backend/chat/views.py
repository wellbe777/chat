from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework.views import APIView
from users.models import User
from users.serializers import UserSerializer
from .serializers import ChannelSerializer, MessageSerializer
from .models import Channel, Message
import jwt

def check_auth(func):
    def wrapper(*args):
        request = args[1]
        if not args[1]:
            raise ParseError('Something went wrong!') 
        token = request.COOKIES.get('jwt')
            
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.DecodeError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            raise AuthenticationFailed('Unauthenticated!')
        return func(*args, user)
    return wrapper
    
class ChannelView(APIView):
    @check_auth
    def get(self, request, user):
        request_type = int(request.query_params.get('request_type'))
        response = Response()
        if request_type == 1:
            channels = Channel.objects.all()
            response.data = ChannelSerializer(channels, many=True).data
        elif request_type == 2:
            chat_name = request.query_params.get('channel_name')
            messages = Message.objects.filter(chat_name=chat_name)
            response.data = MessageSerializer(messages, many=True).data
        return response
 
