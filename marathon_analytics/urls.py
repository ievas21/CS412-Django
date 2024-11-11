from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResultsListView.as_view(), name = "home"),
    path('results', views.ResultsListView.as_view(), name = "results"),
    path('result/<int:pk>', views.ResultDetailView.as_view(), name = "result_detail"),
]
