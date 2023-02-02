from django.db import models
from tweet.helper_class import TwitterAPI


class AuthToken(models.Model):
    auth_token = models.CharField(max_length=100)
    auth_token_secret = models.CharField(max_length=100)

    def __str__(self):
        return self.auth_token


class UserToken(models.Model):
    STATUS_CHOICES = (
        ('success', 'Active'),
        ('danger', 'Inactive'),
    )
    access_token = models.CharField(max_length=100)
    access_token_secret = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='success')

    def save(self, *args, **kwargs):
        tweep = TwitterAPI()
        user = tweep.get_me(self.access_token, self.access_token_secret)
        self.screen_name = user.get('name')
        self.user_id = user.get('id')
        self.username = user.get('username')
        super(UserToken, self).save(*args, **kwargs)

    def __str__(self):
        return self.access_token
