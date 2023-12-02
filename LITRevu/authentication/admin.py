from django.contrib import admin

from authentication.models import User, UserFollow
from review.models import Ticket, Review

admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollow)