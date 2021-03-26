from django.urls import path
from . import views

app_name = 'quotes'
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('search_stock', views.search_stock_data, name='search_stock'),
    path('add_to_portfolio/',views.add_to_portfolio, name='add-to-portfolio'),
    path('existing_stock', views.existing_stock, name='existing_stock'),
    path('delete/<stock_symbol>', views.delete, name='delete'),
    path('portfolio', views.portfolio, name='portfolio'),
]