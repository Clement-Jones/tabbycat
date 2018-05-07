from django.urls import path

from . import views

urlpatterns = [
    path('',
        views.PublicDrawForCurrentRoundView.as_view(),
        name='draw-public-current-round'),
    path('round/<int:round_seq>/',
        views.PublicDrawForRoundView.as_view(),
        name='draw-public-for-round'),
    path('all/',
        views.PublicAllDrawsAllTournamentsView.as_view(),
        name='draw-public-all-draws'),
    path('sides/',
        views.PublicSideAllocationsView.as_view(),
        name='draw-public-side-allocations'),
]
