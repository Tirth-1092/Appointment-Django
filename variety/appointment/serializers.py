
# from rest_framework import serializers
# from .models import Service, Staff, Appointment
# from django.contrib.auth import get_user_model
# from datetime import timedelta, time
# from .tasks import send_appointment_reminder

# User = get_user_model()

# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = '__all__'


# class StaffSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Staff
#         fields = '__all__'

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['is_employee'] = instance.is_employee
#         data['services'] = [service.name for service in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data


# class AppointmentSerializer(serializers.ModelSerializer):
#     services = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Service.objects.all()
#     )

#     class Meta:
#         model = Appointment
#         fields = ['id', 'client', 'services', 'staff', 'start_time', 'end_time']
#         read_only_fields = ['client', 'staff', 'end_time']

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['client_username'] = instance.client.username
#         data['services'] = [service.name for service in instance.services.all()]
#         data['staff_username'] = instance.staff.staff.username
#         data['start_time'] = instance.start_time.strftime('%Y-%m-%d %H:%M')
#         data['end_time'] = instance.end_time.strftime('%Y-%m-%d %H:%M')
#         return data

#     def validate(self, data):
#         services = data.get('services', [])
#         start_time = data.get('start_time')

#         if not services:
#             raise serializers.ValidationError("At least one service must be selected.")

#         # Enforce 9 AM - 9 PM booking range
#         if not (time(9, 0) <= start_time.time() <= time(21, 0)):
#             raise serializers.ValidationError("Appointments can only be booked between 9:00 AM and 9:00 PM.")

#         # Calculate total duration
#         total_duration = sum([s.duration for s in services], timedelta())
#         end_time = start_time + total_duration

#         # Auto-assign available staff who can perform all selected services
#         available_staff = None
#         for staff in Staff.objects.all():
#             staff_services = staff.services.all()
#             if all(service in staff_services for service in services):
#                 if staff.is_available(start_time, total_duration):
#                     available_staff = staff
#                     break

#         if not available_staff:
#             raise serializers.ValidationError("No available staff found for the selected time and services.")

#         data['staff'] = available_staff
#         data['end_time'] = end_time
#         return data

#     def create(self, validated_data):
#         services = validated_data.pop('services')
#         appointment = Appointment.objects.create(**validated_data)
#         appointment.services.set(services)

#         # Schedule reminders: 24 hrs and 1 hr before appointment
#         send_appointment_reminder.apply_async((appointment.id,), eta=appointment.start_time - timedelta(hours=24))
#         send_appointment_reminder.apply_async((appointment.id,), eta=appointment.start_time - timedelta(hours=1))

#         return appointment

# from rest_framework import serializers
# from .models import Service, Staff, Appointment


# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = '__all__'


# class StaffSerializer(serializers.ModelSerializer):
#     services = ServiceSerializer(many=True, read_only=True)
#     class Meta:
#         model = Staff
#         fields = ['id', 'staff', 'services', 'calendar']


# class AppointmentSerializer(serializers.ModelSerializer):
#     services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)

#     class Meta:
#         model = Appointment
#         fields = ['id',  'services', 'staff', 'start_time', 'end_time']
#         read_only_fields = ['end_time']
    
#     def create(self, validated_data):
#         services = validated_data.pop('services')
#         appointment = Appointment.objects.create(**validated_data)
#         appointment.services.set(services)  # Now it's safe, ID exists
#         return appointment

# # serializers.py
# from rest_framework import serializers
# from .models import Service, Staff, Appointment
# from django.utils.timezone import make_aware
# from datetime import datetime, timedelta


# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = '__all__'


# class StaffSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Staff
#         fields = '__all__'

    
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['is_employee'] = instance.is_employee
#         data['services'] = [service.name for service in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data



# class AppointmentSerializer(serializers.ModelSerializer):
#     services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)

#     class Meta:
#         model = Appointment
#         fields = ['id','services', 'staff', 'start_time', 'end_time']
#         read_only_fields = ['staff', 'end_time']

#     def validate_start_time(self, value):
#         # Ensure start_time is aware
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if not (value.time() >= datetime.strptime("09:00", "%H:%M").time() and value.time() <= datetime.strptime("21:00", "%H:%M").time()):
#             raise serializers.ValidationError("Appointments can only be booked between 9:00 AM and 9:00 PM")
#         return value

#     def create(self, validated_data):
#         request = self.context['request']
#         user = request.user
#         services = validated_data.pop('services')
#         start_time = validated_data['start_time']
#         total_duration = sum([s.duration for s in services], timedelta())

#         # Automatically assign available staff
#         available_staff = None
#         for staff in Staff.objects.all():
#             if all(s in staff.services.all() for s in services) and staff.is_available(start_time, total_duration):
#                 available_staff = staff
#                 break

#         if not available_staff:
#             raise serializers.ValidationError("No available staff for the selected services and time.")

#         appointment = Appointment.objects.create(
#             client=user,
#             staff=available_staff,
#             start_time=start_time
#         )
#         appointment.services.set(services)
#         appointment.save()
#         return appointment
#----------------------------------------
# from rest_framework import serializers
# from .models import Service, Staff, Appointment
# from django.utils.timezone import make_aware
# from datetime import datetime, timedelta, time


# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = '__all__'


# # class StaffSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Staff
# #         fields = '__all__'

# #     def to_representation(self, instance):
# #         data = super().to_representation(instance)
# #         data['staff_username'] = instance.staff.username
# #         data['services'] = [s.name for s in instance.services.all()]
# #         return data

# class StaffSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Staff
#         exclude = ['calendar']  # exclude calendar from input
#         read_only_fields = ['staff']
        
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data


# class AppointmentSerializer(serializers.ModelSerializer):
#     services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
#     end_time = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Appointment
#         fields = ['id', 'services', 'staff', 'start_time', 'end_time']
#         read_only_fields = ['staff', 'end_time']

#     def get_end_time(self, obj):
#         return obj.end_time

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if not (time(9, 0) <= value.time() <= time(21, 0)):
#             raise serializers.ValidationError("Start time must be between 9:00 AM and 9:00 PM")
#         return value

#     def create(self, validated_data):
#         user = self.context['request'].user
#         services = validated_data.pop('services')
#         start_time = validated_data['start_time']
#         total_duration = sum((s.duration for s in services), timedelta())

#         # Auto-assign available staff
#         for staff in Staff.objects.all():
#             if all(s in staff.services.all() for s in services) and staff.is_available(start_time, total_duration):
#                 appointment = Appointment.objects.create(
#                     client=user,
#                     staff=staff,
#                     start_time=start_time
#                 )
#                 appointment.services.set(services)
#                 appointment.save()
#                 return appointment

#         raise serializers.ValidationError("No available staff for selected services and time.")

# from rest_framework import serializers
# from schedule.models import Event
# from .models import Service, Staff, Appointment
# from django.utils.timezone import make_aware
# from datetime import datetime, timedelta, time


# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = '__all__'


# class StaffSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Staff
#         exclude = ['calendar']
#         read_only_fields = ['staff']

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data


# class AppointmentSerializer(serializers.ModelSerializer):
#     services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
#     end_time = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = ['id', 'services', 'staff', 'start_time', 'end_time']
#         read_only_fields = ['staff', 'end_time']

#     def get_end_time(self, obj):
#         return obj.end_time

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if not (time(9, 0) <= value.time() <= time(21, 0)):
#             raise serializers.ValidationError("Start time must be between 9:00 AM and 9:00 PM")
#         return value

#     def create(self, validated_data):
#         user = self.context['request'].user
#         services = validated_data.pop('services')
#         start_time = validated_data['start_time']
#         total_duration = sum((s.duration for s in services), timedelta())

#         for staff in Staff.objects.all():
#             if all(s in staff.services.all() for s in services) and staff.is_available(start_time, total_duration):
#                 appointment = Appointment.objects.create(
#                     client=user,
#                     staff=staff,
#                     start_time=start_time
#                 )
#                 appointment.services.set(services)
#                 appointment.save()
#                 return appointment

#             raise serializers.ValidationError("No available staff for selected services and time.")


# class AvailableSlotSerializer(serializers.ModelSerializer):
#     staff = serializers.SerializerMethodField()

#     class Meta:
#         model = Event
#         fields = ['id', 'title', 'start', 'end', 'staff']
#         read_only_fields = ['staff', 'title']

#     def get_staff(self, obj):
#         try:
#             staff = Staff.objects.get(calendar=obj.calendar)
#             return staff.staff.username
#         except Staff.DoesNotExist:
#             return None

#     def create(self, validated_data):
#         user = self.context['request'].user
#         try:
#             staff = Staff.objects.get(staff=user)
#             return Event.objects.create(
#                 title=f"{user.username}'s Available Slot",
#                 calendar=staff.calendar,
#                 **validated_data
#             )
#         except Staff.DoesNotExist:
#             raise serializers.ValidationError("You're not registered as staff.")


