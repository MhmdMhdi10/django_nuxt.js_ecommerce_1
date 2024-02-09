from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    rating = serializers.IntegerField(min_value=1, max_value=5, error_messages={
        'invalid': _('Rating should be an integer between 1 and 5.')
    })

    class Meta:
        model = Review
        fields = ('id', 'user', 'rating', 'comment', 'product')
