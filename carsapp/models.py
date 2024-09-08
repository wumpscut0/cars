from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now


class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.SmallIntegerField(
        validators=(
            MinValueValidator(1888),
            MaxValueValidator(now().year),
        )
    )
    description = models.TextField(max_length=1023, null=True, blank=True)

    def __str__(self):
        return f"{self.make}[{self.model}]"


class Comment(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, default="Unknown", on_delete=models.SET_DEFAULT, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    content = models.TextField(max_length=255)
