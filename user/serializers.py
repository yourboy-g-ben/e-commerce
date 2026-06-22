from rest_framework import serializers
from authenticate.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname', 'phone', 'gender', 'created_at']