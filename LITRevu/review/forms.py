from django import forms

from . import models



class TicketForm(forms.ModelForm):
    edit_ticket_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image'
        }
        

class DeleteForm(forms.Form):
    delete_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label='Note'
    )

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre',
            'rating': 'Note',
            'body': 'Commentaire'
        }
        
        



# class FollowUsersForm(forms.ModelForm):
#     followed_user = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
#         label=''
#     )

#     class Meta:
#         model = UserFollow
#         fields = ['followed_user']








class FollowUsersForm(forms.Form):
    followed_user = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
        label=''
    )
