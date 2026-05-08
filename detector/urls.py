from django.urls import path
from . import views

app_name = 'detector'

urlpatterns = [
    path('', views.analyze_view, name='analyze'),
    path('run/', views.run_analysis, name='run_analysis'),
    path('history/', views.history_view, name='history'),
    path('result/<int:pk>/', views.analysis_detail, name='detail'),
]
