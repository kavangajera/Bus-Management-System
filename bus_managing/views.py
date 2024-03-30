from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render, redirect
from .models import CustomUser,City_Detail,Route_Detail,CitiesOrder,Distance,Bus_Detail,Bus_Type
from django.contrib import messages
from datetime import datetime,date
from geopy.geocoders import Nominatim
from geopy import distance
from django.db.models import Q

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        role = request.POST['role']
        phone = request.POST['phone']
        
        #validations::
        
        if len(phone)>10 or len(phone)<10:
            messages.error(request,"invalid phone number")
            return redirect('homepage')
        
        if(password!=confirm_password):
            messages.error(request,"enter correct as above password")
            return redirect('homepage')
        user = CustomUser.objects.create_user(username=username, password=password, email=email, role=role,phone=phone)
        
        return redirect('login_view')

    return render(request,'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            if user.role == 'passenger':
                request.session['user_username'] = user.username
                return redirect('passenger')
            else:
                request.session['user_username'] = user.username
                return redirect('govt_agent')
                 
        else:
            messages.success(request,"invalid credentials")
            return redirect('homepage')
    
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    messages.success(request,"logged OUT")
    return redirect('homepage')

def passenger(request):
    return render(request,'passenger.html')

def govt_agent(request):
    return render(request,'govt_agent.html')

def select_route(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        request.session['source'] = source
        request.session['destination'] = destination
        return redirect('choose_bus')
    
    return render(request,'select_route.html',{'cities': City_Detail.objects.all()})

def choose_bus(request):
    busList = []
    cities = []
    fares = []
    dis = 0
    fare_ = 0
    source = request.session.get('source')
    destination = request.session.get('destination')
    source_order = CitiesOrder.objects.filter(city=source)
    destination_order = CitiesOrder.objects.filter(city=destination)
    route_list = []
    for source_city_order in source_order:
        for destination_city_order in destination_order:
            if source_city_order.route == destination_city_order.route:
                route_list.append(source_city_order.route)
    
    for route in route_list:
        route.cities_order = CitiesOrder.objects.filter(route=route).order_by('order')
        for city_order in route.cities_order:
            cities.append(city_order.city.city)
        start=0
        end=0
        for i in range(len(cities)):
            if cities[i] == source:
                start=i
            if cities[i] == destination:
                end = i
        for i in range(start,end):
            if (Distance.objects.filter(from_city=cities[i], to_city=cities[i+1]).exists()):
                dis = dis + Distance.objects.get(from_city=cities[i],to_city=cities[i+1]).distance
            elif (Distance.objects.filter(from_city=cities[i+1], to_city=cities[i]).exists()):
                dis = dis + Distance.objects.get(from_city=cities[i+1],to_city=cities[i]).distance  
        bus_list = Bus_Detail.objects.filter(route=route)
        
        for bus in bus_list:
            print("hi")
            fare_ = dis*bus.bus_type.fare
            fares.append(fare_)
            busList.append(bus)
    
    busId = zip(busList,fares)
    return render(request,'choose_bus.html',{'buses':busList,'busId':busId})



def city(request):
    if request.method =='POST':   
       city = request.POST.get('city')
       ct = City_Detail(city=city)
       ct.save()
    return render(request,'city.html') 


    
def route(request):
    if request.method == 'POST':
        source_name = request.POST.get('source')
        destination_name = request.POST.get('destination')

       
        source = City_Detail.objects.get(city=source_name)
        destination = City_Detail.objects.get(city=destination_name)

        route_instance = Route_Detail(source=source, destination=destination)
        route_instance.save()

        
        cities_names = [city.city for city in City_Detail.objects.all()]

        cities = []
        for city_name in cities_names:
            order_key = f'orders_{city_name}'
            time_key = f'times_{city_name}'

            order = request.POST.get(order_key)
            time_str = request.POST.get(time_key)

            if order and time_str:
                city = City_Detail.objects.get(city=city_name)
                time = datetime.strptime(time_str, '%H:%M').time()
                CitiesOrder.objects.create(route=route_instance, city=city, order=order, time=time)
        route_instance.cities_order = CitiesOrder.objects.filter(route=route_instance).order_by('order')
        for city_order in route_instance.cities_order:
            cities.append(city_order.city)
            
        for i in range(0,len(cities)-1):
            from_city = cities[i]
            to_city = cities[i+1]
            if not (Distance.objects.filter(from_city=from_city, to_city=to_city).exists() or Distance.objects.filter(from_city=to_city, to_city=from_city).exists()):
                getDistance(from_city,to_city)
            
        
    return render(request, 'route.html', {'cities': City_Detail.objects.all()})

def getDistance(source,destination):
        geocoder = Nominatim(user_agent="KavanG")

        city1 = source
        city2 = destination

        lat1 = geocoder.geocode(city1).latitude
        long1 = geocoder.geocode(city1).longitude

        lat2 = geocoder.geocode(city2).latitude
        long2 = geocoder.geocode(city2).longitude

        place1 = (lat1,long1)
        place2 = (lat2,long2)

        dis=distance.distance(place1,place2).km     
        Distance.objects.create(from_city = source,to_city = destination,distance = dis)

def build_bus(request):
    if request.method=='POST':
        route = request.POST.get('route')
        bus_type = request.POST.get('bus_type')
        b_type = Bus_Type.objects.get(bus_type=bus_type)
        cities = route.split('-')
        cities = [city.strip() for city in cities]
        source = cities[0]
        destination = cities[1]
        r = Route_Detail.objects.get(source=source,destination=destination)
        
        seats = int(request.POST.get('seats'))
        
        name = cities[0]+'-'+cities[len(cities)-1]
        bus = Bus_Detail(bus_name=name,route=r,bus_type=b_type,seats=seats)
        bus.save()
    return render(request,'build_bus.html',{'routes':Route_Detail.objects.all(),'bus_types':Bus_Type.objects.all()})
    


