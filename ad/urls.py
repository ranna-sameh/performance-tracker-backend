
from .views import AdListView, AdDetailedView
from django.urls import path

urlpatterns = [
    path('', AdListView.as_view(), name='ads-list'),
    path('<int:pk>', AdDetailedView.as_view(),
         name='ad-details'),

]
