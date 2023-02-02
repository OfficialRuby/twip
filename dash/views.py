from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views.generic import (View, ListView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin

from tweet.models import UserToken


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = UserToken.objects.all().order_by('-timestamp')
        context = {
            'users': user,

        }

        return render(request, 'dash/index.html', context)
