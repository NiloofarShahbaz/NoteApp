from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteRetrieveUpdateView.as_view(), name='note-retrieve-update'),

    path('notes/<int:pk>/contents/', ContentCreateView.as_view(), name="content-create"),
    path('notes/<int:pk>/contents/<int:content_pk>/', ContentUpdateView.as_view(), name="content-update"),

    path('notes/<int:pk>/setting/', SettingUpdateView.as_view(), name='setting-update'),

    path('labels/', LabelListView.as_view(), name='label-list'),
    path('notes/<int:pk>/label/', LabelCreateView.as_view(), name='label-create'),
    path('notes/<int:pk>/label/<int:label_pk>/', LabelUpdateView.as_view(), name='label-update'),

    path('notes/<int:pk>/label/add/<int:label_pk>/', SettingLabelCreate.as_view(), name='setting-add-label'),

]
