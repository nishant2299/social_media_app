from django.contrib.auth.models import User
from .models import Post, FavoritePost
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password']
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['image','title','description']


class ListPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','image','title','description','created_at','user']


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritePost
        fields = ['post']