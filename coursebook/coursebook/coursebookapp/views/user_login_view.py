from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages

class UserLoginView(LoginView):
    template_name = "pages/login.html"

    def form_invalid(self, form):
        messages.error(self.request, "Nieprawidłowy login lub hasło")
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Zostałeś zalogowany")

        # Dodaj informację o zalogowaniu do ciasteczka
        response.set_cookie('is_logged', 'true')

        return response

    def get_success_url(self):
        return reverse_lazy("account")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("account"))
        return super().dispatch(request, *args, **kwargs)
