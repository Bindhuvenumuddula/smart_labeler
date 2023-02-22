from django.contrib import admin

from .models import WebMedia


# Register your models here.
@admin.register(WebMedia)
class WebMediaAdmin(admin.ModelAdmin):
    list_display = ("media_type", "get_user_name", "id")
    list_filter = ("media_type",)
    search_fields = ("media_type", "id")

    @admin.display(ordering='name', description='User')
    def get_user_name(self, obj):
        return obj.user.name
