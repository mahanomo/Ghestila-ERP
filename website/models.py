from django.db import models
from accounts.models import Department,User
# Create your models here.
class PlanTable(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="calendar_entries")
    day = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.day
    
class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending_1', 'منتظر تایید سرپرست'),
        ('approved_1', 'تایید توسط سرپرست'),
        ('rejected_1', 'رد توسط سرپرست'),
        ('pending_2', 'منتظر تایید مدیر بخش'),
        ('approved_2', 'تایید توسط مدیر بخش'),
        ('rejected_2', 'رد توسط مدیر بخش'),
        ('pending_3', 'منتظر تایید مدیر منابع انسانی'),
        ('approved_3', 'تایید توسط مدیر منابع انسانی'),
        ('rejected_3', 'رد توسط مدیر منابع انسانی'),
        ('approved_4', 'تایید نهایی'),
        ('rejected_4', 'رد نهایی'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_requester')
    start_day = models.DateField()
    end_day = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_1')
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'درخواست مرخصی {self.user.full_name} از تاریخ {self.start_day} تا {self.end_day}'
    
class StatusDiscoverImage(models.Model):
    status = models.CharField(max_length=30)
    image = models.ImageField()

    def __str__(self):
        return self.status
