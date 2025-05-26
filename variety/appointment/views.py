# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import Service, Staff, Appointment
# from .serializers import ServiceSerializer, StaffSerializer, AppointmentSerializer
# from datetime import datetime, timedelta
# from schedule.models import Event
# from rest_framework.status import HTTP_400_BAD_REQUEST
# from rest_framework.exceptions import NotAuthenticated

# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     permission_classes = [IsAuthenticated]


# class StaffViewSet(viewsets.ModelViewSet):
#     # queryset = Staff.objects.all()
#     serializer_class = StaffSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Staff.objects.filter(staff__is_staff=True, staff__is_superuser=False)


#     @action(detail=True, methods=['get'])
#     def availability(self, request, pk=None):
#         staff = self.get_object()
#         events = staff.calendar.events.all()
#         data = [{
#             'title': e.title,
#             'start': e.start,
#             'end': e.end
#         } for e in events]
#         return Response(data)


# # class AppointmentViewSet(viewsets.ModelViewSet):
# #     serializer_class = AppointmentSerializer
# #     permission_classes = [IsAuthenticated]

# #     def get_queryset(self):
# #         user = self.request.user
# #         if user.is_staff:
# #             # Employee: show only appointments assigned to them
# #             return Appointment.objects.filter(staff__staff=user)
# #         else:
# #             # Customer: show only their own appointments
# #             return Appointment.objects.filter(client=user)

# #     def perform_create(self, serializer):
# #         serializer.save(client=self.request.user)


# class AppointmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AppointmentSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if not user or not user.is_authenticated:
#             raise NotAuthenticated("Authentication credentials were not provided.")

#         if hasattr(user, 'staff'):
#             # Employee: show only appointments assigned to them
#             return Appointment.objects.filter(staff__user=user)
#         else:
#             # Customer: show only their own appointments
#             return Appointment.objects.filter(client=user)

#     def perform_create(self, serializer):
#         serializer.save(client=self.request.user)


# class AvailableSlotsViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=["get"], url_path="available-slots")
#     def available_slots(self, request):
#         # Get the requested date
#         date_str = request.query_params.get('date')
#         if not date_str:
#             return Response({"error": "Date parameter is required."}, status=HTTP_400_BAD_REQUEST)
        
#         try:
#             requested_date = datetime.strptime(date_str, '%Y-%m-%d').date()
#         except ValueError:
#             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=HTTP_400_BAD_REQUEST)

#         # Get selected services and calculate total duration
#         service_ids = request.query_params.getlist('services', [])
#         selected_services = Service.objects.filter(id__in=service_ids)
#         total_service_duration = sum(service.duration.total_seconds() for service in selected_services)

#         available_slots = []

#         # Iterate over staff members
#         for staff in Staff.objects.all():
#             staff_calendar = staff.calendar
#             work_start_time = datetime.combine(requested_date, datetime.min.time()) + timedelta(hours=9)
#             work_end_time = datetime.combine(requested_date, datetime.min.time()) + timedelta(hours=21)
#             current_time = work_start_time

#             # Get existing events (appointments) for this day
#             existing_events = Event.objects.filter(
#                 calendar=staff_calendar,
#                 start__gte=work_start_time,
#                 end__lte=work_end_time
#             ).order_by('start')

#             for event in existing_events:
#                 # Check if there's space before this event
#                 if current_time + timedelta(seconds=total_service_duration) <= event.start:
#                     available_slots.append({
#                         'staff': staff.staff.username,
#                         'start_time': current_time.strftime('%Y-%m-%d %H:%M'),
#                         'end_time': (current_time + timedelta(seconds=total_service_duration)).strftime('%Y-%m-%d %H:%M')
#                     })
#                 current_time = event.end

#             # Check after last event
#             if current_time + timedelta(seconds=total_service_duration) <= work_end_time:
#                 available_slots.append({
#                     'staff': staff.staff.username,
#                     'start_time': current_time.strftime('%Y-%m-%d %H:%M'),
#                     'end_time': (current_time + timedelta(seconds=total_service_duration)).strftime('%Y-%m-%d %H:%M')
#                 })

#         return Response({'available_slots': available_slots})


# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.exceptions import NotAuthenticated
# from rest_framework.status import HTTP_400_BAD_REQUEST
# from .models import Service, Staff, Appointment
# from .serializers import ServiceSerializer, StaffSerializer, AppointmentSerializer
# from schedule.models import Event
# from datetime import datetime, timedelta


# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     # permission_classes = [IsAuthenticated]


# class StaffViewSet(viewsets.ModelViewSet):
#     serializer_class = StaffSerializer
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Staff.objects.filter(staff__is_staff=True, staff__is_superuser=False)

#     @action(detail=True, methods=['get'])
#     def availability(self, request, pk=None):
#         staff = self.get_object()
#         events = staff.calendar.events.all()
#         data = [{
#             'title': e.title,
#             'start': e.start,
#             'end': e.end
#         } for e in events]
#         return Response(data)


# class AppointmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AppointmentSerializer
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if not user or not user.is_authenticated:
#             raise NotAuthenticated("Authentication credentials were not provided.")

#         if hasattr(user, 'staff'):
#             return Appointment.objects.filter(staff__staff=user)
#         else:
#             return Appointment.objects.filter(client=user)

#     def perform_create(self, serializer):
#         serializer.save(client=self.request.user)

#     @action(detail=False, methods=["get"], url_path="available-slots")
#     def available_slots(self, request):
#         date_str = request.query_params.get('date')
#         if not date_str:
#             return Response({"error": "Date parameter is required."}, status=HTTP_400_BAD_REQUEST)

#         try:
#             requested_date = datetime.strptime(date_str, '%Y-%m-%d').date()
#         except ValueError:
#             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=HTTP_400_BAD_REQUEST)

#         service_ids = request.query_params.getlist('services', [])
#         selected_services = Service.objects.filter(id__in=service_ids)
#         total_service_duration = sum(service.duration.total_seconds() for service in selected_services)

#         available_slots = []

#         for staff in Staff.objects.all():
#             staff_calendar = staff.calendar
#             work_start_time = datetime.combine(requested_date, datetime.min.time()) + timedelta(hours=9)
#             work_end_time = datetime.combine(requested_date, datetime.min.time()) + timedelta(hours=21)
#             current_time = work_start_time

