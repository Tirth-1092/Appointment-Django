# from django.contrib import admin
# from .models import Service,Staff,Appointment

# admin.site.register(Service)
# admin.site.register(Staff)
# admin.site.register(Appointment)

from django.contrib import admin
from .models import Service, Staff, Appointment,Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price')
    search_fields = ('name',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff', 'get_services')
    filter_horizontal = ('services',)
    
    def get_services(self, obj):
        return ", ".join([s.name for s in obj.services.all()])
    get_services.short_description = 'Services'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'get_services', 'staff', 'start_time', 'status')
    list_filter = ('status', 'staff', 'start_time')
    search_fields = ('client__username', 'staff__staff__username')
    filter_horizontal = ('services',)
    
    def get_services(self, obj):
        return ", ".join([s.name for s in obj.services.all()])
    get_services.short_description = 'Services'