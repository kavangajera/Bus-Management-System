from django.contrib import admin
from .models import CustomUser,City_Detail,Route_Detail,Distance,CitiesOrder,Bus_Detail,Bus_Type,Advance_booking,Bus_Seats

admin.site.register(CustomUser)
admin.site.register(City_Detail)
admin.site.register(Route_Detail)
admin.site.register(Distance)
admin.site.register(CitiesOrder)
admin.site.register(Bus_Detail)
admin.site.register(Bus_Type)
admin.site.register(Advance_booking)
admin.site.register(Bus_Seats)