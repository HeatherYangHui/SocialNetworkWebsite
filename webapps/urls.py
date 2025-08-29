"""
URL configuration for webapps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialnetwork import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_action, name='login'),
    path('', views.home_view, name='home'),
    path('register/', views.register_action, name='register'),
    path('logout/', views.logout_action, name='logout'),
    path('global_stream/', views.global_stream_action, name='global_stream'),
    path('follower_stream/', views.follower_stream_view, name='follower_stream'),
    path('myprofile/', views.my_profile, name='my_profile'),  # No username required
    path('profile/<int:user_id>/', views.other_profile, name='profile'),
    path('otherprofile/<int:user_id>/', views.other_profile, name='other_profile'),
    path('profile/<int:user_id>/follow/', views.follow, name='follow'),
    path('profile/<int:user_id>/unfollow/', views.unfollow, name='unfollow'),
    path('photo/<int:user_id>/', views.photo, name='photo'),
    path("socialnetwork/get-global", views.get_global, name="get_global"),
    path("socialnetwork/get-follower", views.get_follower, name="get_follower"),
    path('socialnetwork/add-comment', views.add_comment, name='add_comment'),
    # path("global_stream/", views.add_comment, name="add_comment"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
