from django.db import models

import uuid   
class Device(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    deviceId = models.CharField(max_length=25,blank=True,null=True)
    lat = models.CharField(max_length=25,blank=True,null=True)
    long = models.CharField(max_length=25,blank=True,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    status= models.BooleanField(default=True)
    
    class Meta:
        ordering =['-createdAt','-updatedAt']
    
    def __str__(self):
        return str(self.id)
    
