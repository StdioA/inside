from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField("Date Published")
    exist = models.BooleanField(default=True)

    def __str__(self):
        return self.content.encode("utf-8")

    def getObj(self):
        return {
            "content": self.content.encode("utf-8"),
            "pub_date": self.pub_date.strftime("%Y-%m-%d %H:%M:%S")
        }

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    author = models.CharField(max_length=32)

    def __str__(self):
        return self.content.encode("utf-8")

    def getObj(self):
        return {
            "content": self.content.encode("utf-8"),
            "author": self.author.encode("utf-8"),
        }