# from rest_framework import serializers
# from schedule.models import Event
# from .models import Service, Staff, Appointment
# from django.utils.timezone import make_aware
# from datetime import timedelta, time


# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = '__all__'


# class StaffSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Staff
#         exclude = ['calendar']
#         read_only_fields = ['staff']

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data


# class AppointmentSerializer(serializers.ModelSerializer):
#     services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
#     end_time = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = ['id', 'services', 'staff', 'start_time', 'end_time']
#         read_only_fields = ['staff', 'end_time']

#     def get_end_time(self, obj):
#         return obj.end_time

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if not (time(9, 0) <= value.time() <= time(21, 0)):
#             raise serializers.ValidationError("Start time must be between 9:00 AM and 9:00 PM")
#         return value

#     def create(self, validated_data):
#         user = self.context['request'].user
#         services = validated_data.pop('services')
#         start_time = validated_data['start_time']
#         total_duration = sum((s.duration for s in services), timedelta())

#         print("⏱️ Total Duration:", total_duration)
#         print("🕐 Start Time:", start_time)

#         for staff in Staff.objects.all():
#             staff_services = list(staff.services.all())
#             has_all_services = all(s in staff_services for s in services)
#             is_available = staff.is_available(start_time, total_duration)

#             print(f"👤 Staff: {staff.staff.username}")
#             print(f"   📦 Has All Services: {has_all_services}")
#             print(f"   ✅ Is Available: {is_available}")

#             if has_all_services and is_available:
#                 appointment = Appointment.objects.create(
#                     client=user,
#                     staff=staff,
#                     start_time=start_time
#                 )
#                 appointment.services.set(services)
#                 appointment.save()
#                 return appointment

#         raise serializers.ValidationError("No available staff for selected services and time.")


# class AvailableSlotSerializer(serializers.ModelSerializer):
#     staff = serializers.SerializerMethodField()

#     class Meta:
#         model = Event
#         fields = ['id', 'title', 'start', 'end', 'staff']
#         read_only_fields = ['staff', 'title']

#     def get_staff(self, obj):
#         try:
#             staff = Staff.objects.get(calendar=obj.calendar)
#             return staff.staff.username
#         except Staff.DoesNotExist:
#             return None

#     def create(self, validated_data):
#         user = self.context['request'].user
#         from .models import Staff
#         try:
#             staff = Staff.objects.get(staff=user)
#             return Event.objects.create(
#                 title=f"{user.username}'s Available Slot",
#                 calendar=staff.calendar,
#                 **validated_data
#             )
#         except Staff.DoesNotExist:
#             raise serializers.ValidationError("You're not registered as staff.")


# from rest_framework import serializers
# from schedule.models import Event
# from .models import Service, Staff, Appointment
# from django.utils.timezone import make_aware
# from datetime import timedelta, time


# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = '__all__'


# class StaffSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Staff
#         exclude = ['calendar']
#         read_only_fields = ['staff']

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data


# class AppointmentSerializer(serializers.ModelSerializer):
#     services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
#     end_time = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = ['id', 'services', 'staff', 'start_time', 'end_time']
#         read_only_fields = ['staff', 'end_time']

#     def get_end_time(self, obj):
#         return obj.end_time

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if not (time(9, 0) <= value.time() <= time(21, 0)):
#             raise serializers.ValidationError("Start time must be between 9:00 AM and 9:00 PM")
#         return value

#     def create(self, validated_data):
#         user = self.context['request'].user
#         services = validated_data.pop('services')
#         start_time = validated_data['start_time']
#         total_duration = sum((s.duration for s in services), timedelta())

#         for staff in Staff.objects.all():
#             if all(s in staff.services.all() for s in services) and staff.is_available(start_time, total_duration):
#                 appointment = Appointment.objects.create(
#                     client=user,
#                     staff=staff,
#                     start_time=start_time
#                 )
#                 appointment.services.set(services)
#                 appointment.save()  # Now triggers Event creation safely
#                 return appointment

#         raise serializers.ValidationError("No available staff for selected services and time.")

# class AvailableSlotSerializer(serializers.ModelSerializer):
#     staff = serializers.SerializerMethodField()

#     class Meta:
#         model = Event
#         fields = ['id', 'title', 'start', 'end', 'staff']
#         read_only_fields = ['staff', 'title']

#     def get_staff(self, obj):
#         from .models import Staff
#         try:
#             staff = Staff.objects.get(calendar=obj.calendar)
#             return staff.staff.username
#         except Staff.DoesNotExist:
#             return None

#     def create(self, validated_data):
#         user = self.context['request'].user
#         from .models import Staff
#         try:
#             staff = Staff.objects.get(staff=user)
#             return Event.objects.create(
#                 title="available slot",
#                 calendar=staff.calendar,
#                 **validated_data
#             )
#         except Staff.DoesNotExist:
#             raise serializers.ValidationError("You are not registered as staff.")

#-----------------------------------------------------------available-slotes-below---------------------------------------------------------------------------

# from rest_framework import serializers
# from schedule.models import Event
# from .models import Service, Staff, Appointment
# from django.utils.timezone import make_aware
# from datetime import timedelta, time, datetime
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']

