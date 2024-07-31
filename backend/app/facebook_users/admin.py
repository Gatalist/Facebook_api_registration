from django.contrib import admin
from .models import FacebookUsers, GenderUsers


@admin.register(FacebookUsers)
class FacebookUsersAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "gender", "is_register_fb", "created", "updated",)
    list_display_links = ("first_name",)


@admin.register(GenderUsers)
class GenderUsersAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created", "updated",)
    list_display_links = ("name",)
