from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.auth.admin import UserAdmin

from account.models import CustomUser, Profile


class ProfileInline(TabularInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'
    fk_name = 'user'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("phone",)}),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)
