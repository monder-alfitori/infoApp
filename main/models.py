from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Headline(models.Model):
    title = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Tag(models.Model):
    title = models.CharField(max_length=500, null=True)
    creator = models.ForeignKey(User, related_name='Tcreator', null=True, on_delete=models.SET_NULL)    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Party(models.Model):
    title = models.CharField(max_length=2000)
    text = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, related_name='Pcreator', null=True, on_delete=models.SET_NULL)    
   #parent = models.ManyToManyField('self', symmetrical=False, related_name='Pparent', blank=True)
    headline = models.ManyToManyField(Headline, blank=True, related_name="Pheadline")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    

    class Meta:
        ordering = ['-created_at']

class Info(models.Model):
    title = models.CharField(max_length=10000, null=True)
    text = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=1000, null=True, blank=True)
    party = models.ManyToManyField(Party, blank=True, related_name="infoParty")
    tags = models.ManyToManyField(Tag, blank=True, related_name="infotags")
    creator = models.ForeignKey(User, related_name='Icreator', null=True, on_delete=models.SET_NULL)    
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(upload_to='files/%y/%m/%d', null=True, blank=True)
    #video = models.FileField(upload_to='videos/%y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']