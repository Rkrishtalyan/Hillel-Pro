"""
Views for the web_site app.

This module defines class-based views for handling requests and rendering
templates in the web_site application.
"""

from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import View

from web_site.forms import ArticleForm
from web_site.models import Article
from web_site.forms import RegistrationForm
from web_site.utils import fetch_reviewed_news_articles


class HomePageView(TemplateView):
    """
    View for rendering the home page.

    :var template_name: The path to the template for the home page.
    """
    template_name = 'web_site/home.html'


class RegisterView(FormView):
    """
    View for user registration.

    Handles the display of the registration form and user creation upon form submission.

    :var template_name: The path to the template for the registration page.
    :var form_class: The form class used for user registration.
    :var success_url: The URL to redirect to upon successful registration.
    """
    template_name = 'web_site/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Save the form data to create a new user and proceed with the valid response.

        :param form: The submitted registration form.
        :type form: RegistrationForm
        :return: The HTTP response for a successful form submission.
        :rtype: HttpResponse
        """
        form.save()  # Save the new user
        return super().form_valid(form)


# Task 8

class ReviewedNewsView(TemplateView):
    """
    View for displaying reviewed news articles.

    Retrieves articles in the 'news' category that have been reviewed and passes
    them to the template context.

    :var template_name: The path to the template for displaying reviewed news.
    """
    template_name = 'web_site/reviewed_news.html'

    def get_context_data(self, **kwargs):
        """
        Retrieve context data for rendering the template.

        Adds reviewed news articles to the context.

        :param kwargs: Additional context keyword arguments.
        :type kwargs: dict
        :return: The context dictionary.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        articles = fetch_reviewed_news_articles()
        context['articles'] = articles
        return context


# Task 10

class ArticleCreateView(View):
    """
    View for creating new articles.

    Handles both GET and POST requests for rendering the form and saving new articles.

    :var template_name: The path to the template for the article creation form.
    """
    template_name = 'article_form.html'

    def get(self, request):
        """
        Render the article creation form.

        :param request: The HTTP GET request.
        :type request: HttpRequest
        :return: The HTTP response with the rendered form.
        :rtype: HttpResponse
        """
        form = ArticleForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Handle form submission and create a new article.

        If the form is valid, a new article is created and the user is redirected
        to the home page. If invalid, the form is re-rendered with errors.

        :param request: The HTTP POST request.
        :type request: HttpRequest
        :return: The HTTP response for the form submission.
        :rtype: HttpResponse
        """
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
