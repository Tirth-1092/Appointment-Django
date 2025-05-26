# from celery import shared_task
# from django.core.mail import send_mail
# from django.utils import timezone
# from datetime import timedelta
# from .models import Appointment

# @shared_task(bind=True, max_retries=3, default_retry_delay=60)
# def send_appointment_reminder(self, appointment_id):
#     try:
#         appointment = Appointment.objects.get(id=appointment_id)
#         client = appointment.client

#         if client.email:
#             send_mail(
#                 subject='Appointment Reminder',
#                 message=(
#                     f"Dear {client.username},\n\n"
#                     f"This is a reminder for your appointment for '{appointment.service.name}' "
#                     f"scheduled at {appointment.start_time.strftime('%Y-%m-%d %H:%M')}.\n\n"
#                     f"Thank you!"
#                 ),
#                 from_email='no-reply@salonapp.com',
#                 recipient_list=[client.email],
#                 fail_silently=False,
#             )
#     except Appointment.DoesNotExist:
#         # Appointment was deleted or invalid
#         pass
#     except Exception as exc:
#         raise self.retry(exc=exc)


# @shared_task
# def generate_monthly_report():
#     now = timezone.now()
#     start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     end_of_month = (start_of_month + timedelta(days=32)).replace(day=1)

#     total_bookings = Appointment.objects.filter(start_time__gte=start_of_month, start_time__lt=end_of_month).count()
#     # Assuming `status` field exists in model (you might need to add this if not already)
#     cancelled = Appointment.objects.filter(status='cancelled', start_time__gte=start_of_month, start_time__lt=end_of_month).count()

#     # Log or send the report
#     print(f"Monthly Report: {total_bookings} bookings, {cancelled} cancellations")


# @shared_task
# def cleanup_expired_appointments():
#     threshold = timezone.now() - timedelta(days=30)
#     expired_appointments = Appointment.objects.filter(start_time__lt=threshold, is_deleted=True)
#     count = expired_appointments.count()
#     expired_appointments.delete()
#     print(f"Cleaned up {count} expired soft-deleted appointments.")

#----------------------------------------------------------Better-Below----------------------------------------------------------


# # variety/appointment/tasks.py
# from celery import shared_task
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils import timezone
# from .models import Appointment
# from datetime import timedelta

# @shared_task(bind=True, max_retries=3, default_retry_delay=60)
# def send_appointment_reminder(self, appointment_id):
#     try:
#         appointment = Appointment.objects.get(id=appointment_id)
#         if appointment.status != 'confirmed':
#             return
            
#         subject = f"Appointment Reminder - {appointment.start_time.strftime('%b %d, %Y')}"
#         context = {
#             'appointment': appointment,
#             'services': appointment.services.all(),
#             'staff': appointment.staff
#         }
#         html_message = render_to_string('emails/appointment_reminder.html', context)
#         text_message = render_to_string('emails/appointment_reminder.txt', context)

#         if appointment.client.email:
#             send_mail(
#                 subject,
#                 text_message,
#                 'no-reply@salonapp.com',
#                 [appointment.client.email],
#                 html_message=html_message,
#                 fail_silently=False
#             )
#     except Appointment.DoesNotExist:
#         pass
#     except Exception as exc:
#         raise self.retry(exc=exc)

# @shared_task
# def cleanup_past_appointments():
#     """Archive completed appointments older than 30 days"""
#     threshold = timezone.now() - timedelta(days=30)
#     Appointment.objects.filter(
#         start_time__lt=threshold,
#         status='completed'
#     ).delete()
    #----------------------------------------------------------Better-Above----------------------------------------------------------

# from celery import shared_task
# from django.core.cache import cache
# from django.utils import timezone
# from .models import Appointment, Staff, Service
# from datetime import timedelta, datetime

# @shared_task(bind=True, max_retries=3, default_retry_delay=60)
# def send_appointment_reminder(self, appointment_id):
#     try:
#         appointment = Appointment.objects.get(id=appointment_id)
#         if appointment.status != 'confirmed':
#             return

#         # (Email sending logic, already in signal)
#     except Appointment.DoesNotExist:
#         pass
#     except Exception as exc:
#         raise self.retry(exc=exc)

# @shared_task
# def cleanup_past_appointments():
#     """Archive completed appointments older than 30 days"""
#     threshold = timezone.now() - timedelta(days=30)
#     Appointment.objects.filter(
#         start_time__lt=threshold,
#         status='completed'
#     ).delete()

# @shared_task
# def update_staff_available_slots(staff_id, date_str, service_ids):
#     try:
#         staff = Staff.objects.get(pk=staff_id)
#         date = datetime.strptime(date_str, "%Y-%m-%d").date()
#         services = Service.objects.filter(id__in=service_ids)
#     except (Staff.DoesNotExist, ValueError):
#         return

#     total_duration = sum((s.duration for s in services), timedelta())
#     slots = staff.get_available_slots(date, total_duration)

#     slot_data = [
#         {
#             'staff_id': staff.id,
#             'staff_name': staff.staff.get_full_name(),
#             'time': slot.strftime('%H:%M')
#         }
#         for slot in slots
#     ]

#     cache_key = f"available_slots:{staff.id}:{date_str}:{'-'.join(map(str, service_ids))}"
#     cache.set(cache_key, slot_data, timeout=600)  # 10 mins

# variety/appointment/tasks.py
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from .models import Appointment, Staff, Service
from datetime import timedelta, datetime
import pytz

INDIAN_TZ = pytz.timezone('Asia/Kolkata')


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_appointment_reminder(self, appointment_id):
    """
    Sends a reminder for a confirmed appointment.
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.status != 'confirmed':
            return
        # Reminder logic (email/SMS/etc.) is assumed to be handled elsewhere (e.g., signals)
    except Appointment.DoesNotExist:
        return
    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task
def cleanup_past_appointments():
    """
    Deletes completed appointments older than 30 days.
    """
    threshold = timezone.now().astimezone(INDIAN_TZ) - timedelta(days=30)
    Appointment.objects.filter(
        start_time__lt=threshold,
        status='completed'
    ).delete()


@shared_task
def update_staff_available_slots(staff_id, date_str, service_ids):
    """
    Rebuilds and caches the available slot map for a given staff and service set on a date.
    """
    try:
        staff = Staff.objects.get(pk=staff_id)
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        services = Service.objects.filter(id__in=service_ids)
    except (Staff.DoesNotExist, ValueError):
        return

    # Calculate total duration
    total_duration = sum((s.duration for s in services), timedelta())

    # Build slot data using existing logic (timezone-aware)
    slots = staff.get_available_slots(date, total_duration)

    # Convert to India timezone and format
    slot_data = [
        {
            'staff_id': staff.id,
            'staff_name': staff.staff.get_full_name(),
            'time': slot.astimezone(INDIAN_TZ).strftime('%H:%M'),
            'available': True  # You may want to include availability flag if needed
        }
        for slot in slots
    ]

    # Cache for 10 minutes
    cache_key = f"available_slots:{staff.id}:{date_str}:{'-'.join(map(str, service_ids))}"
    cache.set(cache_key, slot_data, timeout=600)
