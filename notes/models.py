from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    context = models.CharField(max_length=50)
    pub_date = models.DateTimeField(auto_now=True)
    notes_files = models.FileField(upload_to='uploads/',blank=True,null=True)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class Notification(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user_set',null=True)
    notes = models.ForeignKey(Notes,on_delete=models.CASCADE,null=True)
    followed = models.BooleanField(default=False)
    unfollowed = models.BooleanField(default=False)
    liked = models.BooleanField(default=False)
    unliked = models.BooleanField(default=False)
    new_notes = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


@receiver(post_save,sender=User)
def create_or_get_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()