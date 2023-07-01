from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        validated_data['title'] = self.context['request'].data.get('title')
        validated_data['description'] = self.context['request'].data.get('description')
        validated_data['status'] = self.context['request'].data.get('status')
        return super().create(validated_data)

    def validate(self, data):
        user = self.context['request'].user

        open_advertisements_count = Advertisement.objects.filter(creator=user, status='open').count()
        if open_advertisements_count >= 10 and data.get('status') != 'CLOSED':
            raise serializers.ValidationError('У пользователя не может быть больше 10 действующих объявлений')

        return data
