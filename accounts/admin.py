from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from accounts.models import User, Contact


class UserAdmin(admin.ModelAdmin):

    list_display = ('username', 'email','is_staff','is_teacher',
                    'is_student')


admin.site.register(User,UserAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['First_Name','Last_Name','Email_Address','Phone_number','Message',]


admin.site.register(Contact,ContactAdmin)