from django.urls import path
from . import views

# Ieva sagaitis, ievas@bu.edu

urlpatterns = [
    path('', views.VotersListView.as_view(), name = "home"),
    path('voters', views.VotersListView.as_view(), name = "voters"),
    path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
    path('graphs', views.GraphListView.as_view(), name='graphs'),
]