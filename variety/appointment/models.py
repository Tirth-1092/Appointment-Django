
# from django.db import models
# from django.conf import settings
# from schedule.models import Calendar, Event
# from datetime import timedelta, time


# class Service(models.Model):
#     name = models.CharField(max_length=100)
#     duration = models.DurationField(help_text="Duration of service (e.g., 0:30:00 for 30 mins)")

#     def __str__(self):
#         return self.name


# class Staff(models.Model):
#     staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     services = models.ManyToManyField(Service)
#     calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.staff.username} - Staff"

#     @property
#     def is_employee(self):
#         return self.staff.is_employee

#     def is_available(self, start_time, total_duration):
#         """
#         Check if staff is available for the given time range and within business hours.
#         """
#         end_time = start_time + total_duration

#         # Enforce working hours (9 AM to 9 PM)
#         if not (time(9, 0) <= start_time.time() <= time(21, 0)):
#             return False
#         if not (time(9, 0) <= end_time.time() <= time(21, 0)):
#             return False

#         overlapping_events = Event.objects.filter(
#             calendar=self.calendar,
#             start__lt=end_time,
#             end__gt=start_time
#         )
#         return not overlapping_events.exists()


# class Appointment(models.Model):
#     client = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='appointments')
#     services = models.ManyToManyField(Service)
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     _end_time = models.DateTimeField(db_column='end_time')  # rename the DB field


#     def __str__(self):
#         return f"{self.client.username} - Appointment on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

#     @property
#     def is_customer(self):
#         return self.client.is_customer

#     @property 
#     def end_time(self):
#         return self.start_time + self.get_total_duration()

#     def get_total_duration(self):
#         return sum([service.duration for service in self.services.all()], timedelta())

#     def save(self, *args, **kwargs):
#         is_new = self._state.adding
#         super().save(*args, **kwargs)

#         if is_new:
#             total_duration = self.get_total_duration()
#             end_time = self.start_time + total_duration

#             Event.objects.create(
#                 title=f"{self.client.username}'s Appointment",
#                 start=self.start_time,
#                 end=end_time,
#                 calendar=self.staff.calendar
#             )


# from django.db import models
# # from django.contrib.auth.models import User
# from schedule.models import Calendar, Event
# from datetime import timedelta,datetime
# from django.conf import settings


# class Service(models.Model):
#     name = models.CharField(max_length=100)
#     duration = models.DurationField()

#     def __str__(self):
#         return self.name


# class Staff(models.Model):
#     staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     services = models.ManyToManyField(Service)
#     calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.staff.username


# class Appointment(models.Model):
#     client = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='appointments')
#     services = models.ManyToManyField(Service)
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     _end_time = models.DateTimeField(db_column='end_time', default=datetime.now)

#     def __str__(self):
#         return f"Appointment for {self.client.username} with {self.staff.staff.username} at {self.start_time}"

#     @property
#     def end_time(self):
#         return self.start_time + self.get_total_duration()

#     def get_total_duration(self):
#         return sum([service.duration for service in self.services.all()], timedelta())

#     def save(self, *args, **kwargs):
#         is_new = self._state.adding
#         self._end_time = self.start_time + self.get_total_duration()
#         super().save(*args, **kwargs)

#         if is_new:
#             Event.objects.create(
#                 title=f"{self.client.username}'s Appointment",
#                 start=self.start_time,
#                 end=self._end_time,
#                 calendar=self.staff.calendar
#             )

# from django.db import models
# from django.conf import settings
# from schedule.models import Calendar, Event
# from datetime import timedelta, time, datetime


# class Service(models.Model):
#     name = models.CharField(max_length=100)
#     duration = models.DurationField(help_text="Duration of service (e.g., 0:30:00 for 30 mins)")

#     def __str__(self):
#         return self.name


# class Staff(models.Model):
#     staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     services = models.ManyToManyField(Service)
#     calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.staff.username} - Staff"

#     def is_available(self, start_time, total_duration):
#         end_time = start_time + total_duration

#         if not (time(9, 0) <= start_time.time() <= time(21, 0)):
#             return False
#         if not (time(9, 0) <= end_time.time() <= time(21, 0)):
#             return False

#         overlapping_events = Event.objects.filter(
#             calendar=self.calendar,
#             start__lt=end_time,
#             end__gt=start_time
#         )
#         return not overlapping_events.exists()


# class Appointment(models.Model):
#     client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
#     services = models.ManyToManyField(Service)
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     _end_time = models.DateTimeField(db_column='end_time', default=datetime.now)

