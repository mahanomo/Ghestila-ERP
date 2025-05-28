from django.urls import path,include
from . import views

app_name= 'website'

urlpatterns = [
    path('',views.IndexView,name='index'),
    path('calender/',views.CalenderView,name='calender'),
    path('leave-request/',views.LeaveRequestView,name='leave_request'),
]
