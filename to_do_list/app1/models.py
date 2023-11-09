from django.db import models
from django.utils import timezone

# Create your models here.
class Members (models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,default='',unique=True)
    password=models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
class Task(models.Model):
    user=models.ForeignKey(Members,on_delete=models.CASCADE,to_field='email')
    title=models.CharField(max_length=100)
    completed_status=models.BooleanField(default=False)
    created_on=models.DateTimeField(default=timezone.now)
