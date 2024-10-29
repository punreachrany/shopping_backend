from django.urls import path
from .views import (
    ConcertListView,
    ConcertDetailView,
    ConcertCreateView,
    AvailableConcertsView,
    BookConcertView,
    UserConcertsView,
)

urlpatterns = [
    path('all/', ConcertListView.as_view(), name='concert-list'),
    path('<int:pk>/', ConcertDetailView.as_view(), name='concert-detail'),
    path('create/', ConcertCreateView.as_view(), name='concert-create'),
    path('available/', AvailableConcertsView.as_view(), name='available-concerts'),
    path('book/<int:pk>/', BookConcertView.as_view(), name='book-concert'),
    path('mine/', UserConcertsView.as_view(), name='my-concerts'),
]
