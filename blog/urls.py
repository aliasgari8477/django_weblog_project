
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.PostListView.as_view(), name='home'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('add/', views.PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),


]