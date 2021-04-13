from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio_overview, name='overview'),
    path('dashboard/',views.portfolio_dashboard, name='dashboard'),
    path('edit_holding/<pk>', views.edit_holding, name='edit_holding'),
    path('delete_dashboard/<pk>', views.delete_dashboard, name='del_dashboard'),
    path('efficient_frontier/', views.efficient_frontier_select, name='efficientfrontier'),
    path('efficient_frontier_process/', views.efficient_frontier_post, name='efprocess'),
    path('delete_portfolio/<stock_symbol>',views.delete, name='delete'),
    path('save_in_portfolio/', views.save_in_portfolio, name='save-to-portfolio'),
    path('output_csv_test/', views.output_df_csv, name='output-csv-test')
]
