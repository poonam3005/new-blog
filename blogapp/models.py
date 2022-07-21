from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField
from tinymce.models import HTMLField
# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) :
        return str(self.category)

class Title(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) :
        return str(self.title)

class Blog(models.Model):
    author = models.ForeignKey(User,  on_delete=models.CASCADE)
    title = models.ForeignKey(Title,  on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE, blank=True, null=True)
    entryTxt = models.CharField(max_length=300,blank=True,null=True)
    Desc =  HTMLField(blank=True, null=True)
    keyword = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='static', null=True,blank=True)
    date = models.DateField( auto_now=True)
    likes = models.ManyToManyField(User, related_name='blog_post')

    def total_likes(self):
        return self.likes.count()

    def __str__(self) :
        return str(self.id)

class Comment(models.Model):
    post = models.ForeignKey(Blog,related_name='comments',on_delete=models.CASCADE)
    name = models.ForeignKey(User,  on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return '%s-%s-%s' % (self.id,self.post.title,self.name)