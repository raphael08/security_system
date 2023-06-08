from django.urls import path
from . import views

#paths for account app.
urlpatterns = [
    path('', views.deviceView, name='fridge_url'),
    path('createDevice/', views.createDevice, name='createDevice'),
    path('updateDevice/', views.updateDevice, name='updateDevice'),
    path('userFList/', views.userFList, name='userFList_url'),
    # path('userFridge/', views.UserFridgeView, name='userFridge_url'),
    path('update/<str:deviceno>', views.update, name='update'),
    # path('deleteUserFridge/<str:pk>', views.deleteUserFridgeView, name='deleteUserFridge_url'),
    path('deviceMapView/', views.deviceMapView, name='deviceMapView'),
    path('map/<str:deviceno>/<str:latitude>/<str:longitude>', views.map, name='map'),
    path('location', views.location, name='location'),
    
    # path('drinkOrder/', views.DrinkOrderView, name='drinkOrder_url'),
    # path('makeDOrder/', views.MakeDOrderView, name='makeDOrder_url'),
    # path('requestOAList/', views.RequestOAListiew, name='requestOAList_url'),
 
]
