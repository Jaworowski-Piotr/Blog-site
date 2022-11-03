from django import forms
from .models import Comments, Subscribe


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content', 'email', 'name', 'website']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Type your comment...'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['website'].widget.attrs['placeholder'] = 'Website(optional)'


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'