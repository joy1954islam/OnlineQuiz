from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render
from django.template.loader import render_to_string

from SuperAdmin.forms import ALLUserUpdateForm
from accounts.forms import UserUpdateForm, ChangeEmailForm, ContactForm
from django.views.generic import View, FormView
from django.conf import settings
from django.utils.crypto import get_random_string
from accounts.models import Activation
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from accounts.utils import (
    send_activation_email, send_reset_password_email, send_forgotten_username_email, send_activation_change_email,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
)
from django.contrib.auth import get_user_model

User = get_user_model()


def SuperAdminHome(request):
    return render(request, 'SuperAdmin/Home.html')


def SuperAdminProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('SuperAdminProfile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }
    return render(request, 'SuperAdmin/Profile/SuperAdminProfile.html', context)


class ChangeEmailView(LoginRequiredMixin, FormView):
    template_name = 'SuperAdmin/Profile/change_email.html'
    form_class = ChangeEmailForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        email = form.cleaned_data['email']

        if settings.ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.email = email
            act.save()

            send_activation_change_email(self.request, email, code)

            messages.success(self.request, f'To complete the change of email address, click on the link sent to it.')
        else:
            user.email = email
            user.save()

            messages.success(self.request, f'Email successfully changed.')

        return redirect('SuperAdmin_change_email')


class ChangeEmailActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Change the email
        user = act.user
        user.email = act.email
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, f'You have successfully changed your email!')

        return redirect('SuperAdmin_change_email    ')


class ChangePasswordView(BasePasswordChangeView):
    template_name = 'SuperAdmin/Profile/change_password.html'

    def form_valid(self, form):
        # Change the password
        user = form.save()

        # Re-authentication
        login(self.request, user)

        messages.success(self.request, f'Your password was changed.')

        return redirect('log_in')


from django.shortcuts import render


def contact(request):
    if request.method == 'POST':
        u_form = ContactForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your Contact Send Successfully')
            return redirect('index')
    else:
        u_form = ContactForm()

    context = {
        'form': u_form
    }
    return render(request, 'contact.html', context)


def users_list(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'SuperAdmin/users/users_list.html', context)


def users_view(request, pk):
    student = get_object_or_404(User, pk=pk)
    data = dict()
    context = {'student': student}
    data['html_form'] = render_to_string('SuperAdmin/users/partial_users_view.html', context, request=request)
    return JsonResponse(data)


def users_update(request,pk):
    student = get_object_or_404(User, pk=pk)
    form = ALLUserUpdateForm(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, "User Updated Successfully")
        return redirect("users_list")
    # else:
    #     messages.error(request, "Training Not Updated Successfully")
    return render(request, 'SuperAdmin/users/partial_users_update.html', {'form': form})

