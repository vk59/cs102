import random
from decouple import config

from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from django.shortcuts import redirect
from .forms import UserCreationForm

from django.core.mail import send_mail


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        email = self.request.POST['email']
        password = self.request.POST['password1']

        user = authenticate(email=email, password=password)

        secret = str(random.random())
        secret_key = ''
        for i in range(2, 17):
            secret_key += secret[i]
        user.secret_key = secret_key

        user.save()
        login(self.request, user)

        send_mail(
            "Confirm your account",
            f"To confirm your email in Elevennote, click this link:\nhttp://localhost:8000/accounts/confirm/{user.secret_key}",
            'snegovivan78@gmail.com',
            recipient_list=[email],
            fail_silently=False
        )

        return super(RegisterView, self).form_valid(form)


def ConfirmView(request, secret_key):
    msg = "fail"
    if request.user.secret_key == secret_key:
        request.user.is_confirmed = True
        request.user.save()
        msg = "success"

    return redirect(f"/notes/?msg={msg}")
