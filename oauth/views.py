from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from django.views import generic
from .models import Profile
from .profileform import ProfileModelForm
from django.urls import reverse, reverse_lazy


# Create your views here.
class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'oauth/profile.html'

    # def get(self, request, *args, **kwargs):
        # form = ProfileModelForm
        # return render(request, 'updateProfile.html', {'form': form})
    def get_obj(self):
        return self.request.user


class EditProfileView(generic.UpdateView):
    model = Profile
    template_name = 'oauth/updateProfile.html'
    form_class = ProfileModelForm

    # TODO consider moving away from a primary-key based URL, just use user object instead.
    # TODO handle 404s better when pk is not own. Tests needed 
    def get_obj(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('profile')

    def post(self, request, *args, **kwargs):
        form = ProfileModelForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            profile = self.get_obj()
            profile.bio = cd['bio']
            profile.height = cd['height']
            profile.weight = cd['weight']
            profile.points = cd['points']
            profile.save()

            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, 'oauth/updateProfile.html', {'form': form})