#             existing_events = Event.objects.filter(
#                 calendar=staff_calendar,
#                 start__gte=work_start_time,
#                 end__lte=work_end_time
#             ).order_by('start')

#             for event in existing_events:
#                 if current_time + timedelta(seconds=total_service_duration) <= event.start:
#                     available_slots.append({
#                         'staff': staff.staff.username,
#                         'start_time': current_time.strftime('%Y-%m-%d %H:%M'),
#                         'end_time': (current_time + timedelta(seconds=total_service_duration)).strftime('%Y-%m-%d %H:%M')
#                     })
#                 current_time = event.end

#             if current_time + timedelta(seconds=total_service_duration) <= work_end_time:
#                 available_slots.append({
#                     'staff': staff.staff.username,
#                     'start_time': current_time.strftime('%Y-%m-%d %H:%M'),
#                     'end_time': (current_time + timedelta(seconds=total_service_duration)).strftime('%Y-%m-%d %H:%M')
#                 })

#         return Response({'available_slots': available_slots})


# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.status import HTTP_400_BAD_REQUEST
# from datetime import datetime, time, timedelta
# from .models import Service, Staff, Appointment
# from .serializers import ServiceSerializer, StaffSerializer, AppointmentSerializer
# from schedule.models import Event


# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer


# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer


# class AppointmentViewSet(viewsets.ModelViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer

#     def perform_create(self, serializer):
#         serializer.save(client=self.request.user)


#     @action(detail=False, methods=["get"], url_path="available-slots")
#     def available_slots(self, request):
#         date_str = request.query_params.get('date')
#         service_ids = request.query_params.getlist('services')

#         if not date_str or not service_ids:
#             return Response({"error": "Date and service(s) are required."}, status=HTTP_400_BAD_REQUEST)

#         try:
#             date = datetime.strptime(date_str, '%Y-%m-%d').date()
#         except ValueError:
#             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=HTTP_400_BAD_REQUEST)

#         services = Service.objects.filter(id__in=service_ids)
#         total_duration = sum((s.duration for s in services), timedelta())

#         work_start = datetime.combine(date, time(9, 0))
#         work_end = datetime.combine(date, time(21, 0))
#         slot_size = timedelta(minutes=15)

#         all_slots = []

#         for staff in Staff.objects.all():
#             if not all(service in staff.services.all() for service in services):
#                 continue

#             events = Event.objects.filter(
#                 calendar=staff.calendar,
#                 start__lt=work_end,
#                 end__gt=work_start
#             ).order_by('start')

#             busy_periods = [(event.start, event.end) for event in events]

#             current = work_start
#             while current + total_duration <= work_end:
#                 conflict = any(start < current + total_duration and end > current for start, end in busy_periods)
#                 if not conflict:
#                     all_slots.append({
#                         "staff": staff.staff.username,
#                         "start_time": current.strftime('%Y-%m-%d %H:%M'),
#                         "end_time": (current + total_duration).strftime('%Y-%m-%d %H:%M')
#                     })
#                 current += slot_size

#         return Response({"available_slots": all_slots})


# # views.py
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.utils.timezone import make_aware
# from datetime import datetime, timedelta
# from .models import Service, Staff, Appointment
# from .serializers import ServiceSerializer, StaffSerializer, AppointmentSerializer

# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer


# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer

#     def perform_create(self, serializer):
#         serializer.save(staff=self.request.user)


# class AppointmentViewSet(viewsets.ModelViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff:
#             return Appointment.objects.all()
#         return Appointment.objects.filter(client=user)

#     def perform_create(self, serializer):
#         serializer.save(client=self.request.user)

#     @action(detail=False, methods=['post'], url_path='available-slots')
#     def available_slots(self, request):
#         services_ids = request.data.get('services', [])
#         date = request.data.get('date')
#         if not services_ids or not date:
#             return Response({'error': 'services and date are required'}, status=400)

#         try:
#             date_obj = datetime.strptime(date, '%Y-%m-%d').date()
#         except ValueError:
#             return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)

#         services = Service.objects.filter(id__in=services_ids)
#         total_duration = sum([s.duration for s in services], timedelta())

#         available_slots = []
#         for hour in range(9, 21):
#             slot_start = make_aware(datetime.combine(date_obj, datetime.strptime(f"{hour}:00", "%H:%M").time()))
#             for staff in Staff.objects.all():
#                 if all(s in staff.services.all() for s in services) and staff.is_available(slot_start, total_duration):
#                     available_slots.append({
#                         'time': slot_start,
#                         'staff': staff.staff.username
#                     })
#         return Response(available_slots)

#------------------------------------------------

# from rest_framework import viewsets, status, serializers
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.utils.timezone import make_aware
# from datetime import datetime, timedelta, time

# from .models import Service, Staff, Appointment
# from .serializers import ServiceSerializer, StaffSerializer, AppointmentSerializer
# from schedule.models import Calendar


# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer


# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer

#     def perform_create(self, serializer):
#         user = self.request.user

#         # ❗ Prevent duplicate staff registration
#         if Staff.objects.filter(staff=user).exists():
#             raise serializers.ValidationError("This user is already registered as staff.")

#         # ✅ Automatically create calendar
#         calendar = Calendar.objects.create(name=f"{user.username}'s Calendar")
#         serializer.save(staff=user, calendar=calendar)


# # class AppointmentViewSet(viewsets.ModelViewSet):
# #     queryset = Appointment.objects.all()
# #     serializer_class = AppointmentSerializer

# #     def get_queryset(self):
# #         user = self.request.user
# #         return Appointment.objects.all() if user.is_staff else Appointment.objects.filter(client=user)

# #     def perform_create(self, serializer):
# #         serializer.save(client=self.request.user)

# #     @action(detail=False, methods=['post'], url_path='available-slots')
# #     def available_slots(self, request):
# #         services_ids = request.data.get('services')
# #         date = request.data.get('date')

# #         if not services_ids or not date:
# #             return Response({'error': 'services and date are required'}, status=400)

# #         try:
# #             date_obj = datetime.strptime(date, '%Y-%m-%d').date()
# #         except ValueError:
# #             return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)

# #         services = Service.objects.filter(id__in=services_ids)
# #         total_duration = sum((s.duration for s in services), timedelta())
# #         slots = []

# #         current_time = make_aware(datetime.combine(date_obj, time(9, 0)))
# #         end_boundary = make_aware(datetime.combine(date_obj, time(21, 0)))
# #         interval = timedelta(minutes=15)

