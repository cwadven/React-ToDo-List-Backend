from django.conf import settings
from django.db import models


# To_Do
class ToDo(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    startDate = models.DateTimeField(null=True, blank=True)
    completedDate = models.DateTimeField(null=True, blank=True)
    deadLine = models.DateTimeField(null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text}'
