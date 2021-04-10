from django import forms
from .models import Profile


class ProfileModelForm(forms.ModelForm):
    profile_photo = forms.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ["height","weight","bio"]
