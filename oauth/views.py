from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse
from django.template import loader

from .models import Profile
from .profileform import ProfileModelForm


def index(request):
    print('Test')
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    template = loader.get_template('oauth/index.html')
    return HttpResponse(template.render({}, request))

# Entrypoint for the url /profile/
# We default to showing the logged in user's profile when not given a specifc ID, redirecting to index when not authenticated.
def self_profile(request):
    if not request.user.is_authenticated: 
        return HttpResponseRedirect(reverse('index')) # TODO show message on index page to login
    
    return ProfileView.as_view()(request, pk=request.user.id) # as_view returns a callable, must give request + kwargs

# Entrypoint for /profile/<int:profile_id>/ , gets a specific profile from profile pk
# Does not require authentication, so even not logged in users can view.
# TODO improve 404 page
# TODO consider privacy settings - everyone, only logged in users, only friends, fully private
def specific_profile(request, profile_id):
    if not Profile.objects.filter(pk=profile_id).exists():
        return HttpResponseNotFound('Error: profile with that ID not found')
    return ProfileView.as_view()(request, pk=profile_id)
    
class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'oauth/profile.html'
    context_object_name = 'displayed_profile'

    # TODO replace the PK in the URL with a UUID, prevents leaking signup order
    def get_object(self):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        return profile


# Entrypoint for /profile/edit.
def edit_or_redirect(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    return EditProfileView.as_view()(request, pk=request.user.id)

class EditProfileView(generic.UpdateView):
    model = Profile
    template_name = 'oauth/updateProfile.html'
    form_class = ProfileModelForm

    # TODO consider moving away from a primary-key based URL, just use user object instead.
    # TODO handle 404s better when pk is not own. Tests needed 
    # TODO make sure can only update when trying to edit own profile
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
            #profile.points = cd['points']
            profile.save()

            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, 'oauth/updateProfile.html', {'form': form})



