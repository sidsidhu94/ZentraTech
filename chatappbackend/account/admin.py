from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import UserAccount
from django.db import models


class AccountAdmin(UserAdmin):
    list_display = ('id','username','email','name','mobilenumber','is_admin','is_staff')
    search_fields = ('email','name')
    readonly_fields = ('id','is_staff')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    ordering = ('id',) 

admin.site.register(UserAccount,AccountAdmin)