from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from blog.models import CommentLike, PostLike
from api.serializers import CommentLikeSerializer, PostLikeSerializer
from rest_framework import mixins
from blog.models import Post, Comment
from django.contrib.auth.models import User
from rest_framework.views import APIView

class CommentLikeViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    """
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer

    # for production faze
    # renderer_classes = [JSONRenderer]

    def update(self, request, pk=None):
        comment_like = get_object_or_404(self.queryset, pk=pk)
        if comment_like.user.pk == request.data['user'] and comment_like.comment.pk == request.data['comment']:
            comment_like.like = request.data['like']
            return Response({'status': 'ok'})

        else:
            return Response({'error': 'Update not allowed'})

    def create(self, request):
        serialized = PostLikeSerializer(data=request.data)

        if serialized.is_valid():
            comment = get_object_or_404(Comment.objects.all(), pk=request.data['comment'])
            user = get_object_or_404(User.objects.all(), pk=request.data['user'])

            CommentLike.objects.create(like=request.data['like'], comment=comment, user=user)

            return Response({"status": 'ok'})

        return Response({'error': 'Operation not allowed'})

    def delete(self, request, pk):
        get_object_or_404(self.queryset, pk=pk).delete()
        return Response({"status": 'ok'})

class PostLikeViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    # for production faze
    # renderer_classes = [JSONRenderer]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class NotApprovedView(APIView):

    def get(self, request, format=None):
        return Response({'count': Post.objects.filter(approved=False).count()})