from django import forms


class ContactForm(forms.Form):
    sujet = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
