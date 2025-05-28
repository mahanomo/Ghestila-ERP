from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from accounts.models import User
from .models import LeaveRequest
from .forms import LeaveRequestForm

# Create your views here.
# @login_required
def IndexView(request):
    user_role = request.user.role
    context = {'is_employee':None}
    if user_role != 'employee':
        context['is_employee'] = 'NotNone'
    return render(request,'website/index.html',context)

@login_required
def CalenderView(request):
    user = request.user.profile
    department = user.department
    calendar_entries = department.calendar_entries.all() if department else []
    context = {'calender':calendar_entries}
    return render(request,'website/calender.html',context)

def LeaveRequestView(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.status = 'pending_1'
            leave.save()
            return redirect('leave-request')

    else:
        form = LeaveRequestForm
    return render(request,'website/leave_request.html',{'form':form})