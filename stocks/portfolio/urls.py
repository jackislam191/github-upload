from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio_overview, name='overview'),
    path('testplotly/',views.home, name='testplotly'),
    path('dashboard/',views.portfolio_dashboard, name='dashboard'),
    path('efficient_frontier/', views.efficient_frontier_select, name='efficientfrontier'),
    path('efficient_frontier_process/', views.efficient_frontier_post, name='efprocess'),
]
