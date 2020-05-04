
from django.contrib import admin
from django.urls import path,include
from notes.views import ProfileEditView,ProfileView,LoginView,RegisterView,user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/<int:pk>/profile/',ProfileView.as_view(),name='profile'),
    path('profile-edit/',ProfileEditView.as_view(),name='profile-edit'),
    path('user_login/',LoginView.as_view(),name='user_login'),
    path('user_logout/',user_logout,name='user_logout'),
    path('user_register/',RegisterView.as_view(),name='user_register'),
    path('',include('notes.urls')),
]
