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

    def update(self, instance, validated_data):
        instance.like = validated_data.get('like', instance.like)
        return instance

    def create(self, validated_data):
        try:
            PostLike.objects.get(post=validated_data['post'], user=validated_data['user'])

        except PostLike.DoesNotExist:
            PostLike.objects.create(post=validated_data['post'], user=validated_data['user'], like=validated_data['like'])

        return validated_data