# class StaffSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Staff
#         exclude = ['calendar','is_staff']
#         read_only_fields = ['staff']

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['service_ids'] = [service.id for service in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data


# class AppointmentSerializer(serializers.ModelSerializer):
#     services = ServiceSerializer(many=True, read_only=True)
#     services_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Service.objects.all(),
#         source='services',
#         many=True,
#         write_only=True
#     )
#     staff = StaffSerializer(read_only=True)
#     client = UserSerializer(read_only=True)
#     duration = serializers.SerializerMethodField()
#     available_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = [
#             'id', 'client', 'services', 'services_ids', 'staff', 
#             'start_time', 'end_time', 'status', 'notes',
#             'created_at', 'updated_at', 'duration', 'available_slots'
#         ]
#         read_only_fields = [
#             'end_time', 'created_at', 'updated_at', 
#             'duration', 'available_slots'
#         ]

#     def get_duration(self, obj):
#         return obj.duration.total_seconds() / 60

#     def get_available_slots(self, obj):
#         request = self.context.get('request')
#         if not request or not request.query_params.get('date'):
#             return None
            
#         try:
#             date = datetime.strptime(request.query_params.get('date'), '%Y-%m-%d').date()
#         except:
#             return None
            
#         services = request.query_params.getlist('services[]', [])
#         if not services:
#             return None
            
#         total_duration = sum(
#             Service.objects.filter(id__in=services).values_list('duration', flat=True),
#             timedelta()
#         )
        
#         available_staff = Staff.objects.filter(
#             services__id__in=services
#         ).distinct()
        
#         slots = []
#         for staff in available_staff:
#             staff_slots = staff.get_available_slots(date, total_duration)
#             slots.extend([{
#                 'staff_id': staff.id,
#                 'staff_name': staff.staff.get_full_name(),
#                 'time': slot.strftime('%H:%M')
#             } for slot in staff_slots])
            
#         return sorted(slots, key=lambda x: x['time'])

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
        
#         if value < make_aware(datetime.now()):
#             raise serializers.ValidationError("Appointment cannot be in the past")
            
#         return value

#     # def create(self, validated_data):
#     #     request = self.context.get('request')
#     #     services = validated_data.pop('services', [])
#     #     start_time = validated_data.get('start_time')
#     #     total_duration = sum((s.duration for s in services), timedelta())

#     #     # Find available staff
#     #     available_staff = Staff.objects.filter(
#     #         services__in=services
#     #     ).distinct()
        
#     #     for staff in available_staff:
#     #         if staff.is_available(start_time, total_duration):
#     #             appointment = Appointment.objects.create(
#     #                 client=request.user,
#     #                 staff=staff,
#     #                 start_time=start_time,
#     #                 **validated_data
#     #             )
#     #             appointment.services.set(services)
#     #             return appointment
                
#     #     raise serializers.ValidationError(
#     #         "No available staff for selected services and time."
#     #     )
        

#     # def create(self, validated_data):
#     #     request = self.context.get('request')
        
#     #     # Get and remove start_time from validated_data to avoid duplicate key
#     #     start_time = validated_data.pop('start_time')

#     #     # Extract services from incoming data
#     #     services = validated_data.pop('services', [])
#     #     print("Setting services:", services)
#     #     print("Services:", validated_data.get('services'))

#     #     # Find a staff member who is available
#     #     total_duration = sum((s.duration for s in services), timedelta())
#     #     date = start_time.date()
#     #     staff_queryset = Staff.objects.filter(services__in=services).distinct()
        
#     #     selected_staff = None
#     #     for staff in staff_queryset:
#     #         if staff.is_available(start_time, total_duration):
#     #             selected_staff = staff
#     #             break
        
#     #     if not selected_staff:
#     #         raise serializers.ValidationError("No available staff for selected services and time.")
        
#     #     # # Create appointment
#     #     # appointment = Appointment.objects.create(
#     #     #     client=request.user,
#     #     #     staff=selected_staff,
#     #     #     start_time=start_time,
#     #     #     **validated_data
#     #     # )
#     #     # appointment.services.set(services)
#     #     # appointment.save()


#     #     appointment = Appointment(
#     #         client=request.user,
#     #         staff=selected_staff,
#     #         start_time=start_time,
#     #         **validated_data
#     #     )
                
#     #     # appointment = Appointment(...)
#     #     appointment.save()  # Now appointment has an id
#     #     appointment.services.add(services)  # Now you can add ManyToMany relations   )  # Now you can add ManyToMany relations
        
#     #     return appointment

#     # def create(self, validated_data):
#     #     request = self.context.get('request')
#     #     services = validated_data.pop('services')  # comes from services_ids due to source='services'

#     #     start_time = validated_data.pop('start_time')
#     #     # services = validated_data.pop('services', [])

#     #     total_duration = sum((s.duration for s in services), timedelta())

#     #     staff_queryset = Staff.objects.filter(services__in=services).distinct()

#     #     selected_staff = None
#     #     for staff in staff_queryset:
#     #         if staff.is_available(start_time, total_duration):
#     #             selected_staff = staff
#     #             break

#     #     if not selected_staff:
#     #         raise serializers.ValidationError("No available staff for selected services and time.")

#     #     appointment = Appointment.objects.create(
#     #         client=request.user,
#     #         staff=selected_staff,
#     #         start_time=start_time,
#     #         **validated_data
#     #     )
#     #     appointment.save()  # Now appointment has an id

#     #     appointment.services.set(services)  # ✅ Correct way to assign ManyToMany
#     #     return appointment

#     def create(self, validated_data):
#         request = self.context.get('request')
        
#         services = validated_data.pop('services')  # comes from services_ids due to source='services'
#         start_time = validated_data.pop('start_time')

#         total_duration = sum((s.duration for s in services), timedelta())

#         staff_queryset = Staff.objects.filter(services__in=services).distinct()
#         selected_staff = None
#         for staff in staff_queryset:
#             if staff.is_available(start_time, total_duration):
#                 selected_staff = staff
#                 break

#         if not selected_staff:
#             raise serializers.ValidationError("No available staff for selected services and time.")

#         # Save appointment first
#         appointment = Appointment.objects.create(
#             client=request.user,
#             staff=selected_staff,
#             start_time=start_time,
#             **validated_data
#         )

#         # Now we can set ManyToMany field
#         appointment.services.set(services)

#         return appointment

# class AvailableSlotSerializer(serializers.Serializer):
#     date = serializers.DateField()
#     services = serializers.ListField(
#         child=serializers.IntegerField(),
#         allow_empty=False
#     )

#     def validate_services(self, value):
#         if not Service.objects.filter(id__in=value).exists():
#             raise serializers.ValidationError("One or more services don't exist")
#         return value

#     def get_available_slots(self):
#         date = self.validated_data['date']
#         service_ids = self.validated_data['services']
        
#         services = Service.objects.filter(id__in=service_ids)
#         total_duration = sum((s.duration for s in services), timedelta())
        
#         available_staff = Staff.objects.filter(
#             services__in=services
#         ).distinct()
        
#         slots = []
#         for staff in available_staff:
#             staff_slots = staff.get_available_slots(date, total_duration)
#             slots.extend([{
#                 'staff_id': staff.id,
#                 'staff_name': staff.staff.get_full_name(),
#                 'time': slot.strftime('%H:%M')
#             } for slot in staff_slots])
            
#         return sorted(slots, key=lambda x: x['time'])
    
#     def to_representation(self, instance):
#         """
#         Since this serializer isn't tied to a model, `instance` is ignored.
#         We use validated data to compute and return slot info.
#         """
#         return {
#             'date': self.validated_data['date'].strftime('%Y-%m-%d'),
#             'services': self.validated_data['services'],
#             'available_slots': self.get_available_slots()
#         }
    
# --------------------------------------------------------------available-slots-above------------------------------------------ 


# from rest_framework import serializers
# from schedule.models import Event
# from .models import Service, Staff, Appointment
# from django.utils.timezone import make_aware
# from datetime import timedelta, datetime
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']


# class StaffSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Staff
#         exclude = ['calendar', 'is_staff']
#         read_only_fields = ['staff']

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['service_ids'] = [s.id for s in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data


# class AppointmentSerializer(serializers.ModelSerializer):
#     services = ServiceSerializer(many=True, read_only=True)
#     services_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Service.objects.all(),
#         source='services',
#         many=True,
#         write_only=True
#     )
#     staff = StaffSerializer(read_only=True)
#     client = UserSerializer(read_only=True)
#     duration = serializers.SerializerMethodField()
#     available_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = [
#             'id', 'client', 'services', 'services_ids', 'staff',
#             'start_time', 'end_time', 'status', 'notes',
#             'created_at', 'updated_at', 'duration', 'available_slots'
#         ]
#         read_only_fields = [
#             'end_time', 'created_at', 'updated_at',
#             'duration', 'available_slots'
#         ]

#     def get_duration(self, obj):
#         return obj.duration.total_seconds() / 60 if obj.duration else None

#     def get_available_slots(self, obj):
#         request = self.context.get('request')
#         if not request or not request.query_params.get('date'):
#             return None

#         try:
#             date = datetime.strptime(request.query_params.get('date'), '%Y-%m-%d').date()
#         except:
#             return None

#         services = request.query_params.getlist('services[]', [])
#         if not services:
#             return None

#         service_qs = Service.objects.filter(id__in=services)
#         total_duration = sum((s.duration for s in service_qs), timedelta())

#         available_staff = Staff.objects.filter(
#             services__in=services
#         ).distinct()

#         slots = []
#         for staff in available_staff:
#             staff_slots = staff.get_available_slots(date, total_duration)
#             slots.extend([{
#                 'staff_id': staff.id,
#                 'staff_name': staff.staff.get_full_name(),
#                 'time': slot.strftime('%H:%M')
#             } for slot in staff_slots])

#         return sorted(slots, key=lambda x: x['time'])

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)

#         if value < make_aware(datetime.now()):
#             raise serializers.ValidationError("Appointment cannot be in the past.")

#         return value

#     def create(self, validated_data):
#         request = self.context.get('request')
#         start_time = validated_data.pop('start_time')
#         services = validated_data.pop('services', [])

#         total_duration = sum((s.duration for s in services), timedelta())
#         date = start_time.date()

#         staff_queryset = Staff.objects.filter(services__in=services).distinct()

#         selected_staff = None
#         for staff in staff_queryset:
#             if staff.is_available(start_time, total_duration):
#                 selected_staff = staff
#                 break

#         if not selected_staff:
#             raise serializers.ValidationError("No available staff for selected services and time.")

#         appointment = Appointment.objects.create(
#             client=request.user,
#             staff=selected_staff,
#             start_time=start_time,
#             **validated_data
#         )
#         appointment.services.set(services)
#         appointment.end_time = start_time + total_duration
#         appointment.save()

#         return appointment


# class AvailableSlotSerializer(serializers.Serializer):
#     date = serializers.DateField()
#     services = serializers.ListField(
#         child=serializers.IntegerField(),
#         allow_empty=False
#     )

#     def validate_services(self, value):
#         if not Service.objects.filter(id__in=value).exists():
#             raise serializers.ValidationError("One or more services don't exist.")
#         return value

#     def get_available_slots(self):
#         date = self.validated_data['date']
#         service_ids = self.validated_data['services']

#         services = Service.objects.filter(id__in=service_ids)
#         total_duration = sum((s.duration for s in services), timedelta())

#         available_staff = Staff.objects.filter(
#             services__in=services
#         ).distinct()

#         slots = []
#         for staff in available_staff:
#             staff_slots = staff.get_available_slots(date, total_duration)
#             slots.extend([{
#                 'staff_id': staff.id,
#                 'staff_name': staff.staff.get_full_name(),
#                 'time': slot.strftime('%H:%M')
#             } for slot in staff_slots])

#         return sorted(slots, key=lambda x: x['time'])

#     def to_representation(self, instance):
#         return {
#             'date': self.validated_data['date'].strftime('%Y-%m-%d'),
#             'services': self.validated_data['services'],
#             'available_slots': self.get_available_slots()
#         }

# # appointments/serializers.py
# from rest_framework import serializers
# from .models import Service, Staff, Appointment
# from schedule.models import Event
# from django.utils.timezone import make_aware, now
# from datetime import timedelta, datetime
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']

# class StaffSerializer(serializers.ModelSerializer):
#     service_ids = serializers.SerializerMethodField()

#     class Meta:
#         model = Staff
#         exclude = ['calendar']
#         read_only_fields = ['staff']

#     def get_service_ids(self, obj):
#         return [s.id for s in obj.services.all()]

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data

# class AppointmentSerializer(serializers.ModelSerializer):
#     services = ServiceSerializer(many=True, read_only=True)
#     services_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Service.objects.all(), source='services', many=True, write_only=True
#     )
#     staff = StaffSerializer(read_only=True)
#     client = UserSerializer(read_only=True)
#     duration = serializers.SerializerMethodField()
#     available_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = ['id', 'client', 'services', 'services_ids', 'staff',
#                   'start_time', 'end_time', 'status', 'notes',
#                   'created_at', 'updated_at', 'duration', 'available_slots']
#         read_only_fields = ['end_time', 'created_at', 'updated_at', 'duration', 'available_slots']

#     def get_duration(self, obj):
#         return obj.end_time and (obj.end_time - obj.start_time).total_seconds() / 60

#     def get_available_slots(self, obj):
#         req = self.context.get('request')
#         date = req.query_params.get('date') if req else None
#         services = req.query_params.getlist('services') if req else []
#         if not date or not services:
#             return None
#         try:
#             d = datetime.strptime(date, '%Y-%m-%d').date()
#         except:
#             return None
#         total = sum(Service.objects.filter(id__in=services).values_list('duration', flat=True), timedelta())
#         slots = []
#         for staff in Staff.objects.filter(services__id__in=services).distinct():
#             for t in staff.get_available_slots(d, total):
#                 slots.append({'staff_id': staff.id, 'staff_name': staff.staff.get_full_name(), 'time': t.strftime('%H:%M')})
#         return sorted(slots, key=lambda x: x['time'])

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if value < now():
#             raise serializers.ValidationError("Appointment cannot be in the past")
#         return value

#     def create(self, validated_data):
#         services = validated_data.pop('services')
#         start_time = validated_data.pop('start_time')
#         total = sum((s.duration for s in services), timedelta())
#         chosen = None
#         for s in Staff.objects.filter(services__in=services).distinct():
#             if s.is_available(start_time, total):
#                 chosen = s
#                 break
#         if not chosen:
#             raise serializers.ValidationError("No available staff for selected services and time.")
#         end_time = start_time + total
#         appt = Appointment.objects.create(
#             client=self.context['request'].user,
#             staff=chosen,
#             start_time=start_time,
#             end_time=end_time,
#             status=validated_data.get('status', 'confirmed'),
#             notes=validated_data.get('notes', '')
#         )
#         appt.services.set(services)
#         Event.objects.create(
#             title=f"{appt.client.get_full_name()}'s Appointment",
#             start=appt.start_time,
#             end=appt.end_time,
#             calendar=chosen.calendar,
#             description=f"Services: {', '.join(s.name for s in services)}"
#         )
#         return appt

# class AvailableSlotSerializer(serializers.Serializer):
#     date = serializers.DateField()
#     services = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

#     def to_representation(self, instance):
#         d = self.validated_data['date']
#         svcs = Service.objects.filter(id__in=self.validated_data['services'])
#         total = sum((s.duration for s in svcs), timedelta())
#         result = []
#         for staff in Staff.objects.filter(services__in=svcs).distinct():
#             for t in staff.get_available_slots(d, total):
#                 result.append({'staff_id': staff.id, 'staff_name': staff.staff.get_full_name(), 'time': t.strftime('%H:%M')})
#         return {'date': d.strftime('%Y-%m-%d'), 'services': self.validated_data['services'], 'available_slots': sorted(result, key=lambda x: x['time'])}
    
# --------------------------------------------------Better-code-below------------------------------------------------------------------------------
# # appointments/serializers.py
# from rest_framework import serializers
# from .models import Service, Staff, Appointment,Category
# from schedule.models import Event
# from django.utils.timezone import make_aware, now
# from datetime import timedelta, datetime
# from django.contrib.auth import get_user_model

# User = get_user_model()

# # class ServiceSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Service
# #         fields = '__all__'

# # Add this serializer
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'parent']

