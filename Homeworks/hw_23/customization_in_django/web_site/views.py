from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import View

from web_site.forms import ArticleForm
from web_site.models import Article
from web_site.forms import RegistrationForm
from web_site.utils import fetch_reviewed_news_articles


class HomePageView(TemplateView):
    template_name = 'web_site/home.html'


class RegisterView(FormView):
    template_name = 'web_site/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()  # Save the new user
        return super().form_valid(form)


# Task 8

class ReviewedNewsView(TemplateView):
    template_name = 'web_site/reviewed_news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = fetch_reviewed_news_articles()
        context['articles'] = articles
        return context


# Task 10

class ArticleCreateView(View):
    template_name = 'article_form.html'

    def get(self, request):
        form = ArticleForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            category = form.cleaned_data['category']
            contact = form.cleaned_data['contact']

            article = Article.objects.create(
                title=title,
                body=body,
                category=category,
                contact=contact
            )

            return redirect('home')
        return render(request, self.template_name, {'form': form})
