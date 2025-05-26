from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.timezone import now
from datetime import timedelta
from django.utils.text import slugify

from .models import Staff, Appointment
from schedule.models import Calendar, Event
from .tasks import send_appointment_reminder
# import logging

# @receiver(post_save, sender=Staff)
# def create_staff_calendar(sender, instance, created, **kwargs):
#     if created and not instance.calendar_id:
#         calendar = Calendar.objects.create(name=f"{instance.staff.username} Calendar",slug=f"{instance.staff.username} Slug")
#         instance.calendar = calendar
#         instance.save()


# # Set up logging for debugging
# logger = logging.getLogger(__name__)


# @receiver(post_save, sender=Staff)
# def create_staff_calendar(sender, instance, created, **kwargs):
#     if created and not instance.calendar_id:
#         try:
#             logger.info(f"Creating calendar for {instance.username}")

#             # Generate base name and slug
#             calendar_name = f"{instance.username} Calendar"
#             base_slug = slugify(calendar_name)
#             slug = base_slug

#             # Ensure slug uniqueness
#             counter = 1
#             while Calendar.objects.filter(slug=slug).exists():
#                 slug = f"{base_slug}-{counter}"
#                 counter += 1

#             # Create calendar and associate it with the staff member
#             calendar = Calendar.objects.create(name=calendar_name, slug=slug)
#             Staff.objects.filter(pk=instance.pk).update(calendar_id=calendar.id)

#             logger.info(f"Calendar created: {calendar.name} with slug {calendar.slug}")

#         except Exception as e:
#             logger.error(f"Error creating calendar for {instance.username}: {str(e)}")

# @receiver(post_save, sender=Staff)
# def create_staff_calendar(sender, instance, created, **kwargs):
#     if created and not instance.calendar_id:
#         # Use instance.username, not instance.staff.username
#         calendar_name = f"{instance.username} Calendar"
#         base_slug = slugify(calendar_name)
#         slug = base_slug
#         counter = 1
#         while Calendar.objects.filter(slug=slug).exists():
#             slug = f"{base_slug}-{counter}"
#             counter += 1

#         calendar = Calendar.objects.create(name=calendar_name, slug=slug)
#         # Avoid infinite recursion by updating only the calendar field
#         Staff.objects.filter(pk=instance.pk).update(calendar=calendar)


# @receiver(post_save, sender=Appointment)
# def schedule_appointment_reminders(sender, instance, created, **kwargs):
#     if created and instance.status == 'confirmed':
#         # 24-hour reminder
#         send_appointment_reminder.apply_async(
#             (instance.id,),
#             eta=instance.start_time - timedelta(hours=24)
#         )
#         # 1-hour reminder
#         send_appointment_reminder.apply_async(
#             (instance.id,),
#             eta=instance.start_time - timedelta(hours=1)
#         )

#         # Send confirmation email
#         subject = f"Appointment Confirmation - {instance.start_time.strftime('%b %d, %Y')}"
#         context = {
#             'client': instance.client,
#             'appointment': instance,
#             'services': instance.services.all(),
#             'staff': instance.staff
#         }
#         html_message = render_to_string('emails/appointment_confirmation.html', context)
#         text_message = render_to_string('emails/appointment_confirmation.txt', context)

#         if instance.client.email:
#             send_mail(
#                 subject,
#                 text_message,
#                 'no-reply@salonapp.com',
#                 [instance.client.email],
#                 html_message=html_message,
#                 fail_silently=False
#             )


# @receiver(post_save, sender=Appointment)
# def schedule_appointment_reminders(sender, instance, created, **kwargs):
#     if created and instance.status == 'confirmed':
#         # 24-hour reminder (assuming you have a Celery task defined)
#         # send_appointment_reminder.apply_async(
#         #     (instance.id,),
#         #     eta=instance.start_time - timedelta(hours=24)
#         # )
#         # # 1-hour reminder (assuming you have a Celery task defined)
#         # send_appointment_reminder.apply_async(
#         #     (instance.id,),
#         #     eta=instance.start_time - timedelta(hours=1)
#         # )

#         # Send confirmation email without relying on an HTML file
#         subject = f"Appointment Confirmation - {instance.start_time.strftime('%b %d, %Y')}"
#         context = {
#             'client': instance.client,
#             'appointment': instance,
#             'services': instance.services.all(),
#             'staff': instance.staff
#         }

#         client_name = f"{context['client'].first_name} {context['client'].last_name}"
#         staff_name = context['staff'].staff.get_full_name() if context['staff'] else 'Not assigned'

#         # Construct the plain text message
#         text_message = f"""
# Dear {client_name},

# Your appointment has been confirmed for:
# Date: {context['appointment'].start_time.strftime('%b %d, %Y at %I:%M %p')}
# Services: {', '.join([service.name for service in context['services']])}
# Staff: {staff_name}

# We look forward to seeing you!

# Sincerely,
# The Salon Team
# """

#         # Construct the HTML message directly
#         html_message = f"""
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="utf-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1">
#     <title>Appointment Confirmation</title>
# </head>
# <body>
#     <p>Dear <strong>{client_name}</strong>,</p>
#     <p>Your appointment has been <strong>confirmed</strong> for:</p>
#     <ul>
#         <li><strong>Date:</strong> {context['appointment'].start_time.strftime('%b %d, %Y at %I:%M %p')}</li>
#         <li><strong>Services:</strong> {', '.join([service.name for service in context['services']])}</li>
#         <li><strong>Staff:</strong> {staff_name}</li>
#     </ul>
#     <p>We look forward to seeing you!</p>
#     <p>Sincerely,<br>The Salon Team</p>
# </body>
# </html>
# """

