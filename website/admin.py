from django.contrib import admin
from .models import PlanTable,LeaveRequest

# Register your models here.
admin.site.register(PlanTable)
admin.site.register(LeaveRequest)