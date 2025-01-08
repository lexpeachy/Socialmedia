from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User, Post, Follower
from .serializers import UserSerializer, PostSerializer, FollowerSerializer


# Custom permission class to ensure only the owner can modify the object
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.user == request.user


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


# Post ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        # Automatically set the user to the currently authenticated user
        serializer.save(user=self.request.user)


# Follower ViewSet
class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        user = request.user
        target_user_id = request.data.get('user')

        # Prevent users from following themselves
        if str(user.id) == target_user_id:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the follow relationship
        serializer = self.get_serializer(data={"user": target_user_id, "follower": user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='unfollow/(?P<user_id>[^/.]+)')
    def unfollow(self, request, user_id):
        user = request.user
        try:
            # Find and delete the follow relationship
            follow_relationship = Follower.objects.get(user_id=user_id, follower=user)
            follow_relationship.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follower.DoesNotExist:
            return Response({"detail": "Follow relationship does not exist."}, status=status.HTTP_404_NOT_FOUND)


# Feed ViewSet
class FeedViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        user = request.user
        # Get the list of users the current user is following
        followed_users = user.following.values_list('user_id', flat=True)
        # Retrieve posts from followed users, ordered by timestamp
        posts = Post.objects.filter(user_id__in=followed_users).order_by('-timestamp')
        # Paginate the results
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)