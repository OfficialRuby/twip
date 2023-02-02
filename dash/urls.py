from django.urls import path
from dash.views import IndexView

app_name = 'dash'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),

]
