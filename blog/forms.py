from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=25)
    to = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('email', 'body')


