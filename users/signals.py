from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from .models import Profile

def createProfile(sender,instance,created,**kwargs):
    if created:
        user=instance
        profile=Profile.objects.create(user=user,user_name=user.username,email=user.email,name=user.first_name)

def profileDeleted(sender,instance,**kwargs):
    user=instance.user
    user.delete()

def profileUpdated(sender,instance,created,**kwargs):
    user=instance.user
    if created==False:
        user.first_name=instance.name
        user.username=instance.user_name
        user.email=instance.email
        user.save()

post_save.connect(createProfile,sender=User)
post_save.connect(profileUpdated,sender=Profile)
post_delete.connect(profileDeleted,sender=Profile)