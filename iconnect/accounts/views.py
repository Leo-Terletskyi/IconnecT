from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import LoginForm, UserRegisterForm

User = get_user_model()


class UserRegisterView(generic.CreateView):
    template_name = 'accounts/auth/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('sign_in')
    
    
class LoginView(generic.FormView):
    template_name = 'accounts/auth/login.html'
    form_class = LoginForm
    
    def form_valid(self, form):
        data = form.cleaned_data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect('user_acc', pk=user.id)
            else:
                return HttpResponse('Your account is not active')
        return HttpResponse(f'User with username <h1>{username}</h1> does not exists')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('sign_in')


class UserAccDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'accounts/user_acc.html'
    model = User
    context_object_name = 'user'


