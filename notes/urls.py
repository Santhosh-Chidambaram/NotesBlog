from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
        path('',homeView,name='home'),
        path('about',about,name='about'),
        path('user_login',LoginView.as_view(),name='user_login'),
        path('user_logout',user_logout,name='user_logout'),
        path('user_register',RegisterView.as_view(),name='user_register'),
        path('add_notes',NotesAddView.as_view(),name='add_notes'),
        path('notes',notes,name="notes"),
        path('myposts',myposts,name='myposts'),
        path('editnotes/<int:pk>',NotesUpdateView.as_view(),name='edit_notes'),
        path('delete/<int:pk>',NotesDeleteView,name='delete-notes')
]

if settings.DEBUG == True:
        urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)