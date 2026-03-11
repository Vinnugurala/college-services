from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, Canteen, MenuItem, FoodOrder, FoodOrderItem, XeroxCenter, XeroxOrder

class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('role', 'phone_number')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number')}),
    )

class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'canteen', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'canteen')
    search_fields = ('student__username', 'student__phone_number')

class XeroxOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'center', 'status', 'created_at')
    list_filter = ('status', 'center')
    search_fields = ('student__username', 'student__phone_number')

admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(Canteen)
admin.site.register(MenuItem)
admin.site.register(FoodOrder, FoodOrderAdmin)
admin.site.register(FoodOrderItem)
admin.site.register(XeroxCenter)
admin.site.register(XeroxOrder, XeroxOrderAdmin)
