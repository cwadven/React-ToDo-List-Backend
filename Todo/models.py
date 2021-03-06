from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orderNumber = models.PositiveIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "author")

    def __str__(self):
        return f'{self.name}'


# To_Do
class ToDo(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    startDate = models.DateTimeField(null=True, blank=True, db_index=True)
    completedDate = models.DateTimeField(null=True, blank=True, db_index=True)
    deadLine = models.DateTimeField(null=True, blank=True, db_index=True)
    orderNumber = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text}'
