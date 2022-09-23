from django import forms


class EmailPostForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=25)
    to = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)
