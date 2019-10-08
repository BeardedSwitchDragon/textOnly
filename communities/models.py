from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import misaka

User = get_user_model()

from django import template
register = template.Library()

class Community(models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True,default="A Text Only community.")
    description_html = models.TextField(editable=False,default="A Text Only community.",blank=True)
    members = models.ManyToManyField(User, through="CommunityMember")

    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        #turning into name that doesn't interfere with website directories
        self.description = misaka.html(self.description)
        super().save(*args,**kwargs)
    def get_absolute_url(self):
        return reverse("communitys:single",kwargs={"slug":self.slug})
    class Meta:
        ordering = ["name"]

class CommunityMember(models.Model):
    community = models.ForeignKey(Community,related_name="memberships",on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_communities",on_delete=models.CASCADE)

    def __str__(self):
        self.user.username
    class Meta:
        unique_together = ("community", "user")
    pass
