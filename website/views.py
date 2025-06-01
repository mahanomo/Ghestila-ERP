from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib import messages
from django.utils import timezone

from accounts.models import User
from .models import LeaveRequest,StatusDiscoverImage,PlanTable,WorkLog
from .forms import LeaveRequestForm,PlanTableForm
from .utils import STATUS_VISIBILITY

# Create your views here.
@login_required
def IndexView(request):
    # for departman it is required to Work report
    if request.user.role != 'department_manager' and request.user.role != 'manager':
        user = request.user
        today = timezone.localdate()

        log, created = WorkLog.objects.get_or_create(user=user, date=today)

        if request.method == 'POST':
            action = request.POST.get('action')

            if action == 'start':
                if not log.start_time:
                    log.start_time = timezone.now()
                    log.save()
            
            elif action == 'submit_report':
                report = request.POST.get('report', '').strip()
                dept_code = user.department.department.lower() if user.department else ''

                if dept_code != 'it':
                    
                    if report == '':
                        report = ' '
                    log.report = report
                    log.save()
                else:
                    if report == '':
                        messages.error(request, 'گزارش کار برای بخش IT الزامی است.')
                    else:
                        log.report = report
                        log.save()

            elif action == 'end':
                if log.report:
                    log.end_time = timezone.now()
                    log.save()
                else:
                    messages.error(request, 'لطفا قبل از پایان، گزارش کار وارد کنید.')

        context = {
            'log': log,
            'has_started': log.start_time is not None,
            'has_ended': log.end_time is not None,
            'report_submitted': bool(log.report),
            'user_role': user.role,
            'department': user.department
        }

        return render(request, 'website/index.html', context)
    else:
        return redirect('/calender/')

@login_required
def work_log_list(request):
    logs = WorkLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'website/work_log_list.html', {'logs': logs,'user_role':request.user.role})

@login_required
def logs_manager_list(request):
    if request.user.role == 'department_manager':
        logs = WorkLog.objects.filter(user__department=request.user.department).order_by('-date')
        return render(request, 'website/work_log_for_manager_list.html', {'logs': logs, 'user_role':request.user.role})
    
    if request.user.role == 'manager':
        logs = WorkLog.objects.all().order_by('-date')
        return render(request, 'website/work_log_for_manager_list.html', {'logs': logs,'user_role':request.user.role})

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
def create_plan(request):
    if request.user.role not in ['manager', 'department_manager']:
        return HttpResponse("شما مجاز به ثبت رویداد نیستید.")

    if request.method == 'POST':
        form = PlanTableForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.department = request.user.department
            plan.save()
            return redirect('website:calender')
    else:
        form = PlanTableForm()
    
    return render(request, 'website/create_calender.html', {'form': form})

@login_required
def update_plan(request, pk):
    if request.user.role not in ['manager', 'department_manager']:
        return HttpResponse("شما اجازه‌ی ویرایش این رویداد را ندارید.")
    
    plan = get_object_or_404(PlanTable, pk=pk)
    if plan.department != request.user.department:
        return HttpResponse("شما اجازه‌ی ویرایش این رویداد را ندارید.")

    if request.method == 'POST':
        form = PlanTableForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('website:calender')
    else:
        form = PlanTableForm(instance=plan)
    return render(request, 'website/update_calender.html', {'form': form})

@login_required
def delete_plan(request, pk):
    if request.user.role not in ['manager', 'department_manager']:
        return HttpResponse("شما اجازه‌ی ویرایش این رویداد را ندارید.")
    
    plan = get_object_or_404(PlanTable, pk=pk)
    if plan.department != request.user.department:
        return HttpResponse("شما اجازه‌ی حذف این رویداد را ندارید.")
    
    if request.method == 'POST':
        plan.delete()
        return redirect('website:calender')
    return render(request, 'website/delete_calender.html', {'plan': plan})


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
            if user_role == 'supervisor':
                leave.status = "pending_2"
            elif user_role == 'department_manager':
                leave.status = "pending_3"
            elif user_role == 'human_resources':
                leave.status = "pending_4"
            elif user_role == "employee":
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
    leave_requests = LeaveRequest.objects.filter(user=user).order_by('-created_at')
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


@login_required
def LeaveRequestViewSet(request):
    if request.user.role == "employee":
        return HttpResponse("!شما تحت عنوان کارمند نمی توانید به این صفحه دسترسی داشته باشید")
    
    visible_requests = LeaveRequest.objects.none()
    for status, roles in STATUS_VISIBILITY.items():
        if request.user.role in roles:
            requests_for_status = LeaveRequest.objects.filter(
                # status=status,
                user__department= request.user.department
            )
            visible_requests = visible_requests | requests_for_status
    
    if request.user.role =='human_resources' :
        requests_for_status = LeaveRequest.objects.filter(
                status='pending_3')
        requests_for_status2 = LeaveRequest.objects.filter(
                status='pending_4')
        requests_for_status3 = LeaveRequest.objects.filter(
                status='approved_4')
        visible_requests = visible_requests | requests_for_status | requests_for_status2 | requests_for_status3
    
    elif request.user.role =='manager' :
        visible_requests = LeaveRequest.objects.filter(
                status='pending_4')
        requests_for_status = LeaveRequest.objects.filter(
                status='approved_4')
        
        visible_requests = visible_requests | requests_for_status

    context = {
        'requests': visible_requests.distinct(),
        'user_role': request.user.role
    }
    return render(request, 'website/check_requests.html', context)

@login_required
def LeaveRequestcheck(request,pid):
    user_role = request.user.role
    detail_request = LeaveRequest.objects.get(id=pid)
    show_status = StatusDiscoverImage.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        if user_role == 'supervisor':
            if action == 'approve':
                detail_request.status = 'pending_2'
                messages.success(request, "درخواست تایید شد.")
            elif action == 'reject':
                detail_request.status = 'rejected_1'
                messages.error(request, "درخواست رد شد.")
        
        elif user_role == 'department_manager':
            if action == 'approve':
                detail_request.status = 'pending_3'
                messages.success(request, "درخواست تایید شد.")
            elif action == 'reject':
                detail_request.status = 'rejected_2'
                messages.error(request, "درخواست رد شد.")
        
        elif user_role == 'human_resources':
            if action == 'approve':
                detail_request.status = 'pending_4'
                messages.success(request, "درخواست تایید شد.")
            elif action == 'reject':
                detail_request.status = 'rejected_3'
                messages.error(request, "درخواست رد شد.")

        elif user_role == 'manager':
            if action == 'approve':
                detail_request.status = 'approved_4'
                messages.success(request, "درخواست تایید شد.")
            elif action == 'reject':
                detail_request.status = 'rejected_4'
                messages.error(request, "درخواست رد شد.")
        
        detail_request.save()
        # return redirect('website:check_requests_manager', pid=pid)

    context={'detail':detail_request, 'show_status': show_status, 'user_role':user_role}
    return render(request,'website/check-requests-manager.html',context)