# # # Update ServiceSerializer
# # class ServiceSerializer(serializers.ModelSerializer):
# #     category = CategorySerializer()
# #     category_id = serializers.PrimaryKeyRelatedField(
# #         queryset=Category.objects.all(), source='category', write_only=True, allow_null=True, required=False
# #     )

# #     class Meta:
# #         model = Service
# #         fields = ['id', 'name', 'category', 'category_id', 'duration', 'price', 'description']

# class ServiceSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(), source='category', write_only=True, required=False
#     )

#     class Meta:
#         model = Service
#         fields = '__all__'

# # class ServiceSerializer(serializers.ModelSerializer):
# #     category = CategorySerializer()

# #     class Meta:
# #         model = Service
# #         fields = '__all__'

# #     def update(self, instance, validated_data):
# #         category_data = validated_data.pop('category', None)

# #         if category_data:
# #             category_instance = instance.category
# #             for attr, value in category_data.items():
# #                 setattr(category_instance, attr, value)
# #             category_instance.save()

# #         for attr, value in validated_data.items():
# #             setattr(instance, attr, value)
# #         instance.save()
# #         return instance

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']

# class StaffSerializer(serializers.ModelSerializer):
#     service_ids = serializers.SerializerMethodField()

#     class Meta:
#         model = Staff
#         exclude = ['calendar']
#         read_only_fields = ['staff']

#     def get_service_ids(self, obj):
#         return [s.id for s in obj.services.all()]

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data

# class AppointmentSerializer(serializers.ModelSerializer):
#     # Read-only representation 
#     services = ServiceSerializer(many=True, read_only=True)
#     staff = StaffSerializer(read_only=True)
#     client = UserSerializer(read_only=True)

#     # Write-only input for service IDs from frontend
#     services_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Service.objects.all(),
#         source='services',
#         many=True,
#         write_only=True
#     )

#     duration = serializers.SerializerMethodField()
#     available_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = [
#             'id', 'client', 'services', 'services_ids', 'staff',
#             'start_time', 'end_time', 'status', 'notes',
#             'created_at', 'updated_at', 'duration', 'available_slots'
#         ]
#         read_only_fields = [
#             'end_time', 'created_at', 'updated_at',
#             'client', 'staff', 'services', 'duration', 'available_slots'
#         ]

#     def get_duration(self, obj):
#         if obj.end_time and obj.start_time:
#             return (obj.end_time - obj.start_time).total_seconds() / 60
#         return None

#     def get_available_slots(self, obj):
#         req = self.context.get('request')
#         date = req.query_params.get('date') if req else None
#         services = req.query_params.getlist('services') if req else []
#         if not date or not services:
#             return None
#         try:
#             d = datetime.strptime(date, '%Y-%m-%d').date()
#         except:
#             return None
#         total = sum(Service.objects.filter(id__in=services).values_list('duration', flat=True), timedelta())
#         slots = []
#         for staff in Staff.objects.filter(services__id__in=services).distinct():
#             for t in staff.get_available_slots(d, total):
#                 slots.append({
#                     'staff_id': staff.id,
#                     'staff_name': staff.staff.get_full_name(),
#                     'time': t.strftime('%H:%M')
#                 })
#         return sorted(slots, key=lambda x: x['time'])

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if value < now():
#             raise serializers.ValidationError("Appointment cannot be in the past")
#         return value

#     def create(self, validated_data):
#         services = validated_data.pop('services')
#         start_time = validated_data.pop('start_time')
#         total_duration = sum((s.duration for s in services), timedelta())

#         available_staff = None
#         for staff in Staff.objects.filter(services__in=services).distinct():
#             if staff.is_available(start_time, total_duration):
#                 available_staff = staff
#                 break

#         if not available_staff:
#             raise serializers.ValidationError("No available staff for the selected services and time.")

#         end_time = start_time + total_duration
#         appointment = Appointment.objects.create(
#             client=self.context['request'].user,
#             staff=available_staff,
#             start_time=start_time,
#             end_time=end_time,
#             status=validated_data.get('status', 'confirmed'),
#             notes=validated_data.get('notes', '')
#         )
#         appointment.services.set(services)

#         Event.objects.create(
#             title=f"{appointment.client.get_full_name()}'s Appointment",
#             start=appointment.start_time,
#             end=appointment.end_time,
#             calendar=available_staff.calendar,
#             description=f"Services: {', '.join(s.name for s in services)}"
#         )

#         return appointment


# # class AvailableSlotSerializer(serializers.Serializer):
# #     date = serializers.DateField()
# #     services = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

# #     def to_representation(self, instance):
# #         d = self.validated_data['date']
# #         svcs = Service.objects.filter(id__in=self.validated_data['services'])
# #         total = sum((s.duration for s in svcs), timedelta())
# #         result = []
# #         for staff in Staff.objects.filter(services__in=svcs).distinct():
# #             for t in staff.get_available_slots(d, total):
# #                 result.append({'staff_id': staff.id, 'staff_name': staff.staff.get_full_name(), 'time': t.strftime('%H:%M')})
# #         return {'date': d.strftime('%Y-%m-%d'), 'services': self.validated_data['services'], 'available_slots': sorted(result, key=lambda x: x['time'])}
    

# class AvailableSlotSerializer(serializers.Serializer):
#     date = serializers.DateField()
#     services = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

#     def to_representation(self, instance):
#         d = self.validated_data['date']
#         service_ids = self.validated_data['services']
#         svcs = Service.objects.filter(id__in=service_ids)
#         total = sum((s.duration for s in svcs), timedelta())

#         result = []
#         for staff in Staff.objects.filter(services__in=svcs).distinct():
#             for t in staff.get_available_slots(d, total):
#                 result.append({
#                     'staff_id': staff.id,
#                     'staff_name': staff.staff.get_full_name(),
#                     'time': t.strftime('%H:%M')
#                 })

#         return {
#             'date': d.strftime('%Y-%m-%d'),
#             'services': [s.name for s in svcs],  # ✅ Return service names instead of IDs
#             'available_slots': sorted(result, key=lambda x: x['time'])
#         }

# --------------------------------------------------Better-code-Above------------------------------------------------------------------------------

# from rest_framework import serializers
# from .models import Service, Staff, Appointment, Category
# from schedule.models import Event
# from django.utils.timezone import make_aware, now
# from datetime import timedelta, datetime
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class CategorySerializer(serializers.ModelSerializer):
#     subcategories = serializers.SerializerMethodField()

#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'parent', 'subcategories']
#         read_only_fields = ['subcategories']

#     def get_subcategories(self, obj):
#         if hasattr(obj, 'subcategories'):
#             return CategorySerializer(obj.subcategories.all(), many=True).data
#         return []

# class ServiceSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source='category',write_only=True,required=False,allow_null=True)
#     duration_display = serializers.SerializerMethodField()

#     class Meta:
#         model = Service
#         fields = ['id','name','category','category_id','duration','duration_display','price','description','created_at','updated_at']
#         read_only_fields = ['created_at', 'updated_at', 'duration_display']

#     def get_duration_display(self, obj):
#         total_seconds = obj.duration.total_seconds()
#         hours = int(total_seconds // 3600)
#         minutes = int((total_seconds % 3600) // 60)
#         return f"{hours}h {minutes}m" if hours else f"{minutes} minutes"

#     def validate_duration(self, value):
#         if value.total_seconds() < 300:  # Minimum 5 minutes
#             raise serializers.ValidationError("Duration must be at least 5 minutes")
#         if value.total_seconds() > 14400:  # Maximum 4 hours
#             raise serializers.ValidationError("Duration cannot exceed 4 hours")
#         return value

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']
#         read_only_fields = fields

# class StaffSerializer(serializers.ModelSerializer):
#     staff_details = UserSerializer(source='staff', read_only=True)
#     services_details = ServiceSerializer(source='services', many=True, read_only=True)
#     service_ids = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(),source='services',many=True,write_only=True)

#     class Meta:
#         model = Staff
#         fields = ['id','staff_details','service_ids','services_details','buffer_time','working_hours','created_at','updated_at']
#         read_only_fields = ['created_at', 'updated_at']

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['calendar_id'] = instance.calendar.id
#         data['calendar_name'] = instance.calendar.name
#         return data

# class AppointmentSerializer(serializers.ModelSerializer):
#     services = ServiceSerializer(many=True, read_only=True)
#     staff = StaffSerializer(read_only=True)
#     client = UserSerializer(read_only=True)
#     services_ids = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(),source='services',many=True,write_only=True)
#     duration = serializers.SerializerMethodField()
#     available_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = ['id','client','services','services_ids','staff','start_time', 'end_time', 'status', 'notes','created_at', 'updated_at', 'duration', 'available_slots']
#         read_only_fields = ['end_time', 'created_at', 'updated_at','client', 'staff', 'services', 'duration', 'available_slots']

#     def get_duration(self, obj):
#         if obj.end_time and obj.start_time:
#             return (obj.end_time - obj.start_time).total_seconds() / 60
#         return None

#     def get_available_slots(self, obj):
#         req = self.context.get('request')
#         date = req.query_params.get('date') if req else None
#         services = req.query_params.getlist('services') if req else []
        
#         if not date or not services:
#             return None      
#         try:
#             d = datetime.strptime(date, '%Y-%m-%d').date()
#         except ValueError:
#             return None
            
#         total = sum(Service.objects.filter(id__in=services).values_list('duration', flat=True), timedelta())
        
#         slots = []
#         for staff in Staff.objects.filter(services__id__in=services).distinct():
#             for t in staff.get_available_slots(d, total):
#                 slots.append({'staff_id': staff.id,'staff_name': staff.staff.get_full_name() or staff.staff.username,'time': t.strftime('%H:%M')})
#         return sorted(slots, key=lambda x: x['time'])

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if value < now():
#             raise serializers.ValidationError("Appointment cannot be in the past")
        
#         # Business hours validation (example: 9AM-9PM)
#         if value.hour < 9 or value.hour >= 21:
#             raise serializers.ValidationError("Appointments must be between 9AM and 9PM")
            
#         return value

#     def create(self, validated_data):
#         services = validated_data.pop('services')
#         start_time = validated_data.pop('start_time')
#         total_duration = sum((s.duration for s in services), timedelta())

#         available_staff = None
#         for staff in Staff.objects.filter(services__in=services).distinct():
#             if staff.is_available(start_time, total_duration):
#                 available_staff = staff
#                 break

#         if not available_staff:
#             raise serializers.ValidationError({'non_field_errors': ["No available staff for the selected services and time."]})

#         end_time = start_time + total_duration
#         appointment = Appointment.objects.create(client=self.context['request'].user,staff=available_staff,start_time=start_time,end_time=end_time,status=validated_data.get('status', 'confirmed'),notes=validated_data.get('notes', ''))
#         appointment.services.set(services)
#         Event.objects.create(title=f"{appointment.client.get_full_name() or appointment.client.username}'s Appointment",start=appointment.start_time,end=appointment.end_time,calendar=available_staff.calendar,description=f"Services: {', '.join(s.name for s in services)}")

#         return appointment

# class AvailableSlotSerializer(serializers.Serializer):
#     date = serializers.DateField(required=True)
#     services = serializers.ListField(child=serializers.IntegerField(),allow_empty=False,min_length=1)

#     def validate_services(self, value):
#         if not Service.objects.filter(id__in=value).exists():
#             raise serializers.ValidationError("One or more services don't exist")
#         return value

#     def to_representation(self, instance):
#         d = self.validated_data['date']
#         service_ids = self.validated_data['services']
#         svcs = Service.objects.filter(id__in=service_ids)
#         total = sum((s.duration for s in svcs), timedelta())

#         result = []
#         for staff in Staff.objects.filter(services__in=svcs).distinct():
#             for t in staff.get_available_slots(d, total):
#                 result.append({'staff_id': staff.id,'staff_name': staff.staff.get_full_name() or staff.staff.username,'time': t.strftime('%H:%M')})
#         return {'date': d.strftime('%Y-%m-%d'),'services': [{'id': s.id, 'name': s.name} for s in svcs],'available_slots': sorted(result, key=lambda x: x['time'])}

# # variety/appointment/serializers.py
# from rest_framework import serializers
# from .models import Service, Staff, Appointment, Category
# from schedule.models import Event
# from django.utils.timezone import make_aware, now
# from datetime import timedelta, datetime
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'parent']


# class ServiceSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(), source='category', write_only=True, required=False
#     )

#     class Meta:
#         model = Service
#         fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']


# class StaffSerializer(serializers.ModelSerializer):
#     service_ids = serializers.SerializerMethodField()

#     class Meta:
#         model = Staff
#         exclude = ['calendar']
#         read_only_fields = ['staff']

#     def get_service_ids(self, obj):
#         return [s.id for s in obj.services.all()]

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data


# class AppointmentSerializer(serializers.ModelSerializer):
#     # Read-only representations
#     services = ServiceSerializer(many=True, read_only=True)
#     staff = StaffSerializer(read_only=True)
#     client = UserSerializer(read_only=True)

#     # Write-only fields
#     services_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Service.objects.all(),
#         source='services',
#         many=True,
#         write_only=True
#     )
#     staff_id = serializers.PrimaryKeyRelatedField(
#         queryset=Staff.objects.all(),
#         source='staff',
#         write_only=True
#     )

