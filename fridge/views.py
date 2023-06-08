from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import folium
import geocoder
from geopy.geocoders import ArcGIS,Nominatim
from geopy.distance import geodesic
import json
from django.views.decorators.csrf import *
from . models import Device
from uaa.models import User,Profile

from datetime import datetime, timedelta,timezone
#sending email.
from django.conf import settings
from django.core.mail import send_mail

import time as tm
# Create your views here.
def deviceView(request):
    try:
        
        branchObject = Device.objects.all()
        userObject = User.objects.filter(is_active=True)
    except:
        return render(None, 'uaa/error500.html')
    
    context = {'fod':branchObject, 'fo':userObject}
    return render(request, 'fridge/fridge.html', context)

def createDevice(request):
    try:
        if request.method == "POST":
           
            device = request.POST.get('device')
            
            
            checkFridge = Device.objects.filter(deviceId=device).exists()
            if checkFridge:
                messages.info(request,'Device already exist')
                return redirect('fridge_url')
        
            createf = Device.objects.create(
                deviceId=device
            )
            createf.save()
            messages.success(request,'Fridge created succesfully.')
            return redirect('fridge_url')
    
        return redirect('fridge_url')
        
    except:
        return render(None, 'uaa/error500.html')
    
def updateDevice(request):
    try:
        if request.method == "POST":
            FridgeId = request.POST.get('FridgeId')
            deviceId = request.POST.get('deviceId')
            #Capacity = request.POST.get('Capacity')
        
            Device.objects.filter(id=FridgeId).update(
                deviceId=deviceId
            )
            messages.success(request,'Fridge updated succesfully.')
            return redirect('fridge_url')

        return redirect('fridge_url')
        
    except:
        return render(None, 'uaa/error500.html')

def userFList(request):
    try:
       
        userObject = User.objects.filter(is_active=True)
    except:
        return render(None, 'uaa/error500.html')
    
    context = {'uo':userObject}
    return render(request, 'fridge/userFridge.html', context)


    
       

def deviceMapView(request):
    try:
        userFInstance = Device.objects.all()
        
        geolocator = Nominatim(user_agent="my-app")  # Create a geolocat
            
       # Example: Keko coordinates
          # Example: upanga coordinates
        tanzania = (-6.82349,39.26951)
        

        m = folium.Map(location=tanzania, zoom_start=10)
        
        for i in userFInstance:
            origin_position = (float(i.lat), float(i.long))
            origin = geolocator.reverse(origin_position, exactly_one=True)
            if i.status==True:
                folium.Marker(
                    location=(float(i.lat), float(i.long)), 
                    # popup=orgin_place, 
                    popup=f"<b><i><u>Origin Location:</u></i></b> {origin.address}",
                    tooltip=origin.address,
                    icon=folium.Icon(color='green')
                    ).add_to(m)
            else:
               folium.Marker(
                    location=(float(i.lat), float(i.long)), 
                    # popup=orgin_place, 
                    popup=f"<b><i><u>Origin Location:</u></i></b> {origin.address}",
                    tooltip=origin.address,
                    icon=folium.Icon(color='red')
                    ).add_to(m) 
        m = m._repr_html_()
        
    except:
        return render(None, 'uaa/error500.html')

    context = {'m':m}
    return render(request,'map/userFmap.html',context)



################## ************** this map was for demostration  *********** ######################

#http://127.0.0.1:8000/fridge/map?latitude=-6.807639999999935&longitude=39.280410000000074
@csrf_exempt  
def map(request,deviceno,latitude,longitude):
#  try:
    
   

    # Get current date and time
   
    # print("Date and Time 5 Minutes Later:", later_time.strftime("%Y-%m-%d %H:%M:%S"))
    us = Device.objects.filter(deviceId=deviceno).exists()
    
    # lat = UserFridge.objects.get(fridge_id=u.id)
    if us==True:
        # Example: Keko coordinates
        latitude = float(latitude)
        longitude = float(longitude) # Example: upanga coordinates    
        d = Device.objects.filter(deviceId=deviceno).update(lat=latitude,long=longitude,status=False)
 
    
  
       
        #return redirect('dashboard_url')
    return JsonResponse({'lat':latitude,'longitude':longitude})   
#  except:
#     return JsonResponse({'lat':latitude,'longitude':longitude})      


def location(request):
    
    return render(request,'fridge/location.html')


def update(request,deviceno):
#   current_time = datetime.now()
#   #later_time = current_time + timedelta(minutes=5)
# #   current_times = later_time.replace(tzinfo=timezone.utc)
  us = Device.objects.filter(deviceId=deviceno).exists()
  if us:
#   later = us.updatedAt + timedelta(minutes=5)
 
#   later = later.replace(tzinfo=timezone.utc)
# # Get the offset-aware updatedAt datetime
#   updated_at = us.updatedAt.replace(tzinfo=timezone.utc)

#     # Print the values
#   print("updatedAt:", updated_at)
#   print("later_time:", later)
#   print("current:", )
#   if us.status == False:
#         if  later < current_time:
#             Device.objects.filter(deviceId=deviceno).update(status=True)
#             print("hi")
#         else:
#             print('hellow')
   Device.objects.filter(deviceId=deviceno).update(status=True)
   
  else:
      print("False")
  return JsonResponse({'data':us}) 

############### testing codes for decoding origin name to get latitude and longtude.. #########
    # geolocator = Nominatim(user_agent="map_app")
#    current_locationn = geolocator.geocode("UDSM")  # Example: Enter the name of the current location
#     origin_positionn = geolocator.geocode("National institute of transport (NIT)")  # Example: Enter the name of the origin position

#     # current_coords = (current_location.latitude, current_location.longitude)
#     origin_coords = (current_locationn.latitude)   #-6.80297255 39.2218461588523 NIT
#     origin_coord = (current_locationn.longitude) # -6.79301125 39.21296331862601 UDSM
    
#     # print(current_coords)
#     print("printing the latitude and longtude values..")
#     print(origin_coords)
#     print(origin_coord)


