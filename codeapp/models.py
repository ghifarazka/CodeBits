from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Code(models.Model):
    title = models.CharField(max_length=256)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    snippet = models.TextField(default=None, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('codeapp-code-detail', kwargs={'pk': self.pk})

class Folder(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('codeapp-code-detail', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    code_origin = models.ForeignKey(Code, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    # def get_absolute_url(self):
    #     return reverse('code-detail', kwargs={'pk': self.pk})

class Reply(models.Model):
    content = models.TextField()
    comment_origin = models.ForeignKey(Comment, on_delete=models.CASCADE)