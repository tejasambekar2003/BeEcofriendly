from django.conf.urls import url
from django.urls.conf import path
from . import views
from django.conf import settings


app_name = 'posts'

urlpatterns = [
    path('create/',views.CreatePostView.as_view(),name='create'),
    url(
    r'(?P<slug>[\w\-]{10})/$',
    views.DetailPostView.as_view(),
    name='view'
),
 path('allposts/', views.AllPostsView.as_view(), name='AllPostsView'),
]
