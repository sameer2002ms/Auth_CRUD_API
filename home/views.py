import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializer import *
from home.helper import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
 
# @api_view(['GET', 'POST', 'PATCH'])
# def home(request):
#     if request.method == 'GET':
#       snippets = Student.objects.all()
#       serializer = StudentSerializer(snippets, many=True)
#       return Response({
#        'status' : 300,
#        'data' : serializer.data,
#        'message' : 'you called the GET method'
#     })

class UserRegistration(APIView):
  def UserRegister(self, request):
     serializers = UserSerialiser(data = request.data)

     if not serializers.is_valid():
        return Response({ 
      'status' : 404,
      'errors' : serializers.errors,
      'message' : 'Something went wrong'
    })
     serializers.save()  

     user = User.objects.get(username = serializers.data['username'])
     token_obj , _ = Token.objects.get_or_create(user=user)
     print(serializers.data)
     return Response({
      'status' : 300,
      'data' : serializers.data,
      'token' : str(token_obj),
      'message' : 'you called the PUT method'
    }) 



class StudentAPI(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self,request):
      snippets = Student.objects.all()
      serializer = StudentSerializer(snippets, many=True)
      print(request.user)
      return Response({
       'status' : 300,
       'data' : serializer.data,
       'message' : 'you called the GET method'
    }) 
  
  def post(self,request):
    data = request.data
    serializers = StudentSerializer(data)

    if not serializers.is_valid():
        print(serializers.errors)
        return Response({ 
      'status' : 404,
      'errors' : serializers.errors,
      'message' : 'Something went wrong'
    })
    serializers.save()  

    return Response({
      'status' : 300,
      'data' : serializers.data,
      'message' : 'you called the PUT method'
    }) 
  
  def put(self,request):
    try:
       student_obj = Student.objects.get(id=request.data['id'])
       serializers = StudentSerializer(student_obj, data=request.data)

       if not serializers.is_valid():
        print(serializers.errors)
        return Response({ 
      'status' : 404,
      'errors' : serializers.errors,
      'message' : 'Something went wrong'
    })
       serializers.save()  

       return Response({
      'status' : 300,
      'data' : serializers.data,
      'message' : 'you called the PUT method'
    })
    except Exception as e:
        return Response({'status' :404, 'message': 'you have invalid id'})
        
 
  
  def patch(self,request):
    try:
       student_obj = Student.objects.get(id=request.data['id'])
       serializers = StudentSerializer(student_obj, data=request.data, partial =True)

       if not serializers.is_valid():
        print(serializers.errors)
        return Response({ 
      'status' : 404,
      'errors' : serializers.errors,
      'message' : 'Something went wrong'
    })
       serializers.save()  

       return Response({
      'status' : 300,
      'data' : serializers.data,
      'message' : 'you called the PATCH method'
    })
    except Exception as e:
        return Response({'status' :404, 'message': 'you have invalid id'})
         
  
  def delete(self,request):
    try:
       student_obj = Student.objects.get(id=request.data['id'])
       student_obj.delete()
       return Response({'status' : 300, 'message' : 'deleted'})
    except Exception as e:
        return Response({'status' :404, 'message': 'invalid id'})
      



# @api_view(['POST'])
# def post_req(request):
#       data = request.data
#       serializers = StudentSerializer(data=request.data)

#       if not serializers.is_valid():
#         print(serializers.errors)
#         return Response({ 
#       'status' : 404,
#       'errors' : serializers.errors,
#       'message' : 'Something went wrong'
#     })
#       serializers.save()  

#       return Response({
#       'status' : 300,
#       'data' : serializers.data,
#       'message' : 'you called the PUT method'
#     })

# @api_view(['PUT'])
# def update_student(request,id):
#     try:
#        student_obj = Student.objects.get(id=id)
#        serializers = StudentSerializer(student_obj, data=request.data)

#        if not serializers.is_valid():
#         print(serializers.errors)
#         return Response({ 
#       'status' : 404,
#       'errors' : serializers.errors,
#       'message' : 'Something went wrong'
#     })
#        serializers.save()  

#        return Response({
#       'status' : 300,
#       'data' : serializers.data,
#       'message' : 'you called the PUT method'
#     })
#     except Exception as e:
#         return Response({'status' :404, 'message': 'you have invalid id'})
        

# @api_view(['PATCH'])
# def pupdate_student(request,id):
#     try:
#        student_obj = Student.objects.get(id=id)
#        serializers = StudentSerializer(student_obj, data=request.data, partial =True)

#        if not serializers.is_valid():
#         print(serializers.errors)
#         return Response({ 
#       'status' : 404,
#       'errors' : serializers.errors,
#       'message' : 'Something went wrong'
#     })
#        serializers.save()  

#        return Response({
#       'status' : 300,
#       'data' : serializers.data,
#       'message' : 'you called the PATCH method'
#     })
#     except Exception as e:
#         return Response({'status' :404, 'message': 'you have invalid id'})
        

# @api_view(['DELETE'])
# def delete_student(request,id):
#     try:
#        student_obj = Student.objects.get(id=id)
#        student_obj.delete()
#        return Response({'status' : 300, 'message' : 'deleted'})
#     except Exception as e:
#         return Response({'status' :404, 'message': 'invalid id'})
     
from rest_framework import generics

  
class Studentgeneric(generics.ListAPIView, generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    
class StudentgenericUD(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'
    
class generatepdf(APIView):
  def get(self,request):
    student_objs = Student.objects.all()
    params = {
      'today' : datetime.date.today(),
      'student_objs' : student_objs
    }
    file_name, status = save_pdf(params)
    
    if not status:
      return Response({'status' : 400})
    return Response({'status':200, 'path' : f'/media/{file_name}.pdf'})    