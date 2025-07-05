from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import string,random
from BMS.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from .models import CustomUser,City_Detail,Route_Detail,CitiesOrder,Distance,Bus_Detail,Bus_Type,Bus_Seats,Advance_booking
from django.contrib import messages
from datetime import datetime,date
from geopy.geocoders import Nominatim
from geopy import distance
from django.db.models import Q
import razorpay
from django.views.decorators.csrf import csrf_exempt
import ast
from twilio.rest import Client

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

@login_required
def logout_view(request):
    logout(request)
    messages.success(request,"logged OUT")
    return redirect('homepage')

@login_required
def passenger(request):
    return render(request,'passenger.html')

@login_required
def govt_agent(request):
    return render(request,'govt_agent.html')

@login_required
def select_route(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        request.session['date'] = date
        request.session['source'] = source
        request.session['destination'] = destination
        return redirect('choose_bus')
    
    return render(request,'select_route.html',{'cities': City_Detail.objects.all()})

@login_required
def choose_bus(request):
    
    bus_data = []
    busList = []
    cities = []
    fares = []
    times = []
    dis = 0
    date = request.session.get('date')
    
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
        dis = 0
        
        cities = []
        route.cities_order = CitiesOrder.objects.filter(route=route).order_by('order')
        for city_order in route.cities_order:
            cities.append(city_order.city.city)
            times.append(city_order.time)
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
        bus_list = Bus_Detail.objects.filter(route=route,date=date)
        
       
        for bus in bus_list:
            fare = dis * bus.bus_type.fare
            fares.append(fare)
            city_time = zip(cities,times)
            bus_data.append({
                'bus': bus,
                'fare': fare,
                'city_time':city_time
            })
    if request.method == 'POST':
        bus_id = request.POST.get('bus')
        for bus_d in bus_data:
            if bus_d['bus'].bus_name == bus_id:
                request.session['bus'] = bus_id
                request.session['fare'] = bus_d['fare']
                cities,times = zip(*bus_d['city_time'])
                times_str = [str(time) for time in times]
                request.session['cities'] = cities
                request.session['times'] = times_str
        return redirect('choose_seat')      
         
    return render(request,'choose_bus.html',{'bus_data': bus_data})

@login_required
def choose_seat(request):
    
    bus_data = []
    source = request.session.get('source')
    destination = request.session.get('destination')
    bus=request.session.get('bus')
    bus_obj = Bus_Detail.objects.get(bus_name=bus)
    
    fare = float(request.session.get('fare'))
    times = request.session.get('times')
    cities = request.session.get('cities')
    date = request.session.get('date')
    city_time = zip(cities,times)
    arr_dep = []
    bus_data.append({
                'bus': bus_obj,
                'fare': fare,
                'city_time':city_time
            })
   
    
    seats_per_row = 15  # 15 seats in one row
    total_seats = bus_obj.seats
    print(total_seats)
    # Calculate the number of rows for each set with a gap in between
    num_rows_first_set = (total_seats // seats_per_row) // 2
    num_rows_second_set = total_seats // seats_per_row - num_rows_first_set
    
    seat_arrangement = []
    
    # First set of rows
    for row in range(num_rows_first_set):
        row_seats = [{'number': f'{row+1}{chr(65+i)}', 'available': True} for i in range(seats_per_row)]
        if not Bus_Seats.objects.filter(bus_name=bus_obj,date=date,seat_no__in=[seat['number'] for seat in row_seats]).exists():   
           bus_seats = [Bus_Seats(bus_name=bus_obj,date=date,seat_no=seat['number'], available=seat['available']) for seat in row_seats]
           Bus_Seats.objects.bulk_create(bus_seats)
        seat_arrangement.append(row_seats)
    
    # Add gap
    seat_arrangement.append([])
    
    # Second set of rows
    for row in range(num_rows_first_set, num_rows_first_set + num_rows_second_set):
        row_seats = [{'number': f'{row+1}{chr(65+i)}', 'available': True} for i in range(seats_per_row)]
        if not Bus_Seats.objects.filter(bus_name=bus_obj,date=date,seat_no__in=[seat['number'] for seat in row_seats]).exists():   
           bus_seats = [Bus_Seats(bus_name=bus_obj,date=date,seat_no=seat['number'], available=seat['available']) for seat in row_seats]
           Bus_Seats.objects.bulk_create(bus_seats)
        seat_arrangement.append(row_seats)
    selected_seats=[]
    unavailable_seats = Bus_Seats.objects.filter(bus_name=bus_obj,date=date,available=False).values_list('seat_no', flat=True)
    bus_obj.available_seats = bus_obj.seats - len(unavailable_seats)
    bus_obj.save()
    if request.method == 'POST':
        for city,time in city_time:
            if city ==source:
                arr_dep.append(time)
            if city == destination:
                arr_dep.append(time)
        selected_seats = request.POST.get('selected_seats', '').split(',')  # Retrieve selected seats from POST data
        
        name = request.POST.get('name')
        age = request.POST.get('age')
        print("Selected Seats:", selected_seats)  # Print selected seats in console
        seats = len(selected_seats)
        print("Seats:",seats)
        print("fare:",fare)
        total_fare = int(fare*seats)
        characters = string.ascii_letters + string.digits
        
        txn = ''.join(random.choice(characters) for _ in range(5))
        chars = string.digits
        pnr = 'G1-'+''.join(random.choice(chars) for _ in range(8))
        adv_book = Advance_booking(PNR=pnr,bus_info=f'{source}-{destination}',doj=date,username=request.user.username,phone=request.user.phone,name=name,seat_nos=selected_seats,seats=seats,bus_name=bus,total_fare=total_fare,arrival_time=arr_dep[0],departure_time=arr_dep[1],txn_password=txn)
        
        adv_book.save()
        request.session['pnr'] = adv_book.PNR
        for seat_number in selected_seats:
           bus_seat = Bus_Seats.objects.get(bus_name=bus_obj,date=date,seat_no=seat_number)
           bus_seat.available = False
           bus_seat.save()
        
        request.session['total_fare']=total_fare
        return redirect('payment')
    return render(request,'bus_view.html',{'bus_data':bus_data,'seat_arrangement':seat_arrangement,'unavailable_seats':list(unavailable_seats)})
    
@login_required
def city(request):
    # Add role check for admin/government_agent only
    if request.user.role not in ['admin', 'government_agent']:
        messages.error(request, f"Access denied. Your role '{request.user.role}' doesn't have permission to add cities.")
        return redirect('passenger')
        
    if request.method =='POST':   
       city = request.POST.get('city')
       ct = City_Detail(city=city)
       ct.save()
       messages.success(request, f"City '{city}' added successfully!")
    return render(request,'city.html') 

@login_required   
def route(request):
    # Add role check for admin/government_agent only
    if request.user.role not in ['admin', 'government_agent']:
        messages.error(request, f"Access denied. Your role '{request.user.role}' doesn't have permission to add routes.")
        return redirect('passenger')
        
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
        
        messages.success(request, "Route added successfully!")
        
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

@login_required
def build_bus(request):
    # Add role check for admin/government_agent only
    if request.user.role not in ['admin', 'government_agent']:
        messages.error(request, f"Access denied. Your role '{request.user.role}' doesn't have permission to add buses.")
        return redirect('passenger')
        
    if request.method=='POST':
        route = request.POST.get('route')
        name = request.POST.get('bus_name')
        bus_type = request.POST.get('bus_type')
        date = request.POST.get('date')
        b_type = Bus_Type.objects.get(bus_type=bus_type)
        cities = route.split('-')
        cities = [city.strip() for city in cities]
        source = cities[0]
        destination = cities[1]
        r = Route_Detail.objects.get(source=source,destination=destination)
        
        seats = int(request.POST.get('seats'))
        
        bus = Bus_Detail(bus_name=name,date=date,route=r,bus_type=b_type,seats=seats)
        bus.save()
        messages.success(request, f"Bus '{name}' added successfully!")
    return render(request,'build_bus.html',{'routes':Route_Detail.objects.all(),'bus_types':Bus_Type.objects.all()})
    
@login_required
def payment(request):
    pnr=request.session.get('pnr')
    
    # Security check: Ensure the booking belongs to the current user
    try:
        bus = Advance_booking.objects.get(PNR=pnr, username=request.user.username)
    except Advance_booking.DoesNotExist:
        messages.error(request, "Invalid booking or access denied.")
        return redirect('passenger')
    
    amount = request.session.get('total_fare')*100
    order_currency = 'INR'
    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
    payment = client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
    context = {'payment':payment,'amount':amount,'bus':bus}
    return render(request,'payment.html',context)

@csrf_exempt
@login_required
def success(request):
    # Get PNR from session instead of hardcoded value
    pnr = request.session.get('pnr')
    if not pnr:
        messages.error(request, "No booking found.")
        return redirect('passenger')
    
    # Security check: Ensure the booking belongs to the current user
    try:
        bus = Advance_booking.objects.get(PNR=pnr, username=request.user.username)
    except Advance_booking.DoesNotExist:
        messages.error(request, "Invalid booking or access denied.")
        return redirect('passenger')
    
    # Use the user's phone number from the booking
    msg = "Route: "+bus.bus_info+'\n'+"Bus_Name: "+bus.bus_name+'\n'+"Fare: "+str(bus.total_fare)+'\n'+"DOJ: "+bus.doj+'\n'+"Seats: "+str(bus.seat_nos)+'\n'+"Txnpass: "+bus.txn_password
    
    try:
        account_sid = 'AC533cf4edf8c7b91b7f41992f452f9c8a'
        auth_token = '235409a828c61edb487a494f6c38300a'
        
        twilio_number = '+12512548928'
        # Use the user's phone number from the booking
        user_number = bus.phone
        client = Client(account_sid,auth_token)
        message = client.messages.create(
            body=msg,
            from_=twilio_number,
            to=user_number
        )
        print(message)
    except Exception as e:
        print(f"SMS sending failed: {e}")
        # Don't fail the success page if SMS fails
    
    # Clear session data after successful payment
    request.session.pop('pnr', None)
    request.session.pop('total_fare', None)
    request.session.pop('bus', None)
    request.session.pop('fare', None)
    request.session.pop('cities', None)
    request.session.pop('times', None)
    request.session.pop('date', None)
    request.session.pop('source', None)
    request.session.pop('destination', None)
    
    return render(request, 'success.html', {'bus': bus})

@login_required
def cancel(request):
    # Only show tickets belonging to the current user
    tickets = Advance_booking.objects.filter(username=request.user.username)
    
    if request.method == 'POST':
        PNR = request.POST.get('selected_ticket')
        
        # Security check: Ensure the ticket belongs to the current user
        try:
            ticket = Advance_booking.objects.get(PNR=PNR, username=request.user.username)
            request.session['PNR'] = PNR    
            return redirect('cancel_seats')
        except Advance_booking.DoesNotExist:
            messages.error(request, "Invalid ticket or access denied.")
            return redirect('cancel')
    
    return render(request,'cancel_ticket.html',{'tickets':tickets})
 
@login_required
def cancel_seats(request):
    PNR = request.session.get('PNR')
    if not PNR:
        messages.error(request, "No ticket selected for cancellation.")
        return redirect('cancel')
    
    # Security check: Ensure the ticket belongs to the current user
    try:
        ticket = Advance_booking.objects.get(PNR=PNR, username=request.user.username)
    except Advance_booking.DoesNotExist:
        messages.error(request, "Invalid ticket or access denied.")
        return redirect('cancel')
    
    bus_obj = Bus_Detail.objects.get(bus_name=ticket.bus_name)
    seats = ticket.seat_nos
    ticket_list = ast.literal_eval(seats) if isinstance(seats, str) else seats
    
    if request.method == 'POST':
        selected_seats = request.POST.getlist('selected_seats')
        txn_pass = request.POST.get('txn')
        
        if not selected_seats:
            messages.error(request, "Please select at least one seat to cancel.")
            return render(request,'cancel_seats.html',{'seats':ticket_list,'ticket':ticket})
        
        if txn_pass == ticket.txn_password:
            # Calculate refund amount
            fare_per_seat = ticket.total_fare / ticket.seats
            refund_amount = len(selected_seats) * fare_per_seat
            
            # Update seat availability
            for seat in selected_seats:
                bus_seat = Bus_Seats.objects.get(bus_name=bus_obj,date=ticket.doj,seat_no=seat)
                bus_seat.available = True
                bus_seat.save()
                
                # Remove seat from ticket
                if seat in ticket_list:
                    ticket_list.remove(seat)
            
            # Update ticket or delete if no seats left
            if len(ticket_list) == 0:
                ticket.delete()
                messages.success(request, f"All seats cancelled successfully! Refund amount: ₹{refund_amount:.2f}")
                # Clear session
                request.session.pop('PNR', None)
                return redirect('cancel')
            else:
                # Update ticket with remaining seats
                ticket.seat_nos = ticket_list
                ticket.seats = len(ticket_list)
                ticket.total_fare = ticket.total_fare - refund_amount
                ticket.save()
                messages.success(request, f"Selected seats cancelled successfully! Refund amount: ₹{refund_amount:.2f}")
                
        else:
            messages.error(request, "Incorrect transaction password. Please try again.")
            
    return render(request,'cancel_seats.html',{'seats':ticket_list,'ticket':ticket})