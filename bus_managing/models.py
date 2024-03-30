from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('passenger', 'Passenger'),
        ('government_agent', 'Government Agent'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES , default='Passenger')
    phone = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return self.username
    
class Advance_booking(models.Model):
    PNR = models.CharField(max_length=122, blank=False, null=False)
    username = models.CharField(max_length=122, blank=False, null=False)
    name = models.CharField(max_length=122, blank=False, null=False)
    seats = models.PositiveIntegerField(max_length=40, blank=False, null=False)
    bus_name = bus_name = models.CharField(max_length=122,blank=False, null=False)
    total_fare = models.FloatField(max_length=15,blank = False,null=False)
    txn_password = models.CharField(max_length=122, blank=False, null=False)
    
class City_Detail(models.Model):
    city = models.CharField(max_length=122, primary_key=True)
    def __str__(self):
        return self.city
    

class Route_Detail(models.Model):
    route_id = models.AutoField(primary_key=True)
    source = models.ForeignKey(City_Detail,related_name='source_city',on_delete=models.CASCADE)
    destination = models.ForeignKey(City_Detail,related_name='destination_city',on_delete=models.CASCADE)
    cities = models.ManyToManyField(City_Detail,through='CitiesOrder',related_name='route_cities',limit_choices_to={'city__in':['Junagadh','Rajkot','Nadiad','Ahmedabad']})
    
    def __str__(self):
        return f"{self.source} - {self.destination}"

class CitiesOrder(models.Model):
    route = models.ForeignKey(Route_Detail, on_delete=models.CASCADE)
    city = models.ForeignKey(City_Detail, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(null=True,blank=True)
    time = models.TimeField(default=timezone.now().strftime('%H:%M'))
    class Meta:
        ordering = ['order']
    def __str__(self):
        return f"{self.route.source} - {self.route.destination}"
     
        
class Distance(models.Model):
    dis_id = models.AutoField(primary_key=True)
    from_city = models.ForeignKey(City_Detail, related_name='distance_from', on_delete=models.CASCADE)
    to_city = models.ForeignKey(City_Detail, related_name='distance_to', on_delete=models.CASCADE)
    distance = models.FloatField()
    def __str__(self):
        return f"{self.from_city} - {self.to_city}"

class Bus_Type(models.Model):
    bus_type = models.CharField(max_length=122,primary_key=True)
    fare = models.FloatField(null = False)
    def __str__(self):
        return self.bus_type
    
class Bus_Detail(models.Model):
    bus_name = models.CharField(max_length=122, primary_key=True)
    route_id = models.ForeignKey(Route_Detail,blank=True, null=True,on_delete=models.CASCADE)
    bus_type = models.ForeignKey(Bus_Type,max_length=122, blank=True, null=True,on_delete=models.CASCADE)
    seats = models.IntegerField(max_length=50)
    cost = models.FloatField(null = False)
    def __str__(self):
        return f"{self.bus_name}"
    
    
    

    
    

    
    
    



    