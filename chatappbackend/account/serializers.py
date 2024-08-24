from rest_framework import serializers
from .models import UserAccount

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = ['username','name', 'email', 'mobilenumber', 'password']

    def create(self, validated_data):
        user = UserAccount.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            username=validated_data['username'],
            mobilenumber=validated_data['mobilenumber']
        )
        return user