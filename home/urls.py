from django.urls import path
from .views import *

urlpatterns = [
    path('student/', StudentAPI.as_view()),
    path('pdf/', generatepdf.as_view()),
    path('generic-view/' , Studentgeneric.as_view()),
    path('generic-view/<id>' , StudentgenericUD.as_view()),
    path('register/', UserRegistration.as_view())
# path('', home, name='home'),
# path('student/',post_req, name='post_request'),
# path('update-student/<id>/',update_student, name='update_request'),
# path('pupdate-student/<id>/',pupdate_student, name='pupdate_request'),
# path('delete-student/<id>/',delete_student, name='delete_request')

]



