from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth import get_user_model
User = get_user_model()
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass
