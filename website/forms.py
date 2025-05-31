from django.forms import ModelForm
from jalali_date.widgets import AdminJalaliDateWidget
import django_jalali.forms as jforms

from .models import LeaveRequest,PlanTable

class LeaveRequestForm(ModelForm):
    start_day = jforms.jDateField(label='تاریخ شروع')
    end_day = jforms.jDateField(label='تاریخ پایان')
    class Meta:
        model = LeaveRequest
        fields = ['start_day','end_day','description']
        widgets = {
            'start_day': AdminJalaliDateWidget,
            'end_day': AdminJalaliDateWidget,
        }

class PlanTableForm(ModelForm):
    class Meta:
        model = PlanTable
        fields = ['day', 'description']