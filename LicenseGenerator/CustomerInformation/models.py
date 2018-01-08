from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE,)
    updated_by = models.ForeignKey(User, null=True,related_name='+',on_delete=models.CASCADE,)
    
    def __str__(self):
        return self.name

class LicenseInformation(models.Model):
    product = models.TextField(max_length=4000)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='licenseinformations')
    license = models.TextField(max_length=4000)
    noofusers = models.IntegerField(default=1)
    noofdaystrial = models.IntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE,)
    updated_by = models.ForeignKey(User, null=True,related_name='+',on_delete=models.CASCADE,)   