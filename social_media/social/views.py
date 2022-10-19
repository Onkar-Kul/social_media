from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from .models import Post, Comment, Follow, User
from .serializers import LoginUserSerializer, AllPostSerializer, CommentSerializer, ProfileSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, CreateAPIView, UpdateAPIView, \
    get_object_or_404, RetrieveAPIView


# Create your views here.

class LoginUserView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.

    """
    serializer_class = LoginUserSerializer


class BlackListTokenView(APIView):
    """
    This view is same as a logout's view functionality.

    send a POST request with only the refresh_token object.

    {
        refresh_token: <user_refresh_token>
    }
    """

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(data={'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PostCreateAPIView(ListCreateAPIView):
    """
    This view is to create Posts by authenticated users and display all posts to them
    """
    serializer_class = AllPostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PostDetailAPIView(RetrieveDestroyAPIView):
    """
    This view is used to get all the details of the posts and 
    delete the particular post by authenticated users

    param: pk: Pk should be the post id
    """
    serializer_class = AllPostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]


class CommentCreateAPIView(CreateAPIView):
    """
    This view used to create Comments on particular post by authenticated user
    param: pk: pk should be the post id
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['pk'])
        serializer.save(commented_by=self.request.user, post=post)


class LikeAPIView(UpdateAPIView):
    """
    This view is used to generate likes on the particular posts by authenticated user
    param: pk: pk should be the post id
    """
    serializer_class = AllPostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        post.likes.add(self.request.user)

        serializer = self.get_serializer(post)
        return Response(serializer.data)


class UnlikeAPIView(UpdateAPIView):
    """
    This view is used to unlike the particular posts by authenticated user
    param: pk: pk should be the post id
    """
    serializer_class = AllPostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])

        if post.likes.filter(id=self.request.user.id).exists():
            post.likes.remove(self.request.user)

        serializer = self.get_serializer(post)
        return Response(serializer.data)


class FollowView(viewsets.ViewSet):
    """
    This view is used to follow and unfollow the user
    param: pk: pk should be the other user id (not current logged in user id)
    """
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated]

    def follow(self, request, pk):
        user = get_object_or_404(User, id=self.kwargs['pk'])

        try:
            instance = Follow.objects.get(user=self.request.user)
            instance.follow.add(user)

        except Follow.DoesNotExist:
            follow = Follow.objects.create(user=self.request.user)
            follow.save()
            instance = get_object_or_404(Follow, id=follow.id)
            instance.follow.add(user)
        return Response({'message': 'now you are following'}, status=status.HTTP_200_OK)

    def unfollow(self, request, pk):
        user = get_object_or_404(User, id=self.kwargs['pk'])
        instance = get_object_or_404(Follow, user=self.request.user)
        instance.follow.remove(user)
        return Response({'message': 'you are no longer following'}, status=status.HTTP_200_OK)


class UserProfileAPIView(RetrieveAPIView):
    """
    This view is used to show profile details of the current user
    """
    serializer_class = ProfileSerializer
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Follow.objects.get(user=self.request.user)
