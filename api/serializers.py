from rest_framework import serializers
from rest_framework.response import Response
from blog.models import CommentLike, PostLike, Post
from django.contrib.postgres.search import SearchQuery

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.like = validated_data.get('like', instance.like)
        return instance

    def create(self, validated_data):
        try:
            PostLike.objects.get(post=validated_data['post'], user=validated_data['user'])

        except PostLike.DoesNotExist:
            PostLike.objects.create(post=validated_data['post'], user=validated_data['user'], like=validated_data['like'])

        return validated_data

class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    headline = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ['text', 'img', 'headline', 'create_date', 'url']

class SearchSerializer(serializers.Serializer):
    s = serializers.CharField()