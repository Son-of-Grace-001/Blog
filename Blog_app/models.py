from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Blogs/", default="default.jpg")

    def __str__(self):
        return f"{self.title} by {self.author.username}"

class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.username} commented on {self.blog.title}"