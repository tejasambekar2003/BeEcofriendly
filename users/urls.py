from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('register/', views.register, name = 'register'),
    path('profile/', views.profile, name = 'profile'),
    path('create-drive/', views.createDrive, name = 'createDrive'),
    path('our-team/', views.ourTeam, name = 'ourTeam'),
    path('drive/join/', views.joinDrive, name = 'joinDrive'),
    path('drive/<str:drive_pk>', views.drive_home, name = 'driveHome'),
    path('drive/join/<str:drive_pk>', views.indi_drive_join, name = 'join_drive_temp'),
    # path('upload/', views.upload, name = 'upload'),
    # path('blog/', views.blog_view, name = 'blog'),
    # path('post/', views.posts, name = 'posts'),
    
    # path('add-participants/', views.add, name = 'add'),

]