#     duration = serializers.SerializerMethodField()
#     available_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = [
#             'id', 'client', 'services', 'services_ids',
#             'staff', 'staff_id', 'start_time', 'end_time',
#             'status', 'notes', 'created_at', 'updated_at',
#             'duration', 'available_slots'
#         ]
#         read_only_fields = [
#             'id', 'client', 'services', 'staff', 'end_time',
#             'created_at', 'updated_at', 'duration', 'available_slots'
#         ]

#     def get_duration(self, obj):
#         if obj.start_time and obj.end_time:
#             return (obj.end_time - obj.start_time).total_seconds() / 60
#         return None

#     def get_available_slots(self, obj):
#         req = self.context.get('request')
#         date = req.query_params.get('date') if req else None
#         services = req.query_params.getlist('services') if req else []
#         if not date or not services:
#             return None
#         try:
#             d = datetime.strptime(date, '%Y-%m-%d').date()
#         except:
#             return None
#         total = sum(Service.objects.filter(id__in=services).values_list('duration', flat=True), timedelta())
#         slots = []
#         for staff in Staff.objects.filter(services__id__in=services).distinct():
#             for t in staff.get_available_slots(d, total):
#                 slots.append({
#                     'staff_id': staff.id,
#                     'staff_name': staff.staff.get_full_name(),
#                     'time': t.strftime('%H:%M')
#                 })
#         return sorted(slots, key=lambda x: x['time'])

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if value < now():
#             raise serializers.ValidationError("Appointment cannot be in the past.")
#         return value

#     def create(self, validated_data):
#         services = validated_data.pop('services')
#         staff = validated_data.pop('staff')
#         start_time = validated_data.pop('start_time')
#         total_duration = sum((s.duration for s in services), timedelta())

#         if not staff.is_available(start_time, total_duration):
#             raise serializers.ValidationError("Selected staff is not available at the chosen time.")

#         end_time = start_time + total_duration
#         appointment = Appointment.objects.create(
#             client=self.context['request'].user,
#             staff=staff,
#             start_time=start_time,
#             end_time=end_time,
#             status=validated_data.get('status', 'confirmed'),
#             notes=validated_data.get('notes', '')
#         )
#         appointment.services.set(services)

#         # Create calendar event
#         Event.objects.create(
#             title=f"{appointment.client.get_full_name()}'s Appointment",
#             start=appointment.start_time,
#             end=appointment.end_time,
#             calendar=staff.calendar,
#             description=f"Services: {', '.join(s.name for s in services)}"
#         )

#         return appointment


# class AvailableSlotSerializer(serializers.Serializer):
#     date = serializers.DateField()
#     services = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

#     def to_representation(self, instance):
#         d = self.validated_data['date']
#         service_ids = self.validated_data['services']
#         svcs = Service.objects.filter(id__in=service_ids)
#         total = sum((s.duration for s in svcs), timedelta())

#         result = []
#         for staff in Staff.objects.filter(services__in=svcs).distinct():
#             for t in staff.get_available_slots(d, total):
#                 result.append({
#                     'staff_id': staff.id,
#                     'staff_name': staff.staff.get_full_name(),
#                     'time': t.strftime('%H:%M')
#                 })

#         return {
#             'date': d.strftime('%Y-%m-%d'),
#             'services': [s.name for s in svcs],
#             'available_slots': sorted(result, key=lambda x: x['time'])
#         }


# from rest_framework import serializers
# from .models import Service, Staff, Appointment, Category
# from schedule.models import Event
# from django.utils.timezone import make_aware, now
# from datetime import timedelta, datetime
# from django.contrib.auth import get_user_model
# from django.core.cache import cache

# User = get_user_model()


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'parent']


# class ServiceSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(), source='category', write_only=True, required=False
#     )

#     class Meta:
#         model = Service
#         fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']


# class StaffSerializer(serializers.ModelSerializer):
#     service_ids = serializers.SerializerMethodField()

#     class Meta:
#         model = Staff
#         exclude = ['calendar']
#         read_only_fields = ['staff']

#     def get_service_ids(self, obj):
#         return [s.id for s in obj.services.all()]

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data


# class AppointmentSerializer(serializers.ModelSerializer):
#     services = ServiceSerializer(many=True, read_only=True)
#     staff = StaffSerializer(read_only=True)
#     client = UserSerializer(read_only=True)

#     # Write-only fields for POST
#     services_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Service.objects.all(),
#         source='services',
#         many=True,
#         write_only=True
#     )
#     staff_id = serializers.PrimaryKeyRelatedField(
#         queryset=Staff.objects.all(),
#         source='staff',
#         write_only=True
#     )

#     duration = serializers.SerializerMethodField()
#     available_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = [
#             'id', 'client', 'services', 'services_ids',
#             'staff', 'staff_id', 'start_time', 'end_time',
#             'status', 'notes', 'created_at', 'updated_at',
#             'duration', 'available_slots'
#         ]
#         read_only_fields = [
#             'id', 'client', 'services', 'staff', 'end_time',
#             'created_at', 'updated_at', 'duration', 'available_slots'
#         ]

#     def get_duration(self, obj):
#         if obj.start_time and obj.end_time:
#             return (obj.end_time - obj.start_time).total_seconds() / 60
#         return None

#     def get_available_slots(self, obj):
#         req = self.context.get('request')
#         if not req:
#             return None

#         date = req.query_params.get('date')
#         services = req.query_params.getlist('services')

#         if not date or not services:
#             return None

#         try:
#             service_ids = list(map(int, services))
#             d = datetime.strptime(date, '%Y-%m-%d').date()
#         except:
#             return None

#         slots = []

#         for staff in Staff.objects.filter(services__id__in=service_ids).distinct():
#             cache_key = f"available_slots:{staff.id}:{date}:{'-'.join(map(str, service_ids))}"
#             cached = cache.get(cache_key)

#             if cached:
#                 slots.extend(cached)
#             else:
#                 total = sum(Service.objects.filter(id__in=service_ids).values_list('duration', flat=True), timedelta())
#                 for t in staff.get_available_slots(d, total):
#                     slots.append({
#                         'staff_id': staff.id,
#                         'staff_name': staff.staff.get_full_name(),
#                         'time': t.strftime('%H:%M')
#                     })

#         return sorted(slots, key=lambda x: (x['staff_id'], x['time']))

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if value < now():
#             raise serializers.ValidationError("Appointment cannot be in the past.")
#         return value

#     def create(self, validated_data):
#         services = validated_data.pop('services')
#         staff = validated_data.pop('staff')
#         start_time = validated_data.pop('start_time')

#         total_duration = sum((s.duration for s in services), timedelta())
#         if not staff.is_available(start_time, total_duration):
#             raise serializers.ValidationError("Selected staff is not available at the chosen time.")

#         end_time = start_time + total_duration
#         appointment = Appointment.objects.create(
#             client=self.context['request'].user,
#             staff=staff,
#             start_time=start_time,
#             end_time=end_time,
#             status=validated_data.get('status', 'confirmed'),
#             notes=validated_data.get('notes', '')
#         )
#         appointment.services.set(services)

#         Event.objects.create(
#             title=f"{appointment.client.get_full_name()}'s Appointment",
#             start=appointment.start_time,
#             end=appointment.end_time,
#             calendar=staff.calendar,
#             description=f"Services: {', '.join(s.name for s in services)}"
#         )

#         return appointment


# class AvailableSlotSerializer(serializers.Serializer):
#     date = serializers.DateField()
#     services = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

#     def to_representation(self, instance):
#         d = self.validated_data['date']
#         service_ids = self.validated_data['services']
#         svcs = Service.objects.filter(id__in=service_ids)
#         total = sum((s.duration for s in svcs), timedelta())
#         result = []

#         for staff in Staff.objects.filter(services__in=svcs).distinct():
#             cache_key = f"available_slots:{staff.id}:{d.isoformat()}:{'-'.join(map(str, service_ids))}"
#             cached = cache.get(cache_key)
#             if cached:
#                 result.extend(cached)
#             else:
#                 for t in staff.get_available_slots(d, total):
#                     result.append({
#                         'staff_id': staff.id,
#                         'staff_name': staff.staff.get_full_name(),
#                         'time': t.strftime('%H:%M')
#                     })

#         return {
#             'date': d.strftime('%Y-%m-%d'),
#             'services': [s.name for s in svcs],
#             'available_slots': sorted(result, key=lambda x: (x['staff_id'], x['time']))
#         }

# from rest_framework import serializers
# from .models import Service, Staff, Appointment, Category
# from schedule.models import Event
# from django.utils.timezone import make_aware, now
# from datetime import timedelta, datetime, time
# from django.contrib.auth import get_user_model
# from django.core.cache import cache