# #         while current_time + total_duration <= end_boundary:
# #             for staff in Staff.objects.all():
# #                 if all(s in staff.services.all() for s in services) and staff.is_available(current_time, total_duration):
# #                     slots.append({
# #                         'time': current_time.strftime('%H:%M'),
# #                         'staff': staff.staff.username
# #                     })
# #                     break
# #             current_time += interval

# #         return Response(slots)


# class AppointmentViewSet(viewsets.ModelViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Appointment.objects.all() if user.is_staff else Appointment.objects.filter(client=user)

#     def perform_create(self, serializer):
#         serializer.save(client=self.request.user)

#     @action(detail=False, methods=['post'], url_path='available-slots')
#     def available_slots(self, request):
#         services_ids = request.data.get('services')
#         date = request.data.get('date')

#         if not services_ids or not date:
#             return Response({'error': 'services and date are required'}, status=400)

#         try:
#             date_obj = datetime.strptime(date, '%Y-%m-%d').date()
#         except ValueError:
#             return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)

#         services = Service.objects.filter(id__in=services_ids)
#         if not services.exists():
#             return Response({'error': 'One or more services not found'}, status=404)

#         total_duration = sum((s.duration for s in services), timedelta())
#         interval = timedelta(minutes=15)
#         slots = []

#         current_time = make_aware(datetime.combine(date_obj, time(9, 0)))
#         end_boundary = make_aware(datetime.combine(date_obj, time(21, 0)))

#         while current_time + total_duration <= end_boundary:
#             for staff in Staff.objects.all():
#                 if all(s in staff.services.all() for s in services) and staff.is_available(current_time, total_duration):
#                     slots.append({
#                         'time': current_time.strftime('%H:%M'),
#                         'staff': staff.staff.username
#                     })
#                     break
#             current_time += interval

#         return Response(slots)


# from rest_framework import viewsets, serializers
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.utils.timezone import make_aware
# from datetime import datetime, timedelta, time

# from schedule.models import Event, Calendar
# from .models import Service, Staff, Appointment
# from .serializers import (
#     ServiceSerializer,
#     StaffSerializer,
#     AppointmentSerializer,
#     AvailableSlotSerializer
# )


# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer


# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer

#     def perform_create(self, serializer):
#         user = self.request.user
#         if Staff.objects.filter(staff=user).exists():
#             raise serializers.ValidationError("This user is already registered as staff.")
#         calendar = Calendar.objects.create(name=f"{user.username}'s Calendar")
#         serializer.save(staff=user, calendar=calendar)


# class AppointmentViewSet(viewsets.ModelViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Appointment.objects.all() if user.is_staff else Appointment.objects.filter(client=user)

#     def perform_create(self, serializer):
#         serializer.save(client=self.request.user)


# class AvailableSlotViewSet(viewsets.ModelViewSet):
#     serializer_class = AvailableSlotSerializer

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_superuser:
#             return Event.objects.all()
#         try:
#             staff = Staff.objects.get(staff=user)
#             return Event.objects.filter(calendar=staff.calendar)
#         except Staff.DoesNotExist:
#             return Event.objects.none()

#     def perform_create(self, serializer):
#         serializer.save()

# from rest_framework import viewsets, serializers
# from schedule.models import Event, Calendar
# from .models import Service, Staff, Appointment
# from .serializers import (
#     ServiceSerializer,
#     StaffSerializer,
#     AppointmentSerializer,
#     AvailableSlotSerializer
# )


# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer


# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer

#     def perform_create(self, serializer):
#         user = self.request.user
#         if Staff.objects.filter(staff=user).exists():
#             raise serializers.ValidationError("This user is already registered as staff.")
#         calendar = Calendar.objects.create(name=f"{user.username}'s Calendar")
#         serializer.save(staff=user, calendar=calendar)


# class AppointmentViewSet(viewsets.ModelViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Appointment.objects.all() if user.is_staff else Appointment.objects.filter(client=user)

#     def perform_create(self, serializer):
#         serializer.save(client=self.request.user)


# class AvailableSlotViewSet(viewsets.ModelViewSet):
#     serializer_class = AvailableSlotSerializer

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_superuser:
#             return Event.objects.all()
#         try:
#             staff = Staff.objects.get(staff=user)
#             return Event.objects.filter(calendar=staff.calendar)
#         except Staff.DoesNotExist:
#             return Event.objects.none()

#     def perform_create(self, serializer):
#         serializer.save()


# from rest_framework import viewsets, serializers
# from schedule.models import Event, Calendar
# from .models import Service, Staff, Appointment
# from .serializers import (
#     ServiceSerializer,
#     StaffSerializer,
#     AppointmentSerializer,
#     AvailableSlotSerializer
# )


# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer


# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer

#     def perform_create(self, serializer):
#         user = self.request.user
#         if Staff.objects.filter(staff=user).exists():
#             raise serializers.ValidationError("Already registered as staff.")
#         calendar = Calendar.objects.create(name=f"{user.username}'s Calendar")
#         serializer.save(staff=user, calendar=calendar)


# class AppointmentViewSet(viewsets.ModelViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Appointment.objects.all() if user.is_staff else Appointment.objects.filter(client=user)

#     def perform_create(self, serializer):
#         serializer.save(client=self.request.user)


# class AvailableSlotViewSet(viewsets.ModelViewSet):
#     serializer_class = AvailableSlotSerializer

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_superuser:
#             return Event.objects.all()
#         try:
#             staff = Staff.objects.get(staff=user)
#             return Event.objects.filter(calendar=staff.calendar, title__icontains="available slot")
#         except Staff.DoesNotExist:
#             return Event.objects.none()

#     def perform_create(self, serializer):
#         serializer.save()


# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.shortcuts import get_object_or_404
# from django.utils.timezone import now
# from datetime import timedelta, datetime
# from schedule.models import Calendar, Event

# from .models import Service, Staff, Appointment
# from .serializers import (ServiceSerializer,StaffSerializer,AppointmentSerializer,AvailableSlotSerializer)
# from django.utils.text import slugify
# from rest_framework.exceptions import ValidationError

# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     # permission_classes = [IsAuthenticated]

# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer
#     # permission_classes = [IsAuthenticated]

#     # def perform_create(self, serializer):
#     #     user = self.request.user
#     #     if Staff.objects.filter(staff=user).exists():
#     #         raise serializers.ValidationError("Already registered as staff.")
#     #     calendar = Calendar.objects.create(name=f"{user.username}'s Calendar")
#     #     serializer.save(staff=user, calendar=calendar)


