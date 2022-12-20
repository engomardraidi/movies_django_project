from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'stream', views.StreamPlatformVS, basename = 'streamplatform')

urlpatterns = [
    path('list/', views.WatchListView.as_view(), name = 'watch-list-view'),
    path('<int:pk>/', views.WatchListDetailView.as_view(), name = 'watch-list-details-view'),
    path('', include(router.urls)),
    # path('stream/', views.StreamPlatformView.as_view(), name = 'stream-platform-view'),
    # path('stream/<int:pk>', views.StreamPlatformDetailsView.as_view(), name = 'stream-platform-details-view'),
    path('<int:pk>/review-create/', views.ReviewCreate.as_view(), name = 'stream-platform-review-create-view'),
    path('<int:pk>/reviews/', views.ReviewList.as_view(), name = 'stream-platform-review-view'),
    path('review/<int:pk>/', views.ReviewDetails.as_view(), name = 'review-details-view'),
    path('reviews/', views.UserReview.as_view(), name = 'user-review'),
    path('reviews/', views.UserReview.as_view(), name = 'user-review'),
    path('list2/', views.WatchListTest.as_view(), name = 'list-2'),
    # path('review/', views.ReviewList.as_view(), name = 'review-list-view'),
    # path('review/<int:pk>', views.ReviewDetails.as_view(), name = 'review-details-view'),
]