# User = get_user_model()


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'parent']


# class ServiceSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(), source='category', write_only=True, required=False
#     )

#     class Meta:
#         model = Service
#         fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']


# class StaffSerializer(serializers.ModelSerializer):
#     service_ids = serializers.SerializerMethodField()

#     class Meta:
#         model = Staff
#         exclude = ['calendar']
#         read_only_fields = ['staff']

#     def get_service_ids(self, obj):
#         return [s.id for s in obj.services.all()]

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data


# def build_full_slot_map(staff, date, total_duration):
#     """
#     Return all possible time slots in the working hours, marking each with `available: true/false`
#     """
#     slots = []
#     hours = staff.get_working_hours(date)
#     try:
#         sh, sm = map(int, hours['start'].split(':'))
#         eh, em = map(int, hours['end'].split(':'))
#     except:
#         sh, sm, eh, em = 9, 0, 21, 0

#     working_start = make_aware(datetime.combine(date, time(sh, sm)))
#     working_end = make_aware(datetime.combine(date, time(eh, em)))

#     current = working_start
#     while current + total_duration <= working_end:
#         slots.append({
#             'staff_id': staff.id,
#             'staff_name': staff.staff.get_full_name(),
#             'time': current.strftime('%H:%M'),
#             'available': staff.is_available(current, total_duration)
#         })
#         current += timedelta(minutes=15)
#     return slots


# class AppointmentSerializer(serializers.ModelSerializer):
#     services = ServiceSerializer(many=True, read_only=True)
#     staff = StaffSerializer(read_only=True)
#     client = UserSerializer(read_only=True)

#     # Write-only fields
#     services_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Service.objects.all(),
#         source='services',
#         many=True,
#         write_only=True
#     )
#     staff_id = serializers.PrimaryKeyRelatedField(
#         queryset=Staff.objects.all(),
#         source='staff',
#         write_only=True
#     )

#     duration = serializers.SerializerMethodField()
#     available_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = [
#             'id', 'client', 'services', 'services_ids',
#             'staff', 'staff_id', 'start_time', 'end_time',
#             'status', 'notes', 'created_at', 'updated_at',
#             'duration', 'available_slots'
#         ]
#         read_only_fields = [
#             'id', 'client', 'services', 'staff', 'end_time',
#             'created_at', 'updated_at', 'duration', 'available_slots'
#         ]

#     def get_duration(self, obj):
#         if obj.start_time and obj.end_time:
#             return (obj.end_time - obj.start_time).total_seconds() / 60
#         return None

#     def get_available_slots(self, obj):
#         req = self.context.get('request')
#         if not req:
#             return None

#         date = req.query_params.get('date')
#         services = req.query_params.getlist('services')

#         if not date or not services:
#             return None

#         try:
#             service_ids = list(map(int, services))
#             d = datetime.strptime(date, '%Y-%m-%d').date()
#         except:
#             return None

#         total = sum(Service.objects.filter(id__in=service_ids).values_list('duration', flat=True), timedelta())
#         slots = []

#         for staff in Staff.objects.filter(services__id__in=service_ids).distinct():
#             cache_key = f"available_slots:{staff.id}:{date}:{'-'.join(map(str, service_ids))}"
#             cached = cache.get(cache_key)

#             if cached:
#                 slots.extend(cached)
#             else:
#                 full_map = build_full_slot_map(staff, d, total)
#                 cache.set(cache_key, full_map, timeout=600)
#                 slots.extend(full_map)

#         return sorted(slots, key=lambda x: (x['staff_id'], x['time']))

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if value < now():
#             raise serializers.ValidationError("Appointment cannot be in the past.")
#         return value

#     def create(self, validated_data):
#         services = validated_data.pop('services')
#         staff = validated_data.pop('staff')
#         start_time = validated_data.pop('start_time')

#         total_duration = sum((s.duration for s in services), timedelta())
#         if not staff.is_available(start_time, total_duration):
#             raise serializers.ValidationError("Selected staff is not available at the chosen time.")

#         end_time = start_time + total_duration
#         appointment = Appointment.objects.create(
#             client=self.context['request'].user,
#             staff=staff,
#             start_time=start_time,
#             end_time=end_time,
#             status=validated_data.get('status', 'confirmed'),
#             notes=validated_data.get('notes', '')
#         )
#         appointment.services.set(services)

#         Event.objects.create(
#             title=f"{appointment.client.get_full_name()}'s Appointment",
#             start=appointment.start_time,
#             end=appointment.end_time,
#             calendar=staff.calendar,
#             description=f"Services: {', '.join(s.name for s in services)}"
#         )

#         return appointment


# class AvailableSlotSerializer(serializers.Serializer):
#     date = serializers.DateField()
#     services = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

#     def to_representation(self, instance):
#         d = self.validated_data['date']
#         service_ids = self.validated_data['services']
#         svcs = Service.objects.filter(id__in=service_ids)
#         total = sum((s.duration for s in svcs), timedelta())
#         result = []

#         for staff in Staff.objects.filter(services__in=svcs).distinct():
#             cache_key = f"available_slots:{staff.id}:{d.isoformat()}:{'-'.join(map(str, service_ids))}"
#             cached = cache.get(cache_key)
#             if cached:
#                 result.extend(cached)
#             else:
#                 full_map = build_full_slot_map(staff, d, total)
#                 cache.set(cache_key, full_map, timeout=600)
#                 result.extend(full_map)

#         return {
#             'date': d.strftime('%Y-%m-%d'),
#             'services': [s.name for s in svcs],
#             'available_slots': sorted(result, key=lambda x: (x['staff_id'], x['time']))
#         }

# from rest_framework import serializers
# from .models import Service, Staff, Appointment, Category
# from schedule.models import Event
# from django.utils.timezone import make_aware, now
# from datetime import timedelta, datetime, time
# from django.contrib.auth import get_user_model
# from django.core.cache import cache

# User = get_user_model()


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'parent']


# class ServiceSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(), source='category', write_only=True, required=False
#     )

#     class Meta:
#         model = Service
#         fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']


# class StaffSerializer(serializers.ModelSerializer):
#     service_ids = serializers.SerializerMethodField()

#     class Meta:
#         model = Staff
#         exclude = ['calendar']
#         read_only_fields = ['staff']

#     def get_service_ids(self, obj):
#         return [s.id for s in obj.services.all()]

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['staff_username'] = instance.staff.username
#         data['services'] = [s.name for s in instance.services.all()]
#         data['calendar'] = instance.calendar.name
#         return data


# # 🔧 Util: Build full slots map with `available` flag
# def build_full_slot_map(staff, date, total_duration):
#     slots = []
#     hours = staff.get_working_hours(date)
#     try:
#         sh, sm = map(int, hours['start'].split(':'))
#         eh, em = map(int, hours['end'].split(':'))
#     except:
#         sh, sm, eh, em = 9, 0, 21, 0

#     working_start = make_aware(datetime.combine(date, time(sh, sm)))
#     working_end = make_aware(datetime.combine(date, time(eh, em)))

#     current = working_start
#     while current + total_duration <= working_end:
#         slots.append({
#             'staff_id': staff.id,
#             'staff_name': staff.staff.get_full_name(),
#             'time': current.strftime('%H:%M'),
#             'available': staff.is_available(current, total_duration)
#         })
#         current += timedelta(minutes=15)

#     return slots


# class AppointmentSerializer(serializers.ModelSerializer):
#     services = ServiceSerializer(many=True, read_only=True)
#     staff = StaffSerializer(read_only=True)
#     client = UserSerializer(read_only=True)

#     services_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Service.objects.all(), source='services', many=True, write_only=True
#     )
#     staff_id = serializers.PrimaryKeyRelatedField(
#         queryset=Staff.objects.all(), source='staff', write_only=True
#     )

#     duration = serializers.SerializerMethodField()
#     available_slots = serializers.SerializerMethodField()

#     class Meta:
#         model = Appointment
#         fields = [
#             'id', 'client', 'services', 'services_ids',
#             'staff', 'staff_id', 'start_time', 'end_time',
#             'status', 'notes', 'created_at', 'updated_at',
#             'duration', 'available_slots'
#         ]
#         read_only_fields = [
#             'id', 'client', 'services', 'staff', 'end_time',
#             'created_at', 'updated_at', 'duration', 'available_slots'
#         ]

#     def get_duration(self, obj):
#         if obj.start_time and obj.end_time:
#             return (obj.end_time - obj.start_time).total_seconds() / 60
#         return None

#     def get_available_slots(self, obj):
#         req = self.context.get('request')
#         if not req:
#             return None

#         date = req.query_params.get('date')
#         services = req.query_params.getlist('services')

#         if not date or not services:
#             return None

#         try:
#             service_ids = list(map(int, services))
#             d = datetime.strptime(date, '%Y-%m-%d').date()
#         except:
#             return None

