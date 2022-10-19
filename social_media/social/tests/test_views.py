from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from .test_setup import TestSetup
from ..models import Post


class Login(TestSetup):

    def client_login(self):
        self.client.logout()
        self.user = self.client.login(email='client@gmail.com', password='password123')
        access = AccessToken.for_user(self.client_user_1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        return


class TestPosts(Login):

    def test_create_post_with_validdata(self):
        self.client_login()
        url = reverse('social:posts')
        data = {"title": "New Post", "description": "My first Post"}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_with_invalid_data(self):
        self.client_login()
        url = reverse('social:posts')
        data = {"title": "New Post"}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestComment(Login):

    def test_create_comment_with_valid_data(self):
        self.client_login()
        post = Post.objects.get(title="Post")
        url = reverse('social:comment', kwargs={'pk': post.id})
        data = {"comment": "Nice Post"}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_with_invalid_data(self):
        self.client_login()
        post = Post.objects.get(title="Post")
        url = reverse('social:comment',  kwargs={'pk': post.id})
        data = {"title": "New Post"}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
