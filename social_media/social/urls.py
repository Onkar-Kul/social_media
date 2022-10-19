from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginUserView, PostCreateAPIView, PostDetailAPIView, CommentCreateAPIView, \
    LikeAPIView, UnlikeAPIView, FollowView, UserProfileAPIView, BlackListTokenView

app_name = 'social'
urlpatterns = [

    path('login/', LoginUserView.as_view(), name='token_obtain_pair'),
    path('posts/', PostCreateAPIView.as_view(), name='posts'),
    path('all_posts/', PostCreateAPIView.as_view(), name='all_posts'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('comment/<int:pk>/', CommentCreateAPIView.as_view(), name='comment'),
    path('like/<int:pk>/', LikeAPIView.as_view(), name='like'),
    path('unlike/<int:pk>/', UnlikeAPIView.as_view(), name='unlike'),
    path('follow/<int:pk>/', FollowView.as_view({'post': 'follow'}), name='follow'),
    path('unfollow/<int:pk>/', FollowView.as_view({'post': 'unfollow'}), name='unfollow'),
    path('user/<int:pk>/', UserProfileAPIView.as_view(), name='user'),
    path('logout/', BlackListTokenView.as_view(), name='token_blacklist'),

]
