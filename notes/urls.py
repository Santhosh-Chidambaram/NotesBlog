from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
        path('',homeView,name='home'),
        path('about',about,name='about'),
        path('user_login',user_login,name='user_login'),
        path('user_logout',user_logout,name='user_logout'),
        path('user_register',user_register,name='user_register'),
        path('add_notes',add_notes,name='add_notes'),
        path('notes',notes,name="notes"),
        path('myposts',myposts,name='myposts'),
        path('profile',profile,name='profile'),
        path('editnotes/<int:id>',edit_notes,name='edit_notes'),
        path('deletenotes/<int:id>',delete_notes,name='delete_notes')
]

if settings.DEBUG == True:
        urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)