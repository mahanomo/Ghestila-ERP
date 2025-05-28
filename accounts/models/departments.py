from django.db import models
from .users import User

class Department(models.Model):
    DEPARTMENT_CHOICES = (
        ('unknown', 'تعریف نشده'),
        ('admin', 'مدیر سیستم'),
        ('manager', 'مدیریت'),
        ('site', 'سایت'),
        ('it', 'آی تی'),
        ('human_resources', 'منابع انسانی'),
        ('finance', 'مالی'),
        ('support', 'پشتیبانی'),
        ('sales', 'فروش'),
        ('adminstrative', 'اداری'),
        ('formal', 'حضوری'),
        ('content', 'محتوا'),
    )
    name = models.CharField(max_length=35, choices=DEPARTMENT_CHOICES)
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, related_name="supervisor_departments")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, related_name="managed_departments")

    def __str__(self):
        return self.name