from rest_framework import serializers
from blog.models import CommentLike, PostLike

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'