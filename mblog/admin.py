from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("get_content", "exist", "pub_date")
    fields = ["content", "exist", "pub_date"]

    def get_content(self, obj):
        return obj.abstract

    get_content.short_description = "Content"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "author", "get_post_content")

    def get_post_content(self, obj):
        return obj.abstract

    get_post_content.short_description = "Content"


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