#     def __str__(self):
#         return f"{self.client.username} - Appointment on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

#     @property
#     def end_time(self):
#         return self.start_time + self.get_total_duration()

#     def get_total_duration(self):
#         return sum([service.duration for service in self.services.all()], timedelta())

#     def save(self, *args, **kwargs):
#         is_new = self._state.adding
#         self._end_time = self.start_time + self.get_total_duration()
#         super().save(*args, **kwargs)

#         if is_new:
#             Event.objects.create(
#                 title=f"{self.client.username}'s Appointment",
#                 start=self.start_time,
#                 end=self._end_time,
#                 calendar=self.staff.calendar
#             )

# from django.db import models
# from django.conf import settings
# from schedule.models import Calendar, Event
# from datetime import timedelta, datetime, time


# class Service(models.Model):
#     name = models.CharField(max_length=100)
#     duration = models.DurationField(help_text="Duration of service (e.g., 0:30:00 for 30 mins)")

#     def __str__(self):
#         return self.name


# class Staff(models.Model):
#     staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     services = models.ManyToManyField(Service)
#     calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.staff.username} - Staff"

#     def is_available(self, start_time, duration):
#         from django.utils.timezone import make_aware

#         end_time = start_time + duration
#         working_start = make_aware(datetime.combine(start_time.date(), time(9, 0)))
#         working_end = make_aware(datetime.combine(start_time.date(), time(21, 0)))

#         if not (working_start <= start_time < working_end and start_time < end_time <= working_end):
#             return False

#         overlapping = Event.objects.filter(
#             calendar=self.calendar,
#             start__lt=end_time,
#             end__gt=start_time
#         )
#         return not overlapping.exists()


# class Appointment(models.Model):
#     client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
#     services = models.ManyToManyField(Service)
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     _end_time = models.DateTimeField(db_column='end_time', default=datetime.now)

#     def __str__(self):
#         return f"{self.client.username} - Appointment on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

#     @property
#     def end_time(self):
#         return self.start_time + self.get_total_duration()

#     def get_total_duration(self):
#         return sum((service.duration for service in self.services.all()), timedelta())

#     def save(self, *args, **kwargs):
#         is_new = self._state.adding
#         self._end_time = self.start_time + self.get_total_duration()
#         super().save(*args, **kwargs)

#         if is_new:
#             Event.objects.create(
#                 title=f"{self.client.username}'s Appointment",
#                 start=self.start_time,
#                 end=self._end_time,
#                 calendar=self.staff.calendar
#             )


# from django.db import models
# from django.conf import settings
# from schedule.models import Calendar, Event
# from datetime import timedelta, datetime, time
# from django.utils.timezone import make_aware


# class Service(models.Model):
#     name = models.CharField(max_length=100)
#     duration = models.DurationField(help_text="e.g., 0:15:00 for 15 minutes")

#     def __str__(self):
#         return self.name


# class Staff(models.Model):
#     staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     services = models.ManyToManyField(Service)
#     calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.staff.username} - Staff"

#     def is_available(self, start_time, duration):
#         end_time = start_time + duration
#         working_start = make_aware(datetime.combine(start_time.date(), time(9, 0)))
#         working_end = make_aware(datetime.combine(start_time.date(), time(21, 0)))

#         if not (working_start <= start_time < working_end and end_time <= working_end):
#             return False

#         return not Event.objects.filter(
#             calendar=self.calendar,
#             start__lt=end_time,
#             end__gt=start_time
#         ).exclude(title__icontains="available slot").exists()


# class Appointment(models.Model):
#     client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     services = models.ManyToManyField(Service)
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     _end_time = models.DateTimeField(db_column='end_time', blank=True, null=True)

#     def __str__(self):
#         return f"{self.client.username} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

#     @property
#     def end_time(self):
#         return self.start_time + self.get_total_duration()

#     def get_total_duration(self):
#         return sum((s.duration for s in self.services.all()), timedelta())

#     def save(self, *args, **kwargs):
#         creating = self._state.adding
#         super().save(*args, **kwargs)

#         if creating and self.services.exists():
#             total_duration = self.get_total_duration()
#             self._end_time = self.start_time + total_duration
#             super().save(update_fields=['_end_time'])

#             Event.objects.create(
#                 title=f"{self.client.username}'s Appointment",
#                 start=self.start_time,
#                 end=self._end_time,
# #                 calendar=self.staff.calendar
# #             )

