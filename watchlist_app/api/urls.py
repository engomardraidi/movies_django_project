from django.urls import path
from . import views 

urlpatterns = [
    path('list/', views.MovieList.as_view(), name = 'movie_list'),
    path('<int:pk>/', views.MovieDetail.as_view(), name = 'movie_details')
]