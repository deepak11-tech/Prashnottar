from django.contrib import admin
from login.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class ProfileInline(admin.StackedInline):
    model=Profile
    can_delete: bool=False
    verbose_name='Profiles'

class CustomizedUserAdmin(UserAdmin):
    inlines=(ProfileInline, )
admin.site.unregister(User)
admin.site.register(User,CustomizedUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('id','user','phone_number','uid')