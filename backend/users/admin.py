from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AccountTier, ImagesUser

# Register your models here.


class ImagesUserAdmin(UserAdmin):
    list_display = ("email", "username", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    #TODO: include account tier and username while registering user via admin panel


admin.site.register(AccountTier)
admin.site.register(ImagesUser, ImagesUserAdmin)
