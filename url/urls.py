from django.urls import path
from .views import index, generate_report

app_name = 'url'

urlpatterns = [
    path('', index, name='index'),
    path('submit/<path:path>/', generate_report, name='generate_report'),
]