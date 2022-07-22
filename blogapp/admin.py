from django.contrib import admin
from .models import Blog,Category,Title, Comment, ReplyComment
# Register your models here.

admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Comment)
admin.site.register(ReplyComment)