# from django.db import models
# from django.conf import settings
# from schedule.models import Calendar, Event
# from datetime import timedelta, datetime, time
# from django.utils.timezone import make_aware
# from django.utils.timezone import now

# class Service(models.Model):
#     name = models.CharField(max_length=100)
#     duration = models.DurationField(help_text="e.g., 0:15:00 for 15 minutes")
#     price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return self.name

# class Staff(models.Model):
#     staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     services = models.ManyToManyField(Service)
#     calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE,unique=False)
#     working_hours = models.JSONField(default=dict, blank=True, null=True)
#     buffer_time = models.DurationField(default=timedelta(minutes=15), help_text="Buffer time between appointments")
#     is_staff = models.BooleanField(default=True)
#     class Meta:
#         verbose_name_plural = "Staff"

#     def __str__(self):
#         return f"{self.staff.get_full_name()} - Staff"

#     def get_working_hours(self, date):
#         """Get working hours for a specific date, considering custom hours if set"""
#         default_hours = {'start': '09:00', 'end': '21:00'}
#         if not self.working_hours:
#             return default_hours
        
#         weekday = date.strftime('%A').lower()
#         return self.working_hours.get(weekday, default_hours)

#     def get_available_slots(self, date, duration):
#         """Returns available time slots for a given date and duration"""
#         slots = []
#         hours = self.get_working_hours(date)
        
#         try:
#             start_hour, start_minute = map(int, hours['start'].split(':'))
#             end_hour, end_minute = map(int, hours['end'].split(':'))
#         except:
#             start_hour, start_minute = 9, 0
#             end_hour, end_minute = 21, 0

#         working_start = make_aware(datetime.combine(date, time(start_hour, start_minute)))
#         working_end = make_aware(datetime.combine(date, time(end_hour, end_minute)))
        
#         current_time = working_start
#         while current_time + duration <= working_end:
#             if self.is_available(current_time, duration):
#                 slots.append(current_time)
#             current_time += timedelta(minutes=15)  # Minimum time slot increment
            
#         return slots

#     def is_available(self, start_time, duration):
#         """Check if staff is available for given time and duration"""
#         end_time = start_time + duration
#         date = start_time.date()
#         hours = self.get_working_hours(date)
        
#         try:
#             start_hour, start_minute = map(int, hours['start'].split(':'))
#             end_hour, end_minute = map(int, hours['end'].split(':'))
#         except:
#             start_hour, start_minute = 9, 0
#             end_hour, end_minute = 21, 0

#         working_start = make_aware(datetime.combine(date, time(start_hour, start_minute)))
#         working_end = make_aware(datetime.combine(date, time(end_hour, end_minute)))

#         # Check within working hours
#         if not (working_start <= start_time < working_end and end_time <= working_end):
#             return False

#         # Check for existing appointments with buffer time
#         buffer = self.buffer_time
#         return not Event.objects.filter(
#             calendar=self.calendar,
#             start__lt=end_time + buffer,
#             end__gt=start_time - buffer
#         ).exists()

# class Appointment(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('confirmed', 'Confirmed'),
#         ('cancelled', 'Cancelled'),
#         ('completed', 'Completed'),
#     ]

#     client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_appointments')
#     services = models.ManyToManyField(Service)
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_appointments')
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
#     notes = models.TextField(blank=True)
#     created_at = models.DateTimeField(default=now)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['start_time']

#     def __str__(self):
#         return f"{self.client.get_full_name()} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

#     @property
#     def duration(self):
#         return self.get_total_duration()

#     def get_total_duration(self):
#         return sum((s.duration for s in self.services.all()), timedelta())

#     def save(self, *args, **kwargs):
#         creating = self._state.adding
#         if creating or 'services' in kwargs.get('update_fields', []):
#             total_duration = self.get_total_duration()
#             self.end_time = self.start_time + total_duration

#         super().save(*args, **kwargs)

#         if creating and self.services.exists():
#             Event.objects.create(
#                 title=f"{self.client.get_full_name()}'s Appointment",
#                 start=self.start_time,
#                 end=self.end_time,
#                 calendar=self.staff.calendar,
#                 description=f"Services: {', '.join(s.name for s in self.services.all())}"
#             )

# # appointments/models.py
# from django.db import models
# from django.conf import settings
# from schedule.models import Calendar, Event
# from datetime import timedelta, datetime, time
# from django.utils.timezone import make_aware, now

# class Service(models.Model):
#     name = models.CharField(max_length=100)
#     duration = models.DurationField(help_text="e.g., 0:15:00 for 15 minutes")
#     price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return self.name

