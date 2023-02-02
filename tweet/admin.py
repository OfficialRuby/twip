from django.contrib import admin
from tweet.models import UserToken, AuthToken


admin.site.register(AuthToken)
admin.site.register(UserToken)
