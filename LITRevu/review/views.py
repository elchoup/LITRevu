from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db import IntegrityError
from django.db.models import Q
from itertools import chain

from . import forms
from . import models
from authentication.models import User, UserFollow


@login_required
def home(request):
    user_follow = UserFollow.objects.filter(user=request.user)
    followed_users = [user.followed_user for user in user_follow]
    followed_users.append(request.user)
    tickets = models.Ticket.objects.filter(user__in=followed_users)
    reviews = models.Review.objects.filter(Q(user__in=followed_users)
                                           | Q(ticket__user=request.user))
    posts = list(chain(tickets, reviews))
    posts.sort(key=lambda x: x.time_created, reverse=True)
    return render(request,
                  'review/home.html',
                  context={'posts': posts})


@login_required
def create_ticket(request):
    """ function to create a ticket with a form.
    We check if the user want to post a ticket and save it"""
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request,
                  'review/create_ticket.html',
                  context={'ticket_form': ticket_form})


@login_required
def create_review(request, ticket_id):
    """ Function to create a review of a ticket
    Args = the id of the ticket we want to make a review on.
    We recreate the ticket object with the id and use a form
    to create the review """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
    return render(request,
                  'review/create_review.html',
                  {'review_form': review_form, 'ticket': ticket})


@login_required
def create_ticket_and_review(request):
    """ Function to create a ticket and his review directly """
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            """ Saving the ticket first """
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
    return render(request,
                  'review/create_ticket_and_review.html',
                  {'ticket_form': ticket_form, 'review_form': review_form})


@login_required
def your_posts(request):
    """ fucntion to get all the post of the connected user"""
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    """ make a list of tickets and reviews object and sort it by date time"""
    posts = list(chain(tickets, reviews))
    posts.sort(key=lambda x: x.time_created, reverse=True)
    return render(request,
                  'review/your_posts.html',
                  context={'posts': posts})


@login_required
def edit_tickets(request, ticket_id):
    """ Function to edit a ticket
    args = ticket id
    Recreate the ticket object with the id and keep
    the instance to create the ticket form and modify it """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_ticket_form = forms.TicketForm(instance=ticket)
    if ticket.user == request.user:
        if request.method == 'POST':
            if 'edit_ticket_form' in request.POST:
                edit_ticket_form = forms.TicketForm(request.POST,
                                                    request.FILES,
                                                    instance=ticket)
                if edit_ticket_form.is_valid():
                    edit_ticket_form.save()
                    return redirect('your_posts')
    return render(request,
                  'review/edit_ticket.html',
                  context={'edit_ticket_form': edit_ticket_form})


@login_required
def edit_reviews(request, review_id):
    """ Function to edit a review
    args = review id
    Recreate the review object with the id and keep
    the instance to create the review form and modify it """
    review = get_object_or_404(models.Review, id=review_id)
    edit_review_form = forms.ReviewForm(instance=review)
    if review.user == request.user:
        if request.method == 'POST':
            edit_review_form = forms.ReviewForm(request.POST, instance=review)
            if edit_review_form.is_valid():
                edit_review_form.save()
                return redirect('your_posts')

    return render(request,
                  'review/edit_review.html',
                  {'edit_review_form': edit_review_form})


@login_required
def delete_tickets(request, ticket_id):
    """ Function to delete a ticket
    args = ticket id """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    delete_ticket_form = forms.DeleteForm()
    if ticket.user == request.user:
        if request.method == 'POST':
            delete_ticket_form = forms.DeleteForm(request.POST)
            if delete_ticket_form.is_valid():
                ticket.delete()
                return redirect('your_posts')
    return render(request,
                  'review/delete_ticket.html',
                  {'delete_ticket_form': delete_ticket_form})


@login_required
def delete_reviews(request, review_id):
    """ Function to delete a review
    args = review id """
    review = get_object_or_404(models.Review, id=review_id)
    delete_review_form = forms.DeleteForm()
    if review.user == request.user:
        if request.method == 'POST':
            delete_review_form = forms.DeleteForm(request.POST)
            if delete_review_form.is_valid():
                review.delete()
                return redirect('your_posts')
    return render(request,
                  'review/delete_review.html',
                  {'delete_review_form': delete_review_form})


@login_required
def follow_users_form(request):
    form = forms.FollowUsersForm()
    followed_user = None
    following_users = UserFollow.objects.filter(user=request.user)
    followed_users = UserFollow.objects.filter(followed_user=request.user)

    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['followed_user']

            try:
                followed_user = get_object_or_404(User, username=username)
            except Http404:
                form.add_error(None,
                               'L\'utilisateur recherché n\'a pas été trouvé')
                return render(request,
                              'review/follow_users.html',
                              context={'form': form,
                                       'following_users': following_users,
                                       'followed_users': followed_users})

            if followed_user == request.user:
                form.add_error(None,
                               'Vous ne pouvez pas vous suivre vous même')
                return render(request,
                              'review/follow_users.html',
                              context={'form': form,
                                       'following_users': following_users,
                                       'followed_users': followed_users})
            else:
                try:
                    sub = UserFollow(user=request.user,
                                     followed_user=followed_user)
                    sub.save()
                except IntegrityError:
                    form.add_error(None, 'Vous suivez déjà cet utilisateur')
                    return render(request,
                                  'review/follow_users.html',
                                  context={'form': form,
                                           'following_users': following_users,
                                           'followed_users': followed_users})
    return render(request,
                  'review/follow_users.html',
                  context={'form': form,
                           'following_users': following_users,
                           'followed_users': followed_users})


@login_required
def unfollow_user(request, followed_user_id):
    followed_user = get_object_or_404(User, id=followed_user_id)
    user_follow = get_object_or_404(UserFollow, user=request.user,
                                    followed_user=followed_user)
    if request.method == 'POST':
        if user_follow.user == request.user:
            user_follow.delete()
    return redirect('users_follow')
