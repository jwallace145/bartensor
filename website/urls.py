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
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('about/', gnt_views.about, name='about'),
    path('admin/', admin.site.urls),
    path('', gnt_views.home, name='home'),
    path('results/', gnt_views.results, name='results'),
    path('loading/', gnt_views.loading, name='loading'),
    path('register/', gnt_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='gnt/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='gnt/logout.html'), name='logout'),
    path('profile/', gnt_views.profile, name='profile'),
    path('liked_drinks/', gnt_views.liked_drinks, name='liked_drinks'),
    path('like_drink/', gnt_views.like_drink, name='like_drink'),
    path('remove_liked_drink/', gnt_views.remove_liked_drink, name='remove_liked_drink'),
    path('dislike_drink/', gnt_views.dislike_drink, name='dislike_drink'),
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
    # Following two lines handle all non matching urls
    re_path(r'^(?P<path>.*)/$', gnt_views.bad_request, name='bad_request'),
    path('', gnt_views.home, name='empty')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
