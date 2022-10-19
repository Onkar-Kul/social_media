from django.urls import resolve
from rest_framework.reverse import reverse
from rest_framework.test import APISimpleTestCase

from ..views import PostCreateAPIView, CommentCreateAPIView


class TestUrls(APISimpleTestCase):
    def setUp(self):
        self.base_url = '/api/'
        self.app_name = 'social'
        return

    def test_create_post_url(self):
        url = reverse(f'{self.app_name}:posts')
        resolved = resolve(url)
        self.assertEqual(resolved.func.__name__, PostCreateAPIView.as_view().__name__)
        self.assertEqual(resolved.namespace, self.app_name)
        self.assertEqual(url, f'{self.base_url}posts/')

    def test_create_comment_url(self):
        pk = 1
        url = reverse(f'{self.app_name}:comment', kwargs={'pk': pk})
        resolved = resolve(url)
        self.assertEqual(resolved.func.__name__, CommentCreateAPIView.as_view().__name__)
        self.assertEqual(resolved.namespace, self.app_name)
        self.assertEqual(url, f'{self.base_url}comment/{pk}/')
