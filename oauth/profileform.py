from django import forms
from .models import Profile


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["height","weight","bio",]
        #exclude = {"user",}
        #label = {
        #    "height": "Height",
        #    "weight": "Weight",
        #    "points": "points",
        #    "bio": "Bio"
        #}
