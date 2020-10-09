from rest_framework import serializers

from .models import User


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class TokenGainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=100)


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "bio", "email", "role"]
