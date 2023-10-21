from django.contrib import admin
from home.models import *

# class amenities(admin.ModelAdmin):
#     list_display=("amenity_name")

# class Hotel_booking(admin.ModelAdmin):
#     list_display=("hotel","start_date","end_date","user","booking_type")

# class Hotel_images(admin.ModelAdmin):
#     list_display=("images","hotel")

# class Hotel(admin.ModelAdmin):
#     list_display=("hotel_name","hotel_price","description","hotel_count")
# Register your models here.

# admin.site.register(Amenities)
# admin.site.register(hotel,Hotel)
# admin.site.register(hotel_images,Hotel_images)
# admin.site.register(booking,Hotel_booking)


admin.site.register(Amenities)
admin.site.register(hotel)
admin.site.register(hotel_images)
admin.site.register(booking)