#         if instance.client.email:
#             send_mail(
#                 subject,
#                 text_message,
#                 'no-reply@salonapp.com',
#                 [instance.client.email],
#                 html_message=html_message,
#                 fail_silently=False
#             )

#---------------------------------------------Better-below------------------------------------------------------------------------------

# #variety/appointment/signals.py
# import logging
# from django.core.mail import send_mail
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from datetime import timedelta
# from .models import Appointment  # Assuming Appointment model is in the same app

# # Get an instance of a logger
# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=Appointment)
# def schedule_appointment_reminders(sender, instance, created, **kwargs):
#     if created and instance.status == 'confirmed':
#         # Log that the signal is being processed
#         logger.info(f"schedule_appointment_reminders signal triggered for Appointment ID: {instance.id}")

#         try:
#             # Fetch the appointment again to be absolutely sure we have the services
#             appointment = Appointment.objects.get(pk=instance.pk)
#             services = appointment.services.all()

#             # Log the number of services fetched
#             logger.info(f"Number of services fetched: {services.count()}")

#             # Log the service names
#             service_names_list = [service.name for service in services]
#             logger.info(f"Service names: {service_names_list}")
            
#             subject = f"Appointment Confirmation - {appointment.start_time.strftime('%b %d, %Y')}"
#             context = {
#                 'client': appointment.client,
#                 'appointment': appointment,
#                 'services': services,
#                 'staff': appointment.staff,
#             }

#             client_name = f"{context['client'].first_name} {context['client'].last_name}"
#             staff_name = context['staff'].staff.get_full_name() if context['staff'] else 'Not assigned'
#             service_names = ', '.join([service.name for service in context['services']])
            
#             # Construct the plain text message
#             text_message = f"""
#                 Dear {client_name},

#                 Your appointment has been confirmed for:
#                 Date: {context['appointment'].start_time.strftime('%b %d, %Y at %I:%M %p')}
#                 Services: {service_names}
#                 Staff: {staff_name}

#                 We look forward to seeing you!

#                 Sincerely,
#                 The Salon Team
#                 """
            
#             # Construct the HTML message directly
#             html_message = f"""
#                 <!DOCTYPE html>
#                 <html>
#                 <head>
#                     <meta charset="utf-8">
#                     <meta name="viewport" content="width=device-width, initial-scale=1">
#                     <title>Appointment Confirmation</title>
#                 </head>
#                 <body>
#                     <p>Dear <strong>{client_name}</strong>,</p>
#                     <p>Your appointment has been <strong>confirmed</strong> for:</p>
#                     <ul>
#                         <li><strong>Date:</strong> {context['appointment'].start_time.strftime('%b %d, %Y at %I:%M %p')}</li>
#                         <li><strong>Services:</strong> {service_names}</li>
#                         <li><strong>Staff:</strong> {staff_name}</li>
#                     </ul>
#                     <p>We look forward to seeing you!</p>
#                     <p>Sincerely,<br>The Salon Team</p>
#                 </body>
#                 </html>
#                 """
#             if appointment.client.email:
#                 send_mail(
#                     subject,
#                     text_message,
#                     'no-reply@salonapp.com',
#                     [appointment.client.email],
#                     html_message=html_message,
#                     fail_silently=False
#                 )
#                 logger.info(f"Email sent successfully to {appointment.client.email}") #log
#         except Exception as e:
#             logger.error(f"Error sending email: {e}", exc_info=True)

#----------------------------------------------------------Better-Above----------------------------------------------------------
# variety/appointment/signals.py

import logging
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from .tasks import update_staff_available_slots

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Appointment)
def schedule_appointment_reminders(sender, instance, created, **kwargs):
    if created and instance.status == 'confirmed':
        logger.info(f"Triggered signal for Appointment ID: {instance.id}")

        try:
            services = instance.services.all()
            service_names = ', '.join(service.name for service in services)
            client_name = f"{instance.client.first_name} {instance.client.last_name}"
            staff_name = instance.staff.staff.get_full_name() if instance.staff else 'Not assigned'

            subject = f"Appointment Confirmation - {instance.start_time.strftime('%b %d, %Y')}"
            text_message = f"""
            Dear {client_name},

            Your appointment has been confirmed for:
            Date: {instance.start_time.strftime('%b %d, %Y at %I:%M %p')}
            Services: {service_names}
            Staff: {staff_name}

            Sincerely,
            The Salon Team
            """
            html_message = f"""
            <html><body>
            <p>Dear <strong>{client_name}</strong>,</p>
            <p>Your appointment has been <strong>confirmed</strong> for:</p>
            <ul>
            <li><strong>Date:</strong> {instance.start_time.strftime('%b %d, %Y at %I:%M %p')}</li>
            <li><strong>Services:</strong> {service_names}</li>
            <li><strong>Staff:</strong> {staff_name}</li>
            </ul>
            <p>Sincerely,<br>The Salon Team</p>
            </body></html>
            """

            if instance.client.email:
                send_mail(
                    subject, text_message,
                    'no-reply@salonapp.com',
                    [instance.client.email],
                    html_message=html_message
                )
                logger.info(f"Email sent to {instance.client.email}")

            # 🔄 Trigger Celery task to update slot cache
            update_staff_available_slots.delay(
                staff_id=instance.staff.id,
                date_str=instance.start_time.date().isoformat(),
                service_ids=[s.id for s in services]
            )

        except Exception as e:
            logger.error(f"Signal processing failed: {e}", exc_info=True)
