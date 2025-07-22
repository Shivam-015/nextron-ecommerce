from django.urls import path
from . import views
urlpatterns = [
    
    path('login/' , views.login , name="login"),
    path('register/',views.register ,name="register"),
    path('send_otp/', views.send_otp,name='send_otp'),
    path('logout/',views.logout, name="logout"),
    path('register/',views.register,name="register"),
    path('billing/',views.billing,name="billing"),
    path('payment_success/', views.payment_success, name="payment_success"),
    path('payment_cancel/', views.payment_cancel, name="payment_cancel"),
]