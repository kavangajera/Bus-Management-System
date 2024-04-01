from django.urls import path
from bus_managing import views
urlpatterns = [
    path('',views.home,name="homepage" ),
    path('signup/', views.signup, name='signup'),
    path('login_view/',views.login_view,name="login_view"),
    path('logout/',views.logout_view,name="logout_view"),
    path('passenger/',views.passenger,name="passenger"),
    path('govt_agent/',views.govt_agent,name="govt_agent"),
    path('select_route/',views.select_route,name="select_route"),
    path('city/',views.city,name="city"),
    path('choose_bus/',views.choose_bus,name='choose_bus'),
    path('route/',views.route,name="route"),
    path('build_bus/',views.build_bus,name="build_bus"),
    path('choose_seat/',views.choose_seat,name='choose_seat'),
    path('payment/',views.payment,name="payment"),
     path('success/' , views.success , name='success')
    # Add other URLs as needed
]
