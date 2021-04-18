from dashboard.models import Exercise
from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse
from django.template import loader

from .models import Profile
from .profileform import ProfileModelForm


def index(request):
    print('Test')
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    template = loader.get_template('oauth/index.html')
    return HttpResponse(template.render({}, request))

# Show a basic list of friends
def friend_list(request):
    profile = Profile.objects.get(pk=1)
    return render(request, template_name='oauth/friends_list.html', context={
        'profile': profile,
        'friends': profile.friends.all(),
    })

# Take in the desired friend PK from POST params
@login_required
def add_friend(request):
    friend_profile = Profile.objects.get(pk=request.POST['new_friend_pk'])
    profile = Profile.objects.get(pk=request.user.profile.pk)
    profile.friends.add(friend_profile)
    profile.save()
@login_required
def remove_friend(request):
    pass

# Entrypoint for the url /profile/
# We default to showing the logged in user's profile when not given a specifc ID, redirecting to index when not authenticated.
def self_profile(request):
    if not request.user.is_authenticated: 
        return HttpResponseRedirect(reverse('index')) # TODO show message on index page to login
    
    # as_view returns a callable, must give request + kwargs
    return ProfileView.as_view()(request, pk=request.user.id, exercise_list=Exercise.objects.filter(owner__exact=request.user.profile.pk).order_by('-entry_date')[:8]) 

# Entrypoint for /profile/<int:profile_id>/ , gets a specific profile from profile pk
# Does not require authentication, so even not logged in users can view.
# TODO improve 404 page
# TODO consider privacy settings - everyone, only logged in users, only friends, fully private
def specific_profile(request, profile_id):
    if not Profile.objects.filter(pk=profile_id).exists():
        return HttpResponseNotFound('Error: profile with that ID not found')
    return ProfileView.as_view()(request, pk=profile_id, exercise_list=Exercise.objects.filter(owner__exact=profile_id).order_by('-entry_date')[:8])
    
class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'oauth/profile.html'
    context_object_name = 'displayed_profile'

    # TODO replace the PK in the URL with a UUID, prevents leaking signup order
    def get_object(self):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        return profile
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        context['exercise_list'] = self.kwargs.get('exercise_list')
        return context


# Entrypoint for /profile/edit.
def edit_or_redirect(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    return EditProfileView.as_view()(request, pk=request.user.id)

class EditProfileView(generic.UpdateView):
    model = Profile
    template_name = 'oauth/updateProfile.html'
    form_class = ProfileModelForm

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

            try:
                new_photo = request.FILES['profile_photo']
                profile.profile_photo = new_photo
            except Exception:
                pass
            profile.save()

            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, 'oauth/updateProfile.html', {'form': form})

class LeaderboardView(generic.ListView):
    model = Profile
    template_name = 'oauth/leaderboard.html'
    context_object_name = 'latest_leaderboard'


