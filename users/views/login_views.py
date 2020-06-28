from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import Group

from ..models import User
from shop.models import Order

from ..forms import LoginForm, SignUpForm, UserProfileForm


def create_or_get_group(group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        group = Group.objects.create(name=group_name)
    return group


class LoginView(View):
    template_name = 'users/login.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context["form"] = LoginForm()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            credential = {"password": form.cleaned_data["password"]}

            if form.check_email():
                credential["email"] = form.cleaned_data["username"]
            else:
                credential["username"] = form.cleaned_data["username"]

            user = authenticate(request, **credential)
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome %s!" % user.get_full_name())
                return redirect('shop:home')
            else:
                messages.error(request, "Username and/or password does not exist")
                return redirect('users:login')

        self.context["form"] = form
        return render(request, self.template_name, self.context)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'You have successfully logged out!')
        return redirect('users:login')


class SignUpView(View):
    model = User
    template_name = 'users/sign_up.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context["form"] = SignUpForm()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                gender=form.cleaned_data["gender"],
                user_type=form.cleaned_data["user_type"],
                password=form.cleaned_data["confirm_password"],
                email=form.cleaned_data["email"],
                phone_number=form.cleaned_data["phone_number"]
            )

            user.groups.add(create_or_get_group(user.user_type))

            user = authenticate(request,
                                username=form.cleaned_data["username"],
                                password=form.cleaned_data["confirm_password"])
            login(request, user)
            # redirect to profile view
            messages.success(self.request, "Sign up successful")
            return redirect('shop:home')

        self.context["form"] = form
        return render(request, self.template_name, self.context)


class UserProfileView(LoginRequiredMixin, View):
    model = User
    template_name = 'users/profile.html'
    context = {}

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return redirect('users:sign_up')

        self.context['form'] = UserProfileForm(instance=user)
        self.context['user_order'] = Order.get_user_pending_order(request.user),
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return redirect('users:sign_up')

        form = UserProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Updating profile failed")
        return redirect('users:profile')
