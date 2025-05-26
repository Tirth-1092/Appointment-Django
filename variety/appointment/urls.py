# from rest_framework.routers import DefaultRouter
# from .views import ServiceViewSet, StaffViewSet, AppointmentViewSet
# from django.urls import path, include
# from .views import AvailableSlotsViewSet

# router = DefaultRouter()
# router.register(r'services', ServiceViewSet)
# router.register(r'staff', StaffViewSet, basename='staff')
# router.register(r'book-appointments', AppointmentViewSet, basename='appointment')
# router.register(r'available-slots', AvailableSlotsViewSet, basename='available-slots')

# urlpatterns = [
#     path('', include(router.urls)),
# ]
#-----------------------------------------------------------
# from rest_framework.routers import DefaultRouter
# from .views import ServiceViewSet, StaffViewSet, AppointmentViewSet
# from django.urls import path, include

# router = DefaultRouter()
# router.register(r'services', ServiceViewSet)
# router.register(r'staff', StaffViewSet, basename='staff')
# router.register(r'book-appointments', AppointmentViewSet, basename='appointment')

# urlpatterns = [
#     path('', include(router.urls)),
# ]


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     ServiceViewSet,
#     StaffViewSet,
#     AppointmentViewSet,
#     AvailableSlotViewSet
# )

# router = DefaultRouter()
# router.register(r'services', ServiceViewSet)
# router.register(r'staff', StaffViewSet, basename='staff')
# router.register(r'book-appointments', AppointmentViewSet, basename='appointment')
# router.register(r'available-slots', AvailableSlotViewSet, basename='available-slots')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ServiceViewSet, StaffViewSet, AppointmentViewSet, AvailableSlotViewSet

# router = DefaultRouter()
# router.register(r'services', ServiceViewSet)
# router.register(r'staff', StaffViewSet)
# router.register(r'book-appointments', AppointmentViewSet, basename='appointment')
# router.register(r'available-slots', AvailableSlotViewSet, basename='slot')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ServiceViewSet,StaffViewSet,AppointmentViewSet,AvailableSlotsView, CategoryViewSet)

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'book-appointments', AppointmentViewSet, basename='appointment')
router.register(r'available-slots', AvailableSlotsView, basename='available-slots')
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]