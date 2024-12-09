from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy

from web_site.forms import RegistrationForm


class HomePageView(TemplateView):
    template_name = 'home.html'


class RegisterView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()  # Save the new user
        return super().form_valid(form)