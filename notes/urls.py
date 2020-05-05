from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
        path('',homeView,name='home'),
        path('about',about,name='about'),
        path('add_notes',NotesAddView.as_view(),name='add_notes'),
        path('myposts',myposts,name='myposts'),
        path('notes/<int:pk>/edit',NotesUpdateView.as_view(),name='edit_notes'),
        path('notes/<int:pk>/delete',NotesDeleteView,name='delete-notes'),
        path('notes/<int:pk>/detail',NotesDetailView,name='notes-detail'),
        path('notfiy/',NotificationsView.as_view(),name='notification'),
        path('notfiy/remove/<int:pk>',NotifyRemove,name='notify-remove'),
        path('notfiy/remove/all',NotifyRemoveAll,name='notify-removeall'),
        path('user/<int:pk>/follow',Follow,name='follow'),
        path('searchquery/',SearchView,name='user-search')
        
]

if settings.DEBUG == True:
        urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)