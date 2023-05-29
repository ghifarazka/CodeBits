from django.contrib import admin
from .models import Code, Folder, Comment, Reply

admin.site.register(Code)
admin.site.register(Folder)
admin.site.register(Comment)
admin.site.register(Reply)