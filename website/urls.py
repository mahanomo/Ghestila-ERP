from django.urls import path,include
from . import views

app_name= 'website'

urlpatterns = [
    path('',views.IndexView,name='index'),
    path('logs/',views.work_log_list,name='log-list'),
    path('calender/',views.CalenderView,name='calender'),
    path('leave-request/',views.LeaveRequestView,name='leave_request'),
    path('list-request/',views.ListRequestView,name='list_request'),
    path('single-view-request/<int:pid>',views.SingleRequestView,name='single_view_request'),
    path('single-view-request/<int:pid>',views.SingleRequestView,name='single_view_request'),
    # for managers
    # path('check-requests/',views.LeaveRequestViewSet.as_view({'get': 'retrieve'}),name='check_requests'),
    path('logs/manager',views.logs_manager_list,name='logs_manager'),
    path('check-requests/',views.LeaveRequestViewSet,name='check_requests'),
    path('check-requests-manager/<int:pid>',views.LeaveRequestcheck,name='check_requests_manager'),
    path('calendar/create/', views.create_plan, name='create_plan'),
    path('calendar/edit/<int:pk>/', views.update_plan, name='update_calender'),
    path('calendar/delete/<int:pk>/', views.delete_plan, name='delete_calender'),
    # for saeid
    path('api/', include('website.api.v1.urls')),
]