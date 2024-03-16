from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import uuid
from django.conf import settings
# Create your models here.

class CustomUser(AbstractUser):
    username  = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    is_email_verified = models.BooleanField(default=True)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length = 6, null = True, blank = True)
    email_verification_token = models.CharField(max_length =200, null = True, blank =True)
    forgot_password_token = models.CharField(max_length =200, null = True, blank =True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name
    
    def __str__(self):
        return self.email
    
    
#here i am sending the mail to verify the email id
@receiver(post_save, sender = CustomUser)
def send_email_token(sender, instance, created, **kwargs):
    if created:
        try:
            subject = "Your email need to be verified"
            message = f'Hi, click here to verify your email id http://127.0.1:8000/{uuid.uuid4()}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [instance.email]
            send_mail(subject, message, email_from, recipient_list)
            
        except Exception as e:
            print(e)    