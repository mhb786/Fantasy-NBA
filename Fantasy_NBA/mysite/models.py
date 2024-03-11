from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class NBAPlayer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50) 
    team = models.CharField(max_length=50, default='Unknown')

    PPG = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    APG = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    RPG = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    SPG = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    BPG = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    FG_PCT = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    FG3_PCT = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    FT_PCT = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    MIN = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    TOV = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Team(models.Model):
    team_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    logo = models.URLField()
    all_star = models.BooleanField(default=False)
    nba_franchise = models.BooleanField(default=True)
    conference = models.CharField(max_length=50, default='')
    division = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Thread(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self): 
        return reverse('thread_detail', kwargs={'pk': self.pk})

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def default_profile_picture():
    return "default_profile.jpg"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    favorite_team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', default=default_profile_picture)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()