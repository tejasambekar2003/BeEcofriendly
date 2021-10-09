from django.conf.urls import url
from django.urls.conf import path
from . import views
from django.conf import settings


app_name = 'posts'

urlpatterns = [
    path('drive/<str:pk_drive>/create/',views.CreatePostView.as_view(),name='create'),
    url(
    r'(?P<slug>[\w\-]{10})/$',
    views.DetailPostView.as_view(),
    name='view'
),
 path('drive/<str:pk_drive>/allposts/', views.drive_all_posts, name='drive_all_posts'),
 path('drive/<str:pk_drive>/post/', views.drive_posts, name='imagepost'),
]
