from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, is_active=True):
        # simplifies usage of admin & staff users creation

        if not email:
            raise ValueError("User must have an email address")
        if not password:
            pass
            # raise ValueError('User must have a password')
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    admin = models.BooleanField(default=False,
                                help_text='Has full rights to the system and can manage via admin panel')
    staff = models.BooleanField(default=False,
                                help_text='If a user has any of the admin roles, make this to True')
    is_active = models.BooleanField(default=True,
                                    help_text='Inactive users cannot login')
    full_name = models.CharField(max_length=250, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app app_label?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff


class Post(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    follow = models.ManyToManyField(User, related_name='follower')

    def get_followers_count(self):
        return Follow.objects.filter(follow=self.user).count()

    def get_following_count(self):
        return Follow.objects.filter(user=self.user).exclude(follow=self.user).count()
