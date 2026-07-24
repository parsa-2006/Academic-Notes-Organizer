from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list_view, name='course_list'),
    path('create/', views.course_create_view, name='course_create'),
    path('<int:pk>/', views.course_detail_view, name='course_detail'),
    path('<int:pk>/edit/', views.course_edit_view, name='course_edit'),
    path('<int:pk>/delete/', views.course_delete_view, name='course_delete'),

    path('<int:course_pk>/note/create/', views.note_create_view, name='note_create'),
    path('note/<int:pk>/edit/', views.note_edit_view, name='note_edit'),
    path('note/<int:pk>/delete/', views.note_delete_view, name='note_delete'),
    path('search/', views.search_view, name='search'),
]


