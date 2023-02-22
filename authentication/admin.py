from django.contrib import admin

from authentication.models import CustomUser, UserType


# Register your models here.


@admin.register(UserType)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "is_active")


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "get_user_type")

    @admin.display(ordering='name', description='UserType')
    def get_user_type(self, obj):
        return obj.user_type.name
