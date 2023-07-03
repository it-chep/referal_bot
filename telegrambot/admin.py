from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(ReferalBase)
class ReferalAdmin(admin.ModelAdmin):
    list_display = ('father_name', 'tg_id', 'sb_id', 'count_referals')


@admin.register(UsersBase)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'username', 'time', 'invite_link')
