from django.urls import path

from . import views


urlpatterns = [
    path('list/', views.book_list, name='book_list'),
    path('unoptimized/', views.unoptimized_book_list, name='unoptimized_book_list'),
    path('optimized/', views.optimized_book_list, name='optimized_book_list'),
    path('upload/', views.upload_books_csv, name='upload_books_csv'),
    path('task/<str:task_id>/', views.task_status, name='task_status'),
    path('orm_queries/', views.orm_queries, name='orm_queries'),
    path('raw_sql_queries/', views.AuthorBookReviewView.as_view(), name='raw_sql_queries'),
    path('no_sql_orm_queries/', views.no_sql_orm_queries, name='no_sql_orm_queries'),
]
