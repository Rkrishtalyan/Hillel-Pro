from web_site.models import Article


# Task 8

def fetch_reviewed_news_articles():
    return Article.objects.raw("SELECT * FROM web_site_article WHERE category = %s AND reviewed = %s", ['news', True])
