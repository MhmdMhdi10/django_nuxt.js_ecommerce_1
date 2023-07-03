from rest_framework import serializers
from apps.category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'parent', 'name', 'children']
