"""
URL configuration for LITRevu project.

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
from django.contrib.auth.views import (
    LoginView, LogoutView
)

import authentication.views
import review.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
        ),
        name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', authentication.views.signup_form, name='signup'),
    path('home/', review.views.home, name='home'),
    path('create-ticket/', review.views.create_ticket, name='create_ticket'),
    path('home/<int:ticket_id>/create_review/', review.views.create_review,
         name='create_review'),
    path('create_ticket_and_review/', review.views.create_ticket_and_review,
         name='create_ticket_and_review'),
    path('users_follow/', review.views.follow_users_form, name='users_follow'),
    path('your-posts/', review.views.your_posts, name='your_posts'),
    path('edit-ticket/<int:ticket_id>', review.views.edit_tickets,
         name='edit_ticket'),
    path('delete-ticket/<int:ticket_id>', review.views.delete_tickets,
         name='delete_ticket'),
    path('edit-review/<int:review_id>', review.views.edit_reviews,
         name='edit_review'),
    path('delete-review/<int:review_id>', review.views.delete_reviews,
         name='delete_review'),
    path('unfollow_user/<int:followed_user_id>/', review.views.unfollow_user,
         name='unfollow_user'),
]
