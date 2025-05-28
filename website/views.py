from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse
from accounts.models import User
from .models import LeaveRequest,StatusDiscoverImage
from .forms import LeaveRequestForm

# Create your views here.
@login_required
def IndexView(request):
    # for show related base.html show
    user_role = request.user.role
    context = {'user_role':user_role}
    return render(request,'website/index.html',context)

@login_required
def CalenderView(request):
    # for show related base.html show
    user_role = request.user.role
    context = {'user_role':user_role}
    # coding
    department = request.user.department
    calendar_entries = department.calendar_entries.all() if department else []
    context['calender'] = calendar_entries
    return render(request,'website/calender.html',context)
@login_required
def LeaveRequestView(request):
    # for show related base.html show
    user_role = request.user.role
    context = {'user_role':user_role}
    # coding
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.status = 'pending_1'
            leave.save()
            return redirect('/list-request/')

    else:
        form = LeaveRequestForm
    context['form'] = form
    return render(request,'website/leave_request.html',context)
@login_required
def ListRequestView(request):
    # for show related base.html show
    user_role = request.user.role
    context = {'user_role':user_role}
    # coding
    user = request.user
    leave_requests = LeaveRequest.objects.filter(user=user)
    context['requests'] = leave_requests
    return render(request,'website/list_leave_request.html',context)

@login_required
# for see detail of request
def SingleRequestView(request,pid):
    # for show related base.html show
    user_role = request.user.role
    context = {'user_role':user_role}
    # coding
    user = request.user
    detail_request = LeaveRequest.objects.get(user=user,id=pid)
    show_status = StatusDiscoverImage.objects.all()
    context['detail'] = detail_request
    context['show_status'] = show_status
    return render(request,'website/detail_request.html',context)

# for response to leave requests
@login_required
def check_requests(request):
    # for show related base.html show
    user_role = request.user.role
    # define departman
    user_department = request.user.department
    context = {'user_role':user_role,'user_departman':user_department}
    requests = LeaveRequest.objects.filter(user=)
    # if user_role == 'supervisor' and requests.status == 'pending_1':
    #     print('this for super visor')
    # else:
    #     print('ok')
    
    return HttpResponse(f'{requests}')


    # بررسی url های مدیران برای کارمندان عادی باز می شود یا نه