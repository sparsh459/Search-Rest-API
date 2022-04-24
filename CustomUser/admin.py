from django.contrib import admin
from CustomUser.models import NewUser

admin.site.site_title = "Custome User Base"
admin.site.site_header = "ALL CUSTOM USERS"

class NewUserAdmin(admin.ModelAdmin):
    list_display=('name','email','dob','createdAt','modifiedAt','is_active', 'is_superuser','is_staff')
    list_display_links=('name','email','dob',)
    list_filter=('createdAt','is_superuser','dob',)

admin.site.register(NewUser,NewUserAdmin)
