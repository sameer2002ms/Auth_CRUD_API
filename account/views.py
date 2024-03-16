import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.helpers import send_otp_to_mobile

from .models import *
from .serializers import *
from home.helper import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterView(APIView):
    
    def post(self, request):
        try:
            serializer = UserSerialiser(data=request.data)
            if not serializer.is_valid():
              return Response({
                      'status' : 404,
                      'errors' : serializer.errors    
                      })
            serializer.save()
            return Response({'status' : 200, 'message' : 'An email OTP is sent to your Email'})
        except Exception as e:
            print(e)    
            return Response({'status' : 404, 'error' : 'Something went wrong'})
        
        
        
class VerifyOtp(APIView):
    def post(Self,request):
        try:
            data = request.data
            user_obj = CustomUser.objects.get(phone = data.get('phone'))
            otp = data.get('otp')  
            
            
            if user_obj.otp == otp:
                user_obj.is_phone_verified = True
                user_obj.save()
                
                return Response({'status' : 200, 'message' : ' Your OTP is Verified'})
                
            return Response({'status' : 403, 'error' : ' Your OTP is Wrong'})
        
        except Exception as e:
            print(e)
        
        return Response({'status' : 404, 'error' : 'Something went wrong'})

    def patch(self, request):
        try:
            data = request.data
            user_obj = CustomUser.objects.filter(phone = data.get('phone'))
            if not user_obj.exists():
               return Response({'status' : 404, 'error' : 'No User Found'})
           
            status, time= send_otp_to_mobile(data.get('phone'), user_obj[0])
            if status:
                return Response({'status' : 200, 'message' : 'new otp sent'})
            
            return Response({'status': 404, 'error' : f'Try after few second {time}'})
        
        
        except Exception as e:
            print(e)
            
        return Response({'status' : 404, 'error' : 'Something went wrong'})
    