"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from gnt import views as gnt_views
import gnt.db_api as gnt_db_api
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('about/', gnt_views.about, name='about'),
    path('admin/', admin.site.urls),
    path('', gnt_views.home, name='home'),
    path('timeline/', gnt_views.timeline, name='timeline'),
    path('results/', gnt_views.results, name='results'),
    path('register/', gnt_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='gnt/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='gnt/logout.html'), name='logout'),
    path('profile-create-drink', gnt_views.profile_create_drink,
         name='profile_create_drink'),
    path('profile/<username>/friends/', gnt_views.friends, name='friends'),
    path('profile-edit/', gnt_views.profile_edit, name='profile_edit'),
    path('profile/<username>/', gnt_views.profile_public, name='profile_public'),
    path('notifications/<username>', gnt_views.notifications, name='notifications'),
    path('liked_drinks/', gnt_views.liked_drinks, name='liked_drinks'),
    path('get_liked_disliked_drinks/', gnt_db_api.get_liked_disliked_drinks,
         name='get_liked_disliked_drinks'),
    path('like_drink/', gnt_db_api.like_drink, name='like_drink'),
    path('remove_liked_drink/', gnt_db_api.remove_liked_drink,
         name='remove_liked_drink'),
    path('disliked_drinks/', gnt_views.disliked_drinks, name='disliked_drinks'),
    path('dislike_drink/', gnt_db_api.dislike_drink, name='dislike_drink'),
    path('remove_disliked_drink/', gnt_db_api.remove_disliked_drink,
         name='remove_disliked_drink'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='gnt/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='gnt/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='gnt/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='gnt/password_reset_complete.html'),
         name='password_reset_complete'),
    path('search/', gnt_views.search, name='search'),
    # Following two lines handle all non matching urls
    re_path(r'^(?P<path>.*)/$', gnt_views.bad_request, name='bad_request'),
    path('', gnt_views.home, name='empty')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
