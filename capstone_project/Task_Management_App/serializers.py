from rest_framework import serializers
from .models import Task, User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
        

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'user',
            'title',
            'description',
            'due_date',
            'priority',
            'status',
            'completed_at',
        ]
        read_only_fields = ['user', 'completed_at']

    def validate_due_date(self, value):
        # ✅ Ensure due date is in the future
        if value < timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def validate(self, data):
        # ✅ Prevent editing completed tasks unless reverted
        instance = getattr(self, 'instance', None)
        if instance and instance.status == 'Completed' and data.get('status') != 'Completed':
            raise serializers.ValidationError("Cannot edit a completed task unless reverted.")
        return data

    def create(self, validated_data):
        # ✅ Assign task to the current user
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
