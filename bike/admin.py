from django.contrib import admin
from .models import Bicycle, RentailHistory

class BicycleAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "price", "username")


admin.site.register(Bicycle, BicycleAdmin)

class RentailHistoryAdmin(admin.ModelAdmin):
    list_display = ("bicycle_name", "rental_cost", "username")

admin.site.register(RentailHistory, RentailHistoryAdmin)