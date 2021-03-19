# This file contains signal callbacks that occur during the initial user profile setup.
from django.dispatch import reciever
from allauth.socialaccount.signals import pre_social_login

@reciever(pre_social_login)
def create_profile(sender, **kwargs):
    print('TODO')
    print('TODO')
    print('TODO')
    print(sender)
    print(kwargs)