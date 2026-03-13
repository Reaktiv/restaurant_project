from django.db.models.fields import return_None
from django.http import HttpResponse
from django.shortcuts import render, redirect

from account.forms import CustomUserCreationForm, CustomUserChangeForm, ProfileChangeForm
from .models import Profile

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'account/register.html', context=context)

def profile(request):
    return render(request, 'account/profile.html')

def change_profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileChangeForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = ProfileChangeForm(instance=profile)

    context = {
        'u_form': user_form,
        'p_form': profile_form,
    }

    return render(request, 'account/change_profile.html', context)







def password_reset(request):
    pass