#     def perform_create(self, serializer):
#         user = self.request.user
#         if Staff.objects.filter(staff=user).exists():
#             raise ValidationError("Already registered as staff.")
#         # Generate calendar name and slug
#         calendar_name = f"{user.username} Calendar"
#         base_slug = slugify(calendar_name)
#         slug = base_slug
#         # Ensure unique slug
#         counter = 1
#         while Calendar.objects.filter(slug=slug).exists():
#             slug = f"{base_slug}-{counter}"
#             counter += 1
#         # Create calendar
#         calendar = Calendar.objects.create(name=calendar_name, slug=slug)
#         # Save staff with calendar
#         serializer.save(staff=user, calendar=calendar)

#     @action(detail=True, methods=['get'])
#     def availability(self, request, pk=None):
#         staff = self.get_object()
#         date_str = request.query_params.get('date')
#         duration_min = request.query_params.get('duration', 60)
        
#         try:
#             date = datetime.strptime(date_str, '%Y-%m-%d').date()
#             duration = timedelta(minutes=int(duration_min))
#         except (ValueError, TypeError):
#             return Response(
#                 {'error': 'Invalid date or duration format'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         slots = staff.get_available_slots(date, duration)
#         return Response({
#             'date': date_str,
#             'duration_minutes': duration.total_seconds() / 60,
#             'available_slots': [slot.strftime('%H:%M') for slot in slots]
#         })

# class AppointmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AppointmentSerializer
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff:
#             return Appointment.objects.filter(staff__staff=user)
#         return Appointment.objects.filter(client=user)

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
        
#         # Check if we're looking for available slots
#         if 'date' in request.query_params and 'services[]' in request.query_params:
#             dummy_appointment = Appointment()
#             serializer = self.get_serializer(dummy_appointment)
#             return Response(serializer.data)
            
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#     @action(detail=True, methods=['post'])
#     def cancel(self, request, pk=None):
#         appointment = self.get_object()
#         if appointment.status == 'cancelled':
#             return Response(
#                 {'status': 'Already cancelled'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         appointment.status = 'cancelled'
#         appointment.save()
        
#         # Delete corresponding event
#         Event.objects.filter(
#             calendar=appointment.staff.calendar,
#             start=appointment.start_time,
#             end=appointment.end_time
#         ).delete()
        
#         return Response({'status': 'cancelled'})

#     @action(detail=False, methods=['get'])
#     def upcoming(self, request):
#         queryset = self.get_queryset().filter(
#             start_time__gte=now(),
#             status__in=['confirmed', 'pending']
#         ).order_by('start_time')
        
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

# class AvailableSlotsView(viewsets.ViewSet):
#     # permission_classes = [IsAuthenticated]

#     def list(self, request):
#         serializer = AvailableSlotSerializer(data=request.query_params)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
#         slots = serializer.get_available_slots()
#         return Response({
#             'date': serializer.validated_data['date'],
#             'services': serializer.validated_data['services'],
#             'available_slots': slots
#         })

# # --------------------------------------------------Better-Below-code----------------------------------------------
# # appointments/views.py
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Service, Staff, Appointment, Category
# from .serializers import ServiceSerializer, StaffSerializer, AppointmentSerializer, AvailableSlotSerializer,CategorySerializer
# from rest_framework.exceptions import ValidationError
# from django.utils.timezone import now
# from datetime import timedelta, datetime
# from django.utils.text import slugify
# from schedule.models import Calendar
# from rest_framework.exceptions import PermissionDenied
# from rest_framework import filters


# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     # permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['name', 'category__name']
#     ordering_fields = ['price', 'duration']
    
# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer
#     # permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         user = self.request.user
#         if Staff.objects.filter(staff=user).exists():
#             raise ValidationError("Already registered as staff.")
#         cal_name = f"{user.username} Calendar"
#         base = slugify(cal_name)
#         slug = base
#         i = 1
#         while Calendar.objects.filter(slug=slug).exists():
#             slug = f"{base}-{i}"
#             i += 1
#         cal = Calendar.objects.create(name=cal_name, slug=slug)
#         serializer.save(staff=user, calendar=cal)

#     @action(detail=True, methods=['get'])
#     def availability(self, request, pk=None):
#         staff = self.get_object()
#         date_str = request.query_params.get('date')
#         dur = request.query_params.get('duration', 60)
#         try:
#             d = datetime.strptime(date_str, '%Y-%m-%d').date()
#             td = timedelta(minutes=int(dur))
#         except:
#             return Response({'error': 'Invalid date or duration format'}, status=status.HTTP_400_BAD_REQUEST)
#         slots = staff.get_available_slots(d, td)
#         return Response({'date': date_str, 'duration': td.total_seconds()/60, 'available_slots': [t.strftime('%H:%M') for t in slots]})

# class AppointmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AppointmentSerializer
#     # permission_classes = [IsAuthenticated]

#     # def get_queryset(self):
#     #     user = self.request.user
#     #     if user.is_staff:
#     #         return Appointment.objects.filter(staff__staff=user)
#     #     return Appointment.objects.filter(client=user)

#     def get_queryset(self):
#         user = self.request.user

#         # If user is a superuser (admin), show all appointments
#         if user.is_superuser:
#             return Appointment.objects.all()

#         # If user is linked to a Staff model
#         if Staff.objects.filter(staff=user).exists():
#             staff_instance = Staff.objects.get(staff=user)
#             # Filter appointments assigned to this staff member
#             # and only those that include services they provide
#             staff_services = staff_instance.services.all()
#             return Appointment.objects.filter(
#                 staff=staff_instance,
#                 services__in=staff_services
#             ).distinct()

#         # Else, user is a client - show only their own appointments
#         return Appointment.objects.filter(client=user)
#     def create(self, request, *args, **kwargs):
#         user = request.user

#         # Block superusers and staff from booking appointments
#         if user.is_superuser or Staff.objects.filter(staff=user).exists():
#             raise PermissionDenied("Only clients can book appointments.")

#         return super().create(request, *args, **kwargs)
#     def list(self, request, *args, **kwargs):
#         if 'date' in request.query_params and 'services' in request.query_params:
#             slot_ser = AvailableSlotSerializer(data=request.query_params)
#             slot_ser.is_valid(raise_exception=True)
#             return Response(slot_ser.data)
#         return super().list(request, *args, **kwargs)

