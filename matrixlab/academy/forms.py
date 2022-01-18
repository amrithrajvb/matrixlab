from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from academy.models import MyUser, Worknotes


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = MyUser
        fields = ["email","phone","password1", "password2"]
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "phone":forms.NumberInput(attrs={"class":"form-control"}),
        }

    def __str__(self):
        return self.id

class SigninForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

class Notes(ModelForm):

    class Meta:
        model=Worknotes
        fields = ["title","notes","notes_image"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-textarea"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data["title"]
        print("title", title)
        titles = Worknotes.objects.filter(title__iexact=title)
        print("title", titles)
        if titles:
            msg = "The title is already exist"
            self.add_error("title", msg)