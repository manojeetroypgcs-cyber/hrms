from django.urls import path
from . import views

urlpatterns = [
    path('', views.payslip_list, name='payslip_list'),
    path('create/', views.payslip_create, name='payslip_create'),
    path('<int:pk>/', views.payslip_detail, name='payslip_detail'),
    path('<int:pk>/delete/', views.payslip_delete, name='payslip_delete'),
]