#     @action(detail=True, methods=['post'])
#     def cancel(self, request, pk=None):
#         appt = self.get_object()
#         if appt.status == 'cancelled':
#             return Response({'status': 'Already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
#         appt.status = 'cancelled'
#         appt.save()
#         Event.objects.filter(calendar=appt.staff.calendar, start=appt.start_time, end=appt.end_time).delete()
#         return Response({'status': 'cancelled'})

#     @action(detail=False, methods=['get'])
#     def upcoming(self, request):
#         qs = self.get_queryset().filter(start_time__gte=now(), status__in=['confirmed','pending']).order_by('start_time')
#         ser = self.get_serializer(qs, many=True)
#         return Response(ser.data)

# class AvailableSlotsView(viewsets.ViewSet):
#     # permission_classes = [IsAuthenticated]

#     def list(self, request):
#         ser = AvailableSlotSerializer(data=request.query_params)
#         ser.is_valid(raise_exception=True)
#         return Response(ser.data)
    
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
# --------------------------------------------------------------Better-above-code---------------------------------------------------------------

# from rest_framework import viewsets, status, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Service, Staff, Appointment, Category
# from .serializers import (
#     ServiceSerializer,
#     StaffSerializer,
#     AppointmentSerializer,
#     AvailableSlotSerializer,
#     CategorySerializer,
# )
# from rest_framework.exceptions import ValidationError, PermissionDenied
# from django.utils.timezone import now
# from datetime import timedelta, datetime
# from django.utils.text import slugify
# from schedule.models import Calendar, Event

# # class ServiceViewSet(viewsets.ModelViewSet):
# #     queryset = Service.objects.all()
# #     serializer_class = ServiceSerializer
# #     permission_classes = [IsAuthenticated]
# #     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
# #     search_fields = ['name', 'category_name', 'description']
# #     ordering_fields = ['price', 'duration', 'name','category',]

# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, filters.DjangoFilterBackend]  # Add DjangoFilterBackend
#     search_fields = ['name', 'category_name', 'description']
#     ordering_fields = ['price', 'duration', 'name', 'category']
#     filterset_fields = ['category']  # Add this line to enable category filtering


# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, filters.DjangoFilterBackend] 
#     search_fields = ['username', 'services']
#     ordering_fields = ['username', 'buffer_time', 'services']
#     filterset_fields = ['services']

#     def perform_create(self, serializer):
#         user = self.request.user
#         if Staff.objects.filter(staff=user).exists():
#             raise ValidationError("Already registered as staff.")
#         cal_name = f"{user.username} Calendar"
#         base = slugify(cal_name)
#         slug = base
#         i = 1
#         while Calendar.objects.filter(slug=slug).exists():
#             slug = f"{base}-{i}"
#             i += 1
#         cal = Calendar.objects.create(name=cal_name, slug=slug)
#         serializer.save(staff=user, calendar=cal)

#     @action(detail=True, methods=['get'])
#     def availability(self, request, pk=None):
#         staff = self.get_object()
#         date_str = request.query_params.get('date')
#         dur = request.query_params.get('duration', 60)
#         try:
#             d = datetime.strptime(date_str, '%Y-%m-%d').date()
#             td = timedelta(minutes=int(dur))
#         except:
#             return Response({'error': 'Invalid date or duration format'}, status=status.HTTP_400_BAD_REQUEST)
#         slots = staff.get_available_slots(d, td)
#         return Response({
#             'date': date_str,
#             'duration': td.total_seconds() / 60,
#             'available_slots': [t.strftime('%H:%M') for t in slots]
#         })

# class AppointmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AppointmentSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, filters.DjangoFilterBackend] 
#     search_fields = ['username', 'staff', 'services', 'status']
#     ordering_fields = ['start_time', 'end_time', 'created_at', 'staff', 'services', 'status']
#     filterset_fields = ['services', 'staff', 'status']

#     def get_queryset(self):
#         user = self.request.user

#         if user.is_superuser:
#             return Appointment.objects.all()

#         if Staff.objects.filter(staff=user).exists():
#             staff_instance = Staff.objects.get(staff=user)
#             staff_services = staff_instance.services.all()
#             return Appointment.objects.filter(
#                 staff=staff_instance,
#                 services__in=staff_services
#             ).distinct()

#         return Appointment.objects.filter(client=user)

#     def create(self, request, *args, **kwargs):
#         user = request.user
#         if user.is_superuser or Staff.objects.filter(staff=user).exists():
#             raise PermissionDenied("Only clients can book appointments.")
#         return super().create(request, *args, **kwargs)

#     def list(self, request, *args, **kwargs):
#         if 'date' in request.query_params and 'services' in request.query_params:
#             slot_ser = AvailableSlotSerializer(data=request.query_params)
#             slot_ser.is_valid(raise_exception=True)
#             return Response(slot_ser.data)
#         return super().list(request, *args, **kwargs)

#     @action(detail=True, methods=['post'])
#     def cancel(self, request, pk=None):
#         appt = self.get_object()
#         if appt.status == 'cancelled':
#             return Response({'status': 'Already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
#         appt.status = 'cancelled'
#         appt.save()
#         Event.objects.filter(calendar=appt.staff.calendar, start=appt.start_time, end=appt.end_time).delete()
#         return Response({'status': 'cancelled'})

#     @action(detail=False, methods=['get'])
#     def upcoming(self, request):
#         qs = self.get_queryset().filter(
#             start_time__gte=now(),
#             status__in=['confirmed', 'pending']
#         ).order_by('start_time')
#         ser = self.get_serializer(qs, many=True)
#         return Response(ser.data)

# class AvailableSlotsView(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     def list(self, request):
#         ser = AvailableSlotSerializer(data=request.query_params)
#         ser.is_valid(raise_exception=True)
#         return Response(ser.data)

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, filters.DjangoFilterBackend] 
#     search_fields = ['name']
#     ordering_fields = ['name']
#     filterset_fields = ['name']

# from rest_framework import viewsets, status, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Service, Staff, Appointment, Category
# from .serializers import (ServiceSerializer,StaffSerializer,AppointmentSerializer,AvailableSlotSerializer,CategorySerializer,)
# from rest_framework.exceptions import ValidationError, PermissionDenied
# from django.utils.timezone import now
# from datetime import timedelta, datetime
# from django.utils.text import slugify
# from schedule.models import Calendar, Event
# from django.db.models import Prefetch

# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.select_related('category').all()
#     serializer_class = ServiceSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['name', 'description']
#     ordering_fields = ['price', 'duration', 'name', 'category__name']
#     filterset_fields = {
#         'category': ['exact', 'isnull'],
#         'price': ['exact', 'gte', 'lte'],
#     }

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         # Additional custom filtering if needed
#         return queryset

# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.select_related(
#         'staff', 
#         'calendar'
#     ).prefetch_related(
#         Prefetch('services', queryset=Service.objects.select_related('category'))
#     ).all()
#     serializer_class = StaffSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['staff__username', 'staff__first_name', 'staff__last_name']
#     ordering_fields = ['staff__username', 'buffer_time']
#     filterset_fields = {
#         'services': ['exact', 'in'],
#         'staff__is_active': ['exact'],
#     }

#     def perform_create(self, serializer):
#         user = self.request.user
#         if Staff.objects.filter(staff=user).exists():
#             raise ValidationError("Already registered as staff.")
        
#         cal_name = f"{user.username} Calendar"
#         base = slugify(cal_name)
#         slug = base
#         i = 1
#         while Calendar.objects.filter(slug=slug).exists():
#             slug = f"{base}-{i}"
#             i += 1
            
#         cal = Calendar.objects.create(name=cal_name, slug=slug)
#         serializer.save(staff=user, calendar=cal)

#     @action(detail=True, methods=['get'])
#     def availability(self, request, pk=None):
#         staff = self.get_object()
#         date_str = request.query_params.get('date')
#         dur = request.query_params.get('duration', 60)
        
#         if not date_str:
#             return Response(
#                 {'error': 'Date parameter is required'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             d = datetime.strptime(date_str, '%Y-%m-%d').date()
#             td = timedelta(minutes=int(dur))
#         except (ValueError, TypeError) as e:
#             return Response(
#                 {'error': f'Invalid format: {str(e)}'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         slots = staff.get_available_slots(d, td)
#         return Response({
#             'date': date_str,
#             'duration': td.total_seconds() / 60,
#             'available_slots': [t.strftime('%H:%M') for t in slots]
#         })

# class AppointmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AppointmentSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['client__username', 'staff__staff__username','services__name','status']
#     ordering_fields = ['start_time', 'end_time', 'created_at', 'staff__staff__username','status']
#     filterset_fields = {'services': ['exact', 'in'],'staff': ['exact'],'status': ['exact', 'in'],'start_time': ['gte', 'lte', 'date'],'client': ['exact'],}

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Appointment.objects.select_related('client','staff','staff__staff','staff__calendar').prefetch_related('services','services__category').order_by('-start_time')

#         if user.is_superuser:
#             return queryset

#         if Staff.objects.filter(staff=user).exists():
#             staff_instance = Staff.objects.get(staff=user)
#             return queryset.filter(staff=staff_instance)

#         return queryset.filter(client=user)

#     def create(self, request, *args, **kwargs):
#         user = request.user
#         if user.is_superuser or Staff.objects.filter(staff=user).exists():
#             raise PermissionDenied("Only clients can book appointments.")
#         return super().create(request, *args, **kwargs)

#     def list(self, request, *args, **kwargs):
#         if 'date' in request.query_params and 'services' in request.query_params:
#             slot_ser = AvailableSlotSerializer(data=request.query_params)
#             slot_ser.is_valid(raise_exception=True)
#             return Response(slot_ser.data)
#         return super().list(request, *args, **kwargs)

#     @action(detail=True, methods=['post'])
#     def cancel(self, request, pk=None):
#         appt = self.get_object()
#         if appt.status == 'cancelled':
#             return Response(
#                 {'status': 'Already cancelled'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         appt.status = 'cancelled'
#         appt.save()
#         Event.objects.filter(
#             calendar=appt.staff.calendar, 
#             start=appt.start_time, 
#             end=appt.end_time
#         ).delete()
#         return Response({'status': 'cancelled'})

#     @action(detail=False, methods=['get'])
#     def upcoming(self, request):
#         qs = self.get_queryset().filter(
#             start_time__gte=now(),
#             status__in=['confirmed', 'pending']
#         ).order_by('start_time')
#         ser = self.get_serializer(qs, many=True)
#         return Response(ser.data)

# class AvailableSlotsView(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     def list(self, request):
#         ser = AvailableSlotSerializer(data=request.query_params)
#         ser.is_valid(raise_exception=True)
#         return Response(ser.data)

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.prefetch_related('subcategories').all()
#     serializer_class = CategorySerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['name']
#     ordering_fields = ['name']
#     filterset_fields = {
#         'parent': ['exact', 'isnull'],
#     }

# from rest_framework import viewsets, status, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend
# from django.db.models import Prefetch, Q
# from django.utils.timezone import now
# from datetime import timedelta, datetime
# from django.utils.text import slugify
# from schedule.models import Calendar, Event
# from .models import Service, Staff, Appointment, Category
# from .serializers import (
#     ServiceSerializer,
#     StaffSerializer,
#     AppointmentSerializer,
#     AvailableSlotSerializer,
#     CategorySerializer,
# )
# from rest_framework.exceptions import ValidationError, PermissionDenied

# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.select_related('category').filter(is_active=True)
#     serializer_class = ServiceSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['name', 'description']
#     ordering_fields = ['price', 'duration', 'name', 'category__name']
#     filterset_fields = {
#         'category': ['exact', 'isnull'],
#         'price': ['exact', 'gte', 'lte'],
#     }

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         category_id = self.request.query_params.get('category_id')
#         if category_id:
#             queryset = queryset.filter(category_id=category_id)
#         return queryset.order_by('display_order', 'name')

# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.select_related(
#         'staff', 
#         'calendar'
#     ).prefetch_related(
#         Prefetch('services', queryset=Service.objects.filter(is_active=True))
#     ).filter(is_active=True)
#     serializer_class = StaffSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['staff__username', 'staff__first_name', 'staff__last_name']
#     ordering_fields = ['staff__username', 'buffer_time']
#     filterset_fields = {
#         'services': ['exact', 'in'],
#         'staff__is_active': ['exact'],
#     }

#     def perform_create(self, serializer):
#         user = self.request.user
#         if Staff.objects.filter(staff=user).exists():
#             raise ValidationError("Already registered as staff.")
        
