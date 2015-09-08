from django.db import models
from django.contrib.auth.models import User


MESSAGE_TYPE = (
    ('success', 'Success'),
    ('info', 'Info'),
    ('warning', 'Warning'),
    ('danger', 'Danger'),
)


# Create your models here.
class Message(models.Model):
    publish_date = models.DateTimeField(auto_now_add=True)
    display_date = models.DateTimeField()
    expiration_date = models.DateTimeField()
    author = models.ForeignKey(User)
    title = models.CharField(max_length=150)
    text = models.TextField()


class InformationMessage(Message):
    active = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=MESSAGE_TYPE, default='info')
    display_once = models.BooleanField(default=True)

    def is_active(self):
        return self.active
    is_active.boolean = True