from __future__ import unicode_literals

from django.db import models

# Create your models here.
import re
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def registerVal(self, postData):
        results={'status':True, 'errors':[]}
        if not postData['name'] or len(postData['name'])<3:
            results['status']=False
            results['errors'].append("Name must be at least 3 characters.")
        if not postData['email'] or not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", postData['email']) or len(postData['email'])<3:
            results['status']=False
            results['errors'].append("Email address is not valid.")
        if not postData['password'] or len(postData['password'])<8 or postData['password'] != postData['confirmpw']:
            results['status']=False
            results['errors'].append("Password must be at least 8 characters, and both password fields must match.")
        if results['status']==True:
            user = User.objects.filter(email=postData['email'])
            if len(user) != 0:
                results['status']=False
                results['errors'].append("Registration failed. Please use a different email address.")
                return results
            else:
                password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
                User.objects.create(name=postData['name'], email=postData['email'].lower(), password=password)
                results['errors'].append("Registration successful, please log in.")
                return results
        return results

    def loginVal(self, postData):
        results = {'status':True, 'loginMsg':[], 'user':{}}
        if not postData['email'] or not postData['password']:
            results['status']=False
            results['loginMsg'].append("Login failed, please try again.")
            return results
        user = User.objects.filter(email=postData['email'].lower())
        if len(user)==0:
            results['status']=False
            results['loginMsg'].append("Login failed, please try again.")
            return results
        postData['password'].encode()
        if bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) == user[0].password:
            results['user']=user
            return results
        else:
            results['status']=False
            results['loginMsg'].append("Login failed, please try again.")
            return results

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

