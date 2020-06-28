from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetCompleteView)


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/reset/password_reset_form.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/reset/password_reset_confirm.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/reset/password_reset_done.html'


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/reset/password_reset_complete.html'


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/reset/password_change_form.html'


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/reset/password_change_done.html'
