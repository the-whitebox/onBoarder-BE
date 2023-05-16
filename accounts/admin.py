from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User,
    UserProfile, Role
)


# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Roles'), {'fields': ('role',)}),
        (_('Business'), {'fields': ('business',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    # inlines = (UserProfileInline,)