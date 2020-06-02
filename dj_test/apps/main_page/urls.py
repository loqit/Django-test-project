from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'main_page'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('<int:article_id>/leave_comment/', views.leave_comment, name='leave_comment'),
    path('home/', views.home, name='home'),
    path('create_article/', views.create_article, name='create_article'),
    path('<int:article_id>/delete_article/', views.delete_article, name='delete_article'),
    path('<int:comment_id>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('login', views.UserLoginView.as_view(), name='login_page'),
    path('logout', views.UserLogoutView.as_view(), name='logout_page'),
    path('register', views.usersignup, name='register_page'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate_account, name='activate'),
]