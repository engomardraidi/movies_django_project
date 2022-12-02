from django.urls import path
from . import views 

urlpatterns = [
    path('list/', views.WatchListView.as_view(), name = 'watch_list_view'),
    path('<int:pk>/', views.WatchListDetailView.as_view(), name = 'watch_list_details_view'),
    path('stream/', views.StreamPlatformView.as_view(), name = 'stream_platform_view'),
    path('stream/<int:pk>', views.StreamPlatformDetailsView.as_view(), name = 'stream_platform_details_view'),
    path('review/', views.ReviewList.as_view(), name = 'review_list_view'),
    path('review/<int:pk>', views.ReviewDetails.as_view(), name = 'review_details_view'),
]