# class Staff(models.Model):
#     staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     services = models.ManyToManyField(Service)
#     calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE)
#     working_hours = models.JSONField(default=dict, blank=True, null=True)
#     buffer_time = models.DurationField(default=timedelta(minutes=15), help_text="Buffer time between appointments")

#     class Meta:
#         verbose_name_plural = "Staff"

#     def __str__(self):
#         return f"{self.staff.get_full_name()} - Staff"

#     def get_working_hours(self, date):
#         default_hours = {'start': '09:00', 'end': '21:00'}
#         if not self.working_hours:
#             return default_hours
#         weekday = date.strftime('%A').lower()
#         return self.working_hours.get(weekday, default_hours)

#     def get_available_slots(self, date, duration):
#         slots = []
#         hours = self.get_working_hours(date)
#         try:
#             sh, sm = map(int, hours['start'].split(':'))
#             eh, em = map(int, hours['end'].split(':'))
#         except:
#             sh, sm, eh, em = 9, 0, 21, 0
#         working_start = make_aware(datetime.combine(date, time(sh, sm)))
#         working_end = make_aware(datetime.combine(date, time(eh, em)))

#         current = working_start
#         while current + duration <= working_end:
#             if self.is_available(current, duration):
#                 slots.append(current)
#             current += timedelta(minutes=15)
#         return slots

#     def is_available(self, start_time, duration):
#         end_time = start_time + duration
#         date = start_time.date()
#         hours = self.get_working_hours(date)
#         try:
#             sh, sm = map(int, hours['start'].split(':'))
#             eh, em = map(int, hours['end'].split(':'))
#         except:
#             sh, sm, eh, em = 9, 0, 21, 0
#         working_start = make_aware(datetime.combine(date, time(sh, sm)))
#         working_end = make_aware(datetime.combine(date, time(eh, em)))

#         if not (working_start <= start_time < working_end and end_time <= working_end):
#             return False

#         buffer = self.buffer_time
#         conflict = Event.objects.filter(
#             calendar=self.calendar,
#             start__lt=end_time + buffer,
#             end__gt=start_time - buffer
#         ).exists()
#         return not conflict

# class Appointment(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('confirmed', 'Confirmed'),
#         ('cancelled', 'Cancelled'),
#         ('completed', 'Completed'),
#     ]

#     client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_appointments')
#     services = models.ManyToManyField(Service)
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_appointments')
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
#     notes = models.TextField(blank=True)
#     created_at = models.DateTimeField(default=now)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['start_time']

#     def __str__(self):
#         return f"{self.client.get_full_name()} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

#     def save(self, *args, **kwargs):
#         if self.start_time and self.services.exists():
#             total = sum((s.duration for s in self.services.all()), timedelta())
#             self.end_time = self.start_time + total
#         super().save(*args, **kwargs)

# # appointments/models.py
# from django.db import models
# from django.conf import settings
# from schedule.models import Calendar, Event
# from datetime import timedelta, datetime, time
# from django.utils.timezone import make_aware, now
# from django.utils.dateparse import parse_datetime

# class Service(models.Model):
#     name = models.CharField(max_length=100)
#     duration = models.DurationField(help_text="e.g., 0:15:00 for 15 minutes")
#     price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return self.name

# class Staff(models.Model):
#     staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     services = models.ManyToManyField(Service)
#     calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE)
#     working_hours = models.JSONField(default=dict, blank=True, null=True)
#     buffer_time = models.DurationField(default=timedelta(minutes=15), help_text="Buffer time between appointments")

#     class Meta:
#         verbose_name_plural = "Staff"

#     def __str__(self):
#         return f"{self.staff.get_full_name()} - Staff"

#     def get_working_hours(self, date):
#         default_hours = {'start': '09:00', 'end': '21:00'}
#         if not self.working_hours:
#             return default_hours
#         weekday = date.strftime('%A').lower()
#         return self.working_hours.get(weekday, default_hours)

#     def get_available_slots(self, date, duration):
#         slots = []
#         hours = self.get_working_hours(date)
#         try:
#             sh, sm = map(int, hours['start'].split(':'))
#             eh, em = map(int, hours['end'].split(':'))
#         except:
#             sh, sm, eh, em = 9, 0, 21, 0
#         working_start = make_aware(datetime.combine(date, time(sh, sm)))
#         working_end = make_aware(datetime.combine(date, time(eh, em)))

#         current = working_start
#         while current + duration <= working_end:
#             if self.is_available(current, duration):
#                 slots.append(current)
#             current += timedelta(minutes=15)
#         return slots

#     def is_available(self, start_time, duration):
#         end_time = start_time + duration
#         date = start_time.date()
#         hours = self.get_working_hours(date)
#         try:
#             sh, sm = map(int, hours['start'].split(':'))
#             eh, em = map(int, hours['end'].split(':'))
#         except:
#             sh, sm, eh, em = 9, 0, 21, 0
#         working_start = make_aware(datetime.combine(date, time(sh, sm)))
#         working_end = make_aware(datetime.combine(date, time(eh, em)))

#         if not (working_start <= start_time < working_end and end_time <= working_end):
#             return False

#         buffer = self.buffer_time
#         conflict = Event.objects.filter(
#             calendar=self.calendar,
#             start__lt=end_time + buffer,
#             end__gt=start_time - buffer
#         ).exists()
#         return not conflict

# class Appointment(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('confirmed', 'Confirmed'),
#         ('cancelled', 'Cancelled'),
#         ('completed', 'Completed'),
#     ]

#     client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_appointments')
#     services = models.ManyToManyField(Service)
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_appointments')
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
#     notes = models.TextField(blank=True)
#     created_at = models.DateTimeField(default=now)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['start_time']

#     def __str__(self):
#         return f"{self.client.get_full_name()} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

#     def save(self, *args, **kwargs):
#         # First, save to ensure self.pk exists for M2M access
#         is_new = self.pk is None
#         super().save(*args, **kwargs)
#         # Only compute end_time after initial save and if services exist
#         if self.pk and self.services.exists():
#             total_duration = sum((s.duration for s in self.services.all()), timedelta())
#             calculated_end = self.start_time + total_duration
#             # Only update if different
#             if self.end_time != calculated_end:
#                 self.end_time = calculated_end
#                 super().save(update_fields=['end_time'])

from django.db import models
from django.conf import settings
from schedule.models import Calendar, Event
from datetime import timedelta, datetime, time
from django.utils.timezone import make_aware, now, is_naive
from django.utils.dateparse import parse_datetime


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    duration = models.DurationField(help_text="e.g., 0:15:00 for 15 minutes")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Staff(models.Model):
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE)
    working_hours = models.JSONField(default=dict, blank=True, null=True)
    buffer_time = models.DurationField(default=timedelta(minutes=15), help_text="Buffer time between appointments")

    class Meta:
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.staff.get_full_name()} - Staff"

    def get_working_hours(self, date):
        default_hours = {'start': '09:00', 'end': '21:00'}
        if not self.working_hours:
            return default_hours
        weekday = date.strftime('%A').lower()
        return self.working_hours.get(weekday, default_hours)

    def get_available_slots(self, date, duration):
        slots = []
        hours = self.get_working_hours(date)
        try:
            sh, sm = map(int, hours['start'].split(':'))
            eh, em = map(int, hours['end'].split(':'))
        except:
            sh, sm, eh, em = 9, 0, 21, 0
        working_start = make_aware(datetime.combine(date, time(sh, sm)))
        working_end = make_aware(datetime.combine(date, time(eh, em)))

        current = working_start
        while current + duration <= working_end:
            if self.is_available(current, duration):
                slots.append(current)
            current += timedelta(minutes=15)
        return slots

    def is_available(self, start_time, duration):
        end_time = start_time + duration
        date = start_time.date()
        hours = self.get_working_hours(date)
        try:
            sh, sm = map(int, hours['start'].split(':'))
            eh, em = map(int, hours['end'].split(':'))
        except:
            sh, sm, eh, em = 9, 0, 21, 0
        working_start = make_aware(datetime.combine(date, time(sh, sm)))
        working_end = make_aware(datetime.combine(date, time(eh, em)))

        if not (working_start <= start_time < working_end and end_time <= working_end):
            return False

        buffer = self.buffer_time
        conflict = Event.objects.filter(
            calendar=self.calendar,
            start__lt=end_time + buffer,
            end__gt=start_time - buffer
        ).exists()
        return not conflict

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_appointments')
    services = models.ManyToManyField(Service)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.client.get_full_name()} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        # Ensure start_time is timezone-aware
        if self.start_time and is_naive(self.start_time):
            self.start_time = make_aware(self.start_time)

        # First save (required to access M2M for services)
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Calculate end_time based on service durations
        if self.pk and self.services.exists():
            total_duration = sum((s.duration for s in self.services.all()), timedelta())
            calculated_end = self.start_time + total_duration
            if self.end_time != calculated_end:
                self.end_time = calculated_end
                super().save(update_fields=['end_time'])