#         cal_name = f"{user.get_full_name() or user.username}'s Calendar"
#         base = slugify(cal_name)
#         slug = base
#         i = 1
#         while Calendar.objects.filter(slug=slug).exists():
#             slug = f"{base}-{i}"
#             i += 1
            
#         cal = Calendar.objects.create(name=cal_name, slug=slug)
#         serializer.save(staff=user, calendar=cal)

#     @action(detail=True, methods=['get'])
#     def availability(self, request, pk=None):
#         staff = self.get_object()
#         date_str = request.query_params.get('date')
#         dur = request.query_params.get('duration', 60)
        
#         if not date_str:
#             return Response(
#                 {'error': 'Date parameter is required'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             d = datetime.strptime(date_str, '%Y-%m-%d').date()
#             td = timedelta(minutes=int(dur))
#         except (ValueError, TypeError) as e:
#             return Response(
#                 {'error': f'Invalid format: {str(e)}'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         slots = staff.get_available_slots(d, td)
#         return Response({
#             'date': date_str,
#             'duration': td.total_seconds() / 60,
#             'available_slots': [t.strftime('%H:%M') for t in slots]
#         })

# class AppointmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AppointmentSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['client__username', 'staff__staff__username', 'services__name', 'status']
#     ordering_fields = ['start_time', 'end_time', 'created_at', 'staff__staff__username', 'status']
#     filterset_fields = {
#         'services': ['exact', 'in'],
#         'staff': ['exact'],
#         'status': ['exact', 'in'],
#         'start_time': ['gte', 'lte', 'date'],
#         'client': ['exact'],
#     }

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Appointment.objects.select_related(
#             'client',
#             'staff',
#             'staff__staff',
#             'staff__calendar'
#         ).prefetch_related(
#             'services',
#             'services__category'
#         ).order_by('-start_time')

#         if user.is_superuser:
#             return queryset

#         if hasattr(user, 'staff_profile'):
#             staff_instance = user.staff_profile
#             return queryset.filter(staff=staff_instance)

#         return queryset.filter(client=user)

#     def create(self, request, *args, **kwargs):
#         user = request.user
#         if user.is_superuser or hasattr(user, 'staff_profile'):
#             raise PermissionDenied("Only clients can book appointments.")
        
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         # Check if the selected time slot is still available
#         staff_id = serializer.validated_data.get('staff_id')
#         start_time = serializer.validated_data.get('start_time')
#         services = serializer.validated_data.get('services')
        
#         if not services:
#             raise ValidationError({'services': 'At least one service is required'})
            
#         total_duration = sum((s.duration for s in services), timedelta())
#         end_time = start_time + total_duration
        
#         staff = Staff.objects.get(id=staff_id)
#         if not staff.is_available(start_time, total_duration):
#             raise ValidationError({'non_field_errors': ['The selected time slot is no longer available.']})
            
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     @action(detail=True, methods=['post'])
#     def cancel(self, request, pk=None):
#         appt = self.get_object()
#         if appt.status == 'cancelled':
#             return Response(
#                 {'status': 'Already cancelled'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         reason = request.data.get('reason', '')
#         appt.cancel(reason)
#         return Response({'status': 'cancelled'})

#     @action(detail=False, methods=['get'])
#     def upcoming(self, request):
#         qs = self.get_queryset().filter(
#             start_time__gte=now(),
#             status__in=['confirmed', 'pending']
#         ).order_by('start_time')
#         ser = self.get_serializer(qs, many=True)
#         return Response(ser.data)

#     @action(detail=False, methods=['get'])
#     def available_staff(self, request):
#         date_str = request.query_params.get('date')
#         service_ids = request.query_params.getlist('services')
        
#         if not date_str or not service_ids:
#             return Response(
#                 {'error': 'Both date and services parameters are required'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         try:
#             date = datetime.strptime(date_str, '%Y-%m-%d').date()
#             services = Service.objects.filter(id__in=service_ids)
#             total_duration = sum((s.duration for s in services), timedelta())
            
#             staff_list = []
#             for staff in Staff.objects.filter(services__in=services).distinct():
#                 slots = staff.get_available_slots(date, total_duration)
#                 if slots:
#                     staff_list.append({
#                         'id': staff.id,
#                         'name': staff.staff.get_full_name() or staff.staff.username,
#                         'available_slots': [s.strftime('%H:%M') for s in slots]
#                     })
                    
#             return Response({
#                 'date': date_str,
#                 'services': [s.id for s in services],
#                 'staff': staff_list
#             })
#         except Exception as e:
#             return Response(
#                 {'error': str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.prefetch_related('subcategories').all()
#     serializer_class = CategorySerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['name']
#     ordering_fields = ['name']
#     filterset_fields = {
#         'parent': ['exact', 'isnull'],
#     }

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(parent__isnull=True).order_by('display_order', 'name')

#     @action(detail=True, methods=['get'])
#     def services(self, request, pk=None):
#         category = self.get_object()
#         services = category.services.filter(is_active=True).order_by('display_order', 'name')
#         serializer = ServiceSerializer(services, many=True)
#         return Response(serializer.data)


# from rest_framework import viewsets, status, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend
# from django.utils.timezone import now
# from django.utils.text import slugify
# from rest_framework.exceptions import ValidationError, PermissionDenied
# from schedule.models import Calendar, Event
# from datetime import datetime, timedelta
# from .models import Service, Staff, Appointment, Category
# from .serializers import (ServiceSerializer,StaffSerializer,AppointmentSerializer,AvailableSlotSerializer,CategorySerializer,)

# from django.utils import timezone
# print("Current timezone:", timezone.get_current_timezone_name())

# class ServiceViewSet(viewsets.ModelViewSet):
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['name', 'category_name', 'description']
#     ordering_fields = ['price', 'duration', 'name', 'category']
#     filterset_fields = ['category']

# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['username', 'services__name']
#     ordering_fields = ['username', 'buffer_time', 'services']
#     filterset_fields = ['services']

#     def perform_create(self, serializer):
#         user = self.request.user
#         if Staff.objects.filter(staff=user).exists():
#             raise ValidationError("Already registered as staff.")
#         cal_name = f"{user.username} Calendar"
#         base = slugify(cal_name)
#         slug = base
#         i = 1
#         while Calendar.objects.filter(slug=slug).exists():
#             slug = f"{base}-{i}"
#             i += 1
#         cal = Calendar.objects.create(name=cal_name, slug=slug)
#         serializer.save(staff=user, calendar=cal)

#     @action(detail=True, methods=['get'])
#     def availability(self, request, pk=None):
#         staff = self.get_object()
#         date_str = request.query_params.get('date')
#         dur = request.query_params.get('duration', 60)

#         try:
#             d = datetime.strptime(date_str, '%Y-%m-%d').date()
#             td = timedelta(minutes=int(dur))
#         except:
#             return Response({'error': 'Invalid date or duration format'}, status=status.HTTP_400_BAD_REQUEST)

#         slots = staff.get_available_slots(d, td)
#         return Response({
#             'date': date_str,
#             'duration': td.total_seconds() / 60,
#             'available_slots': [t.strftime('%H:%M') for t in slots]
#         })

# class AppointmentViewSet(viewsets.ModelViewSet):
#     serializer_class = AppointmentSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['client__username', 'staff__username', 'services__name', 'status']
#     ordering_fields = ['start_time', 'end_time', 'created_at', 'staff', 'services', 'status']
#     filterset_fields = ['services', 'staff', 'status']

#     def get_queryset(self):
#         user = self.request.user

#         if user.is_superuser:
#             return Appointment.objects.all()

#         if Staff.objects.filter(staff=user).exists():
#             staff_instance = Staff.objects.get(staff=user)
#             return Appointment.objects.filter(staff=staff_instance).distinct()

#         return Appointment.objects.filter(client=user)

#     def create(self, request, *args, **kwargs):
#         user = request.user
#         if user.is_superuser or Staff.objects.filter(staff=user).exists():
#             raise PermissionDenied("Only clients can book appointments.")
#         return super().create(request, *args, **kwargs)

#     def list(self, request, *args, **kwargs):
#         if 'date' in request.query_params and 'services' in request.query_params:
#             slot_ser = AvailableSlotSerializer(data=request.query_params)
#             slot_ser.is_valid(raise_exception=True)
#             return Response(slot_ser.data)
#         return super().list(request, *args, **kwargs)

#     @action(detail=True, methods=['post'])
#     def cancel(self, request, pk=None):
#         appt = self.get_object()
#         if appt.status == 'cancelled':
#             return Response({'status': 'Already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
#         appt.status = 'cancelled'
#         appt.save()
#         Event.objects.filter(calendar=appt.staff.calendar, start=appt.start_time, end=appt.end_time).delete()
#         return Response({'status': 'cancelled'})

#     @action(detail=False, methods=['get'])
#     def upcoming(self, request):
#         qs = self.get_queryset().filter(
#             start_time__gte=now(),
#             status__in=['confirmed', 'pending']
#         ).order_by('start_time')
#         ser = self.get_serializer(qs, many=True)
#         return Response(ser.data)

# class AvailableSlotsView(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     def list(self, request):
#         ser = AvailableSlotSerializer(data=request.query_params)
#         ser.is_valid(raise_exception=True)
#         return Response(ser.data)

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     search_fields = ['name']
#     ordering_fields = ['name']
#     filterset_fields = ['name']

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from pytz import timezone as pytz_timezone
from rest_framework.exceptions import ValidationError, PermissionDenied
from schedule.models import Calendar, Event
from datetime import datetime, timedelta
from django.utils.text import slugify

from .models import Service, Staff, Appointment, Category
from .serializers import (
    ServiceSerializer, StaffSerializer, AppointmentSerializer,
    AvailableSlotSerializer, CategorySerializer
)

INDIAN_TZ = pytz_timezone('Asia/Kolkata')


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'category_name', 'description']
    ordering_fields = ['price', 'duration', 'name', 'category']
    filterset_fields = ['category']


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['username', 'services__name']
    ordering_fields = ['username', 'buffer_time', 'services']
    filterset_fields = ['services']

    def perform_create(self, serializer):
        user = self.request.user
        if Staff.objects.filter(staff=user).exists():
            raise ValidationError("Already registered as staff.")
        cal_name = f"{user.username} Calendar"
        base = slugify(cal_name)
        slug = base
        i = 1
        while Calendar.objects.filter(slug=slug).exists():
            slug = f"{base}-{i}"
            i += 1
        cal = Calendar.objects.create(name=cal_name, slug=slug)
        serializer.save(staff=user, calendar=cal)

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        staff = self.get_object()
        date_str = request.query_params.get('date')
        dur = request.query_params.get('duration', 60)

        try:
            d = datetime.strptime(date_str, '%Y-%m-%d').date()
            td = timedelta(minutes=int(dur))
        except:
            return Response({'error': 'Invalid date or duration format'}, status=status.HTTP_400_BAD_REQUEST)

        slots = staff.get_available_slots(d, td)
        return Response({
            'date': date_str,
            'duration': td.total_seconds() / 60,
            'available_slots': [t.astimezone(INDIAN_TZ).strftime('%H:%M') for t in slots]
        })


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['client__username', 'staff__username', 'services__name', 'status']
    ordering_fields = ['start_time', 'end_time', 'created_at', 'staff', 'services', 'status']
    filterset_fields = ['services', 'staff', 'status']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Appointment.objects.all()

        if Staff.objects.filter(staff=user).exists():
            staff_instance = Staff.objects.get(staff=user)
            return Appointment.objects.filter(staff=staff_instance).distinct()

        return Appointment.objects.filter(client=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser or Staff.objects.filter(staff=user).exists():
            raise PermissionDenied("Only clients can book appointments.")
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if 'date' in request.query_params and 'services' in request.query_params:
            slot_ser = AvailableSlotSerializer(data=request.query_params)
            slot_ser.is_valid(raise_exception=True)
            return Response(slot_ser.data)
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appt = self.get_object()
        if appt.status == 'cancelled':
            return Response({'status': 'Already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        appt.status = 'cancelled'
        appt.save()
        Event.objects.filter(calendar=appt.staff.calendar, start=appt.start_time, end=appt.end_time).delete()
        return Response({'status': 'cancelled'})

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        qs = self.get_queryset().filter(
            start_time__gte=timezone.now().astimezone(INDIAN_TZ),
            status__in=['confirmed', 'pending']
        ).order_by('start_time')
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)


class AvailableSlotsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        ser = AvailableSlotSerializer(data=request.query_params)
        ser.is_valid(raise_exception=True)
        return Response(ser.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['name']
    filterset_fields = ['name']
