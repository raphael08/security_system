from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import FileExtensionValidator
# from django.utils.translation import gettext as _
from django.conf import settings
from django.core.validators import RegexValidator
import uuid


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique = True)
    profileImage = models.FileField(upload_to='profileImages/', 
                                    validators=[FileExtensionValidator(
                                        allowed_extensions=['png','jpg','jpeg'])], 
                                    default='profileImages/profile_default.png',null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return "{}".format(self.email)




class Profile(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    user = models.OneToOneField(User, related_name='profil',on_delete=models.CASCADE)

    
    auth_token = models.CharField(max_length=100,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
   
    phone_number = models.CharField(max_length=15, blank=True,null=True)
    dob = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=50,null=True,blank=True)
    gender = models.CharField(max_length=6,blank=True,null=True)
    
    createdBy = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_profile",blank=True,null=True)
    updatedBy = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_profil",blank=True,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    status= models.BooleanField(default=True)
    
    class Meta:
        ordering =['-createdAt','-updatedAt']
    
    def __str__(self):
        return self.user.email
    