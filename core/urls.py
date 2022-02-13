
from django.urls import path
from . import views

urlpatterns = [
    path('tracker', views.track_visitor, name='track')
]
