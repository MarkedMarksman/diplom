from django import forms
from .models import User

class UserAvatar(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('user_avatar',)