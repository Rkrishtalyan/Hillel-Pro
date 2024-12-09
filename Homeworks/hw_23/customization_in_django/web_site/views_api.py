from rest_framework import generics

from web_site.models import Article
from web_site.serializers import ArticleSerializer
from web_site.permissions import IsAuthenticatedOrReadOnly
from web_site.filters import ArticleFilter


#Task 7

class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permissions_classes = (IsAuthenticatedOrReadOnly,)
    filterset_class = ArticleFilter


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permissions_classes = (IsAuthenticatedOrReadOnly,)
