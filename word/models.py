from django.db import models
from django_quill.fields import QuillField

class Document(models.Model):
    title = models.CharField(max_length=1000, null=True)
    content = QuillField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
