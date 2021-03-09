from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search_stock', views.search_stock_data, name='search_stock'),
    path('about', views.about, name='about'),
    path('add_stock', views.add_stock, name='add_stock'),
    path('delete/<stock_symbol>', views.delete, name='delete'),
    path('portfolio', views.portfolio, name='portfolio'),
]