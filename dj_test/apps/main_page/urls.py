from django.urls import path
from . import views


app_name = 'main_page'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('<int:article_id>/leave_comment/', views.leave_comment, name='leave_comment'),
    path('home', views.home, name='home'),
    path('create_article/', views.create_article, name='create_article'),

]
