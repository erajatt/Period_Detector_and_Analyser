from rest_framework import serializers
from .models import User, PeriodDetail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class PeriodDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PeriodDetail
        fields = ['id', 'user', 'start_date', 'end_date', 'symptoms']
