from django.contrib import admin

# Register your models here.

from django.contrib import admin
from lims.models import Role, Status, Gender, WeekDays, Department, User, Doctor, Menu, SubMenu, DoctorCatagory, DoctorAvailable, DoctorsAway, OpdConfiguration

# Configuring admin model view

class DepartmentFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'dept_name',
    ]
admin.site.register(Department, DepartmentFeatures)

class RoleFeatures(admin.ModelAdmin):   
    list_display = [
        'id',
        'role',
    ]
admin.site.register(Role, RoleFeatures)

class GenderFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'sex',
    ]
admin.site.register(Gender, GenderFeatures)

class WeekDayFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'day_name',
    ]
admin.site.register(WeekDays, WeekDayFeatures)
    
class StatusFeaturers(admin.ModelAdmin):
    list_display = [
        'id',
        'stat',
    ]
admin.site.register(Status, StatusFeaturers)

# class ItemStatusFeatures(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'status',
#     ]
# admin.site.register(ItemStatus, ItemStatusFeatures)

class UserFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'uid',
        'first_name',
        'middle_name',
        'last_name',
        'urole',
        'udept',
        'uaddr',
        'upin',
        'uphn',
        'ustat',
    ]
admin.site.register(User, UserFeatures)

class DoctorCategoryFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'drcat_name'
    ]
admin.site.register(DoctorCatagory, DoctorCategoryFeatures)

class DoctorAvailableFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'available'
    ]
admin.site.register(DoctorAvailable, DoctorAvailableFeatures)

class DoctorFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'dr_uid',
        'dr_regn',
        'council_name',
        'dr_qua',
        'dr_desig',
        'dr_cat',
        'opd_visitchgs',
        'dr_visitchgs',
        'dr_status',
    ]
admin.site.register(Doctor, DoctorFeatures)

class DoctorsAwayFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'leave_from',
        'leave_to'
    ]
admin.site.register(DoctorsAway, DoctorsAwayFeatures)

class OpdConfigurationFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'dr', 
        'week_day', 
        'from_time', 
        'to_time', 
        'max_count', 
        'status', 
    ]
admin.site.register(OpdConfiguration, OpdConfigurationFeatures)

class LaboratoryTypeFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'type_name',
    ] 
# admin.site.register(LaboratoryType, LaboratoryTypeFeatures)

class LaboratoryFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'lab_id',
        'lab_name',
        'lab_type',
        'lab_status',
    ]
# admin.site.register(Laboratory, LaboratoryFeatures)

# NOTE: model registration for the respective roled users

# menus admin user
class MenuFeatures(admin.ModelAdmin):
    list_display = [
        'id', 
        'menus',
        'menu_role',
    ]
admin.site.register(Menu, MenuFeatures)

class SubMenuFeatures(admin.ModelAdmin):
    list_display = [
        'id',
        'sub_menus',
        'menu_name',
    ]
admin.site.register(SubMenu, SubMenuFeatures)
