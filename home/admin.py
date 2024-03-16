from django.contrib import admin
from . import models
# Register your models here.

class AdminStudent(admin.ModelAdmin):
  list_display = ('name','age','father_name',)
admin.site.register(models.Student,AdminStudent)