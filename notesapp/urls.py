
from django.contrib import admin
from django.urls import path,include
from notes.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('',include('notes.urls')),
]
