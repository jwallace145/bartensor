"""
Website URL Configuration Module
"""

# import necessary modules
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

import gnt.db_api as gnt_db_api
from gnt import views as gnt_views

urlpatterns = [
    # admin site url pattern
    path('admin/', admin.site.urls),

    # general url patterns
    path('', gnt_views.home, name='home'),
    path('about/', gnt_views.about, name='about'),
    path('more_results/', gnt_views.more_results, name='more_results'),
    path('results/', gnt_views.results, name='results'),
    path('search/', gnt_views.search, name='search'),
    path('timeline/', gnt_views.timeline, name='timeline'),
    path('timeline_pop/', gnt_views.timeline_pop, name='timeline_pop'),
    path('get_lucky/', gnt_views.get_lucky, name='get_lucky'),

    # login, logout, register url patterns
    path('login/', auth_views.LoginView.as_view(template_name='gnt/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='gnt/logout.html'), name='logout'),
    path('register/', gnt_views.register, name='register'),

    # profile url patterns
    path('profile/<username>/create-drink', gnt_views.profile_create_drink, name='create_drink'),
    path('profile/<username>/disliked-drinks/', gnt_views.disliked_drinks, name='disliked_drinks'),
    path('profile/<username>/edit', gnt_views.profile_edit, name='profile_edit'),
    path('profile/<username>/friends/', gnt_views.friends, name='friends'),
    path('profile/<username>/liked-drinks', gnt_views.liked_drinks, name='liked_drinks'),
    path('profile/<username>/notifications', gnt_views.notifications, name='notifications'),
    path('profile/<username>/timeline', gnt_views.profile_public, name='timeline'),

    # db api url patterns
    path('dislike_drink/', gnt_db_api.dislike_drink, name='dislike_drink'),
    path('dislike_user_drink/', gnt_db_api.dislike_user_drink, name='dislike_user_drink'),
    path('get_liked_disliked_drinks/', gnt_db_api.get_liked_disliked_drinks, name='get_liked_disliked_drinks'),
    path('get_liked_disliked_user_drinks/', gnt_db_api.get_liked_disliked_user_drinks, name='get_liked_disliked_user_drinks'),
    path('like_drink/', gnt_db_api.like_drink, name='like_drink'),
    path('like_user_drink/', gnt_db_api.like_user_drink, name='like_user_drink'),
    path('remove_liked_drink/', gnt_db_api.remove_liked_drink, name='remove_liked_drink'),
    path('remove_disliked_drink/', gnt_db_api.remove_disliked_drink, name='remove_disliked_drink'),
    # password reset url patterns
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='gnt/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='gnt/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='gnt/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='gnt/password_reset_complete.html'), name='password_reset_complete'),

    # following two lines handle all non matching urls
    re_path(r'^(?P<path>.*)/$', gnt_views.bad_request, name='bad_request'),
    path('', gnt_views.home, name='empty')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
