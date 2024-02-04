from django.shortcuts import render
from django.views.generic import FormView
from . forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from books.models import Borrow
from books.models import Book
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Create your views here.
class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    

# @method_decorator(login_required, name='dispatch')
# class ProfileView(View):
#     template_name = 'update_profile.html'

#     def get(self, request, *args, **kwargs):
#         borrows = Borrow.objects.filter(user = request.user)
#         return render(request, self.template_name, {'borrows': borrows})

@login_required
def profile(request):
    data = Book.objects.filter(profile=request.user)
    borrows = Borrow.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'data': data, 'borrows':borrows})








@method_decorator(login_required, name='dispatch')
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


@method_decorator(login_required, name='dispatch')
class UserProfileUpdateView(View):
    template_name = 'accounts/update_profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
        return render(request, self.template_name, {'form': form})

