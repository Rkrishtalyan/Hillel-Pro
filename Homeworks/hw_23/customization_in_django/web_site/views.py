from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy

from web_site.forms import RegistrationForm
from web_site.utils import fetch_reviewed_news_articles


class HomePageView(TemplateView):
    template_name = 'home.html'


class RegisterView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()  # Save the new user
        return super().form_valid(form)


# Task 8

class ReviewedNewsView(TemplateView):
    template_name = 'reviewed_news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = fetch_reviewed_news_articles()
        context['articles'] = articles
        return context
