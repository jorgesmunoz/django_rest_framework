from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter
#from watchlist_app.api.views import movie_details, movie_list
from watchlist_app.api.views import (
    ReviewDetail,
    ReviewCreate,
    StreamPlatformAV,
    StreamPlatformDetailAV,
    WatchListAV,
    WatchDetailAV,
    ReviewList,
    StreamPlatformVS,
    UserReview,
    WatchListFilterSearch
)

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie-detail'),
    path('new-list/', WatchListFilterSearch.as_view(), name='watch-list'),

    # path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(),
    #      name='streamplatform-detail'),
    path('', include(router.urls)),

    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetail.as_view(),
    #      name='review-detail'),

    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create/',
         ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>/', ReviewDetail.as_view(),
         name='review-detail'),

    # Filtering against the current user and query parameters
    # path('reviews/<str:username>/', UserReview.as_view(),
    #      name='user-review-detail'),

    # Filtering against the URL
    # re_path('^reviews/(?P<username>.+)/$', UserReview.as_view()),

    # Filtering against query parameters
    path('reviews/', UserReview.as_view(),
         name='user-review-detail'),
]
