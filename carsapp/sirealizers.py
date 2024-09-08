from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Car, Comment


class CarModelSerializer(ModelSerializer):
    owner = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Car
        read_only_fields = "owner", "created_at", "updated_at"
        fields = "__all__"


class CommentModelSerializer(ModelSerializer):
    car = PrimaryKeyRelatedField(read_only=True)
    author = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Comment
        read_only_fields = "car", "author"
        fields = "__all__"
