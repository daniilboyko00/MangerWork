from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib import messages

def profile(request):
    return render(request=request, template_name='profile.html')


class RegisterUserView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')


class SignUpView(LoginView):
    redirect_authenticated_user = False
    template_name = 'auth.html'


    def get_success_url(self):
        return reverse_lazy('profile')


    def form_invalid(self,form):
        messages.error(self.request, 'Неправильная почта или пароль')
        return self.render_to_response(self.get_context_data(form=form))



