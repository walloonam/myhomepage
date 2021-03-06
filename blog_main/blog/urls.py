from django.urls import path
from . import views

urlpatterns = [
    path('update_post/<int:pk>', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('', views.PostList.as_view()),
    path('', views.postpage),
    path('<int:pk>/', views.PostDetail.as_view()),
    # path('', views.index),
    path('category/<str:slug>/', views.categories_page),
    path('tag/<str:slug>', views.show_tag_posts),
    path('<int:pk>/new_comment/', views.new_comment),
    path('todo/', views.todo),
    path('todo/update/<str:pk>/', views.updatTask),
    path('todo/delete/<str:pk>/', views.deleteTask)
]