from django.urls import path
from . import views

app_name='ROBO'

urlpatterns = [
    path('',views.home, name='Home'),
    path('order/', views.order, name='Order'),
    path('getitems/', views.getItems, name='Get_Items'),
    path('getPayTypes/', views.getPayTypes, name='Get_Payment_Types'),
    path('maintenance/', views.maintenance, name='Maintenance'),
    path('additem/', views.additem, name='Additem'),
    path('getSize/', views.getSize, name='GetSize'),
    path('getCategory/', views.getCategory, name='GetCategory'),
    path('report/', views.report, name='Report'),
    path('getOrders/<str:ordersDate>/', views.getOrders, name="GetOrders"),
    path('getMaintenances/<str:maintenanceDate>/', views.getMaintenances, name="GetMaintenances"),
    path('manageOrders/', views.manageOrder, name="ManageOrder"),
    path('getOrdersMonthly/<str:month>/<str:year>/', views.getOrdersMonthly, name="GetOrdersMonthly"),
    path('getMaintenancesMonthly/<str:month>/<str:year>/', views.getMaintenancesMonthly, name="GetMaintenancesMonthly"),
    path('getOrdersYearly/<str:year>/', views.getOrdersYearly, name="GetOrdersYearly"),
    path('getMaintenancesYearly/<str:year>/', views.getMaintenancesYearly, name="GetMaintenancesYearly"),
    path('deleteOrder/<str:orderId>/', views.deleteOrder, name="DeleteOrder"),
    path('login/', views.logIn, name="Login"),
    path('logout/', views.logOut, name="Logout"),
    path('getMainCategory/', views.getMainCategory, name="GetMainCategory"),
    path('editOrder/<int:orderId>/', views.editOrder, name="EditOrder"),
    path('getOrdersById/<int:orderId>/', views.getOrdersById, name="GetOrdersById"),
    path('getDailyReportByPDf/<str:ordersDate>/', views.getDailyReportByPDf, name="GetDailyReportByPDf"),
    path('getMonthlyReportByPDf/<str:month>/<str:year>/', views.getMonthlyReportByPDf, name="GetMonthlyReportByPDf"),
    path('getYearlyReportByPDf/<str:year>/', views.getYearlyReportByPDf, name="GetYearlyReportByPDf"),
]
