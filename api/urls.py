from django.urls import path, include  # For defining URL patterns
from rest_framework import routers  # To create a router for ViewSets
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # For JWT authentication

# Import ViewSets
from api.views import UserViewSet, PostViewSet, FollowerViewSet, FeedViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'followers', FollowerViewSet, basename='follower')
router.register(r'feed', FeedViewSet, basename='feed')

# URL Configuration
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
