from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('notes/', NoteListCreateView.as_view(), name='notes-list-create'),
    path('notes/<int:pk>/', NoteRetrieveUpdateView.as_view(), name='notes-retrieve-update'),

]
