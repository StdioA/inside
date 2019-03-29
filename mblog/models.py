# coding: utf-8
from django.db import models


class Post(models.Model):
    content = models.TextField("Content")
    pub_date = models.DateTimeField("Date Published", auto_now_add=True)
    exist = models.BooleanField(default=True)

    @property
    def abstract(self):
        content = self.content
        if len(content) > 15:
            return content[:15]+"..."
        else:
            return content

    def __str__(self):
        return self.abstract

    def get_obj(self):
        return {
            "content": self.content,
            "pub_date": self.pub_date.strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_time(self):
        return self.pub_date.strftime("%Y-%m-%d %H:%M:%S")

    def serialize(self):
        result = {
            "id": self.id,
            "content": self.content,
            "pub_date": self.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
            "comments": []
        }
        for comment in self.comment_set.all():
            result["comments"].append(comment.serialize())

        return result


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    author = models.CharField(max_length=32)

    @property
    def abstract(self):
        content = self.content
        if len(content) > 15:
            return content[:15] + "..."
        else:
            return content

    def __str__(self):
        return self.abstract

    def serialize(self):
        return {
            "content": self.content,
            "author": self.author,
        }
