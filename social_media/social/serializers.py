import json
from abc import ABC

from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post, Comment, Follow


class LoginUserSerializer(TokenObtainSerializer):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data


class AllPostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'like_count', 'comments']
        read_only_fields = ['id', 'created_at', 'like_count', 'comments']

    @staticmethod
    def get_like_count(obj):
        like_count = Post.objects.get(id=obj.id).total_likes()
        return like_count

    @staticmethod
    def get_comments(obj):
        comments = Comment.objects.filter(post=obj).values_list('comment', flat=True)
        return comments


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']


class ProfileSerializer(serializers.ModelSerializer):
    follower_count = serializers.IntegerField(source='get_followers_count')
    following_count = serializers.IntegerField(source='get_following_count')
    full_name = serializers.CharField(source='user.full_name')

    class Meta:
        model = Follow
        fields = ['full_name', 'follower_count', 'following_count']
        read_only_fields = ['full_name', 'follower_count', 'following_count']