#         total = sum(Service.objects.filter(id__in=service_ids).values_list('duration', flat=True), timedelta())
#         slots = []

#         for staff in Staff.objects.filter(services__id__in=service_ids).distinct():
#             cache_key = f"available_slots:{staff.id}:{date}:{'-'.join(map(str, service_ids))}"
#             cached = cache.get(cache_key)

#             if cached:
#                 slots.extend(cached)
#             else:
#                 full_map = build_full_slot_map(staff, d, total)
#                 cache.set(cache_key, full_map, timeout=600)  # 10 min
#                 slots.extend(full_map)

#         return sorted(slots, key=lambda x: (x['staff_id'], x['time']))

#     def validate_start_time(self, value):
#         if value.tzinfo is None:
#             value = make_aware(value)
#         if value < now():
#             raise serializers.ValidationError("Appointment cannot be in the past.")
#         return value

#     def create(self, validated_data):
#         services = validated_data.pop('services')
#         staff = validated_data.pop('staff')
#         start_time = validated_data.pop('start_time')

#         total_duration = sum((s.duration for s in services), timedelta())

#         if not staff.is_available(start_time, total_duration):
#             raise serializers.ValidationError("Selected staff is not available at the chosen time.")

#         end_time = start_time + total_duration

#         appointment = Appointment.objects.create(
#             client=self.context['request'].user,
#             staff=staff,
#             start_time=start_time,
#             end_time=end_time,
#             status=validated_data.get('status', 'confirmed'),
#             notes=validated_data.get('notes', '')
#         )
#         appointment.services.set(services)

#         # Create calendar event
#         Event.objects.create(
#             title=f"{appointment.client.get_full_name()}'s Appointment",
#             start=start_time,
#             end=end_time,
#             calendar=staff.calendar,
#             description=f"Services: {', '.join(s.name for s in services)}"
#         )

#         # ❗ Invalidate slot cache
#         service_ids = '-'.join(str(s.id) for s in services)
#         cache_key = f"available_slots:{staff.id}:{start_time.date()}:{service_ids}"
#         cache.delete(cache_key)

#         return appointment


# class AvailableSlotSerializer(serializers.Serializer):
#     date = serializers.DateField()
#     services = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

#     def to_representation(self, instance):
#         d = self.validated_data['date']
#         service_ids = self.validated_data['services']
#         svcs = Service.objects.filter(id__in=service_ids)
#         total = sum((s.duration for s in svcs), timedelta())
#         result = []

#         for staff in Staff.objects.filter(services__in=svcs).distinct():
#             cache_key = f"available_slots:{staff.id}:{d.isoformat()}:{'-'.join(map(str, service_ids))}"
#             cached = cache.get(cache_key)

#             if cached:
#                 result.extend(cached)
#             else:
#                 full_map = build_full_slot_map(staff, d, total)
#                 cache.set(cache_key, full_map, timeout=600)
#                 result.extend(full_map)

#         return {
#             'date': d.strftime('%Y-%m-%d'),
#             'services': [s.name for s in svcs],
#             'available_slots': sorted(result, key=lambda x: (x['staff_id'], x['time']))
#         }

from rest_framework import serializers
from .models import Service, Staff, Appointment, Category
from schedule.models import Event
from django.utils.timezone import make_aware, now
from datetime import timedelta, datetime, time
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from pytz import timezone as pytz_timezone

INDIAN_TZ = pytz_timezone('Asia/Kolkata')
User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )

    class Meta:
        model = Service
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class StaffSerializer(serializers.ModelSerializer):
    service_ids = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        exclude = ['calendar']
        read_only_fields = ['staff']

    def get_service_ids(self, obj):
        return [s.id for s in obj.services.all()]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['staff_username'] = instance.staff.username
        data['services'] = [s.name for s in instance.services.all()]
        data['calendar'] = instance.calendar.name
        return data


def build_full_slot_map(staff, date, total_duration):
    slots = []
    hours = staff.get_working_hours(date)
    try:
        sh, sm = map(int, hours['start'].split(':'))
        eh, em = map(int, hours['end'].split(':'))
    except:
        sh, sm, eh, em = 9, 0, 21, 0

    working_start = make_aware(datetime.combine(date, time(sh, sm)), timezone=INDIAN_TZ)
    working_end = make_aware(datetime.combine(date, time(eh, em)), timezone=INDIAN_TZ)

    current = working_start
    while current + total_duration <= working_end:
        slots.append({
            'staff_id': staff.id,
            'staff_name': staff.staff.get_full_name(),
            'time': current.astimezone(INDIAN_TZ).strftime('%H:%M'),
            'available': staff.is_available(current, total_duration)
        })
        current += timedelta(minutes=15)

    return slots


class AppointmentSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    staff = StaffSerializer(read_only=True)
    client = UserSerializer(read_only=True)

    services_ids = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source='services', many=True, write_only=True
    )
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), source='staff', write_only=True
    )

    duration = serializers.SerializerMethodField()
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'client', 'services', 'services_ids',
            'staff', 'staff_id', 'start_time', 'end_time',
            'status', 'notes', 'created_at', 'updated_at',
            'duration', 'available_slots'
        ]
        read_only_fields = [
            'id', 'client', 'services', 'staff', 'end_time',
            'created_at', 'updated_at', 'duration', 'available_slots'
        ]

    def get_duration(self, obj):
        if obj.start_time and obj.end_time:
            return (obj.end_time - obj.start_time).total_seconds() / 60
        return None

    def get_available_slots(self, obj):
        req = self.context.get('request')
        if not req:
            return None

        date = req.query_params.get('date')
        services = req.query_params.getlist('services')

        if not date or not services:
            return None

        try:
            service_ids = list(map(int, services))
            d = datetime.strptime(date, '%Y-%m-%d').date()
        except:
            return None

        total = sum(Service.objects.filter(id__in=service_ids).values_list('duration', flat=True), timedelta())
        slots = []

        for staff in Staff.objects.filter(services__id__in=service_ids).distinct():
            cache_key = f"available_slots:{staff.id}:{date}:{'-'.join(map(str, service_ids))}"
            cached = cache.get(cache_key)

            if cached:
                slots.extend(cached)
            else:
                full_map = build_full_slot_map(staff, d, total)
                cache.set(cache_key, full_map, timeout=600)
                slots.extend(full_map)

        return sorted(slots, key=lambda x: (x['staff_id'], x['time']))

    def validate_start_time(self, value):
        if value.tzinfo is None:
            value = make_aware(value, timezone=INDIAN_TZ)
        else:
            value = value.astimezone(INDIAN_TZ)
        if value < timezone.now().astimezone(INDIAN_TZ):
            raise serializers.ValidationError("Appointment cannot be in the past.")
        return value

    def create(self, validated_data):
        services = validated_data.pop('services')
        staff = validated_data.pop('staff')
        start_time = validated_data.pop('start_time').astimezone(INDIAN_TZ)

        total_duration = sum((s.duration for s in services), timedelta())

        if not staff.is_available(start_time, total_duration):
            raise serializers.ValidationError("Selected staff is not available at the chosen time.")

        end_time = start_time + total_duration

        appointment = Appointment.objects.create(
            client=self.context['request'].user,
            staff=staff,
            start_time=start_time,
            end_time=end_time,
            status=validated_data.get('status', 'confirmed'),
            notes=validated_data.get('notes', '')
        )
        appointment.services.set(services)

        Event.objects.create(
            title=f"{appointment.client.get_full_name()}'s Appointment",
            start=start_time,
            end=end_time,
            calendar=staff.calendar,
            description=f"Services: {', '.join(s.name for s in services)}"
        )

        cache_key = f"available_slots:{staff.id}:{start_time.date()}:{'-'.join(str(s.id) for s in services)}"
        cache.delete(cache_key)

        return appointment


class AvailableSlotSerializer(serializers.Serializer):
    date = serializers.DateField()
    services = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

    def to_representation(self, instance):
        d = self.validated_data['date']
        service_ids = self.validated_data['services']
        svcs = Service.objects.filter(id__in=service_ids)
        total = sum((s.duration for s in svcs), timedelta())
        result = []

        for staff in Staff.objects.filter(services__in=svcs).distinct():
            cache_key = f"available_slots:{staff.id}:{d.isoformat()}:{'-'.join(map(str, service_ids))}"
            cached = cache.get(cache_key)

            if cached:
                result.extend(cached)
            else:
                full_map = build_full_slot_map(staff, d, total)
                cache.set(cache_key, full_map, timeout=600)
                result.extend(full_map)

        return {
            'date': d.strftime('%Y-%m-%d'),
            'services': [s.name for s in svcs],
            'available_slots': sorted(result, key=lambda x: (x['staff_id'], x['time']))
        }
