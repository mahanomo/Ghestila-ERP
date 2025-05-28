from django.db import models
from .users import User
from .departments import Department
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def valid_order(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)