from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'stream', views.StreamPlatformVS, basename = 'streamplatform')

urlpatterns = [
    path('list/', views.WatchListView.as_view(), name = 'watch_list_view'),
    path('<int:pk>/', views.WatchListDetailView.as_view(), name = 'watch_list_details_view'),
    path('', include(router.urls)),
    # path('stream/', views.StreamPlatformView.as_view(), name = 'stream_platform_view'),
    # path('stream/<int:pk>', views.StreamPlatformDetailsView.as_view(), name = 'stream_platform_details_view'),
    path('<int:pk>/review-create/', views.ReviewCreate.as_view(), name = 'stream_platform_review_create_view'),
    path('<int:pk>/reviews/', views.ReviewList.as_view(), name = 'stream_platform_review_view'),
    path('review/<int:pk>', views.ReviewDetails.as_view(), name = 'review_details_view'),
    # path('review/', views.ReviewList.as_view(), name = 'review_list_view'),
    # path('review/<int:pk>', views.ReviewDetails.as_view(), name = 'review_details_view'),
]