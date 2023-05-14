from django.urls import path, include 
from . import views

app_name = 'web_app'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    #Sales
    path('work_order_forms/', views.work_order_forms, name='work_order_forms'),   # home page for all work order forms 
    path('work_order_forms/<int:work_order_form_number>/', views.work_order_form, name='work_order_form'),   #page for specific work order form
    path('new_work_order_form/', views.new_work_order_form, name='new_work_order_form'), #url for add new work order form

    # Claims
    path('claims/', views.claims, name='claims'),
    path('newclaim/', views.newclaim, name='newclaim'),
    path('viewclaim/<int:claim_number>/', views.viewclaim, name='viewclaim'),
    path('approvedclaims/', views.approvedclaims, name='approvedclaims'),
    path('rejectedclaims/', views.rejectedclaims, name='rejectedclaims'),
    path('validate_vin/', views.validate_vin, name='validate_vin'),

    # Reports
    path('reports/', views.reports, name='reports'),
    path('export-claims-csv/', views.export_claims_csv, name='export_claims_csv'),
    path('export-sales-csv/', views.export_sales_csv, name='export_sales_csv'),
]
