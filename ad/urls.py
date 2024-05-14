
from .views import AdListView
from django.urls import path

urlpatterns = [
    path('', AdListView.as_view(), name='ads-list'),

]
