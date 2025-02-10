from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.hashers import make_password
from .models import Users, Comment


class UserCreateForm(ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'username', 'password']



    def clean_password(self):
        password = self.cleaned_data['password']
        print(password)
        return make_password(password)
    

class UserLoginForm(Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add your comment...'})
        }