import shutil
import tempfile

from django.test import override_settings
from rest_framework.test import APITestCase, APIClient
from ..models import User, Post

MEDIA_ROOT = tempfile.mkdtemp()  # use temporary MEDIA_ROOT to avoid creating test files in MEDIA ROOT


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestSetup(APITestCase):
    """
    Base setup for all the API testcases.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user_1_email = 'user1@gmail.com'
        cls.user_2_email = 'user2@gmail.com'
        cls.password = 'password123'
        cls.client_user_1 = User.objects.create(email=cls.user_1_email,
                                                is_active=True, full_name="Leo")
        cls.client_user_1.set_password(cls.password)
        cls.client_user_1.save()

        cls.client_user_2 = User.objects.create(email=cls.user_2_email,
                                                is_active=True, full_name="John")
        cls.client_user_2.set_password(cls.password)
        cls.client_user_2.save()
        cls.post = Post.objects.create(
            title="Post",
            description="This is post", created_by=cls.client_user_1)

        cls.client = APIClient()
        return

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)  # clear the temporary directory
        super().tearDownClass()
