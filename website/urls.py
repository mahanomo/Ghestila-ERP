from django.urls import path,include
from . import views

app_name= 'website'

urlpatterns = [
    path('',views.IndexView,name='index'),
    path('calender/',views.CalenderView,name='calender'),
    path('leave-request/',views.LeaveRequestView,name='leave_request'),
    path('list-request/',views.ListRequestView,name='list_request'),
    path('single-view-request/<int:pid>',views.SingleRequestView,name='single_view_request'),
    path('single-view-request/<int:pid>',views.SingleRequestView,name='single_view_request'),
    # for managers
    path('check-requests/',views.check_requests,name='check_requests'),
]
