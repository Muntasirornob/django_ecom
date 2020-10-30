from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
# Create your views here.

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate




from App_login.models import Profile 
from App_login.forms import ProfileForm ,SignUpForm


from django.contrib import messages


def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            form.save()
            messages.success(request,"Account has been created")
            
            return HttpResponseRedirect(reverse('App_login:login'))
    return render(request, 'App_login/sign_up.html', context={'form':form})

def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_shop:home'))
    return render(request, 'App_login/login.html', context={'form':form})

@login_required
def logout_user(request):
    logout(request)
    messages.warning(request,"You are logged out")
    
    return HttpResponseRedirect(reverse('App_shop:home'))

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Saved")
            form = ProfileForm(instance=profile)
    return render(request, 'App_Login/change_profile.html', context={'form':form})
