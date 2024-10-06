from django.db import models
from django.contrib.auth.models import AbstractUser
from lims.manager import UserManager


# Create your models here.
class Role(models.Model):
    role = models.CharField(max_length = 50, null = True)

    def __str__(self) -> str:
        return self.role

class Gender(models.Model):
    sex = models.CharField(max_length = 10, null = True)

    def __str__(self) -> str:
        return self.sex
    
class WeekDays(models.Model):
    day_name = models.CharField(max_length = 30, null = True, blank = True)

    def __str__(self) -> str:
        return self.day_name

class Status(models.Model):
    stat = models.CharField(max_length = 10, null = True, blank = True)

    def __str__(self) -> str:
        return self.stat

class Department(models.Model):
    dept_name = models.CharField(max_length = 200, null = True, blank = True)

    def __str__(self) -> str:
        return self.dept_name

class User(AbstractUser):
    username = None
    middle_name = models.CharField(max_length = 50, null = True, blank = True)
    urole = models.ForeignKey(Role, on_delete = models.CASCADE, null = True) 
    uaddr = models.CharField(max_length = 200, null = True, blank = True)
    upin = models.CharField(max_length = 15, null = True, blank = True)
    uphn = models.CharField(max_length = 25, null = True, blank = True)
    uid = models.CharField(max_length = 20, null = True, blank = True, unique = True)
    udept = models.ForeignKey(Department, on_delete = models.CASCADE, null = True)
    usex = models.ForeignKey(Gender, on_delete = models.CASCADE, null = True)
    ustat = models.ForeignKey(Status, on_delete = models.CASCADE, default = 1)

    objects = UserManager()

    USERNAME_FIELD = 'uid'

    REQUIRED_FIELDS = []

    def __str__(self):
            return f"{self.uid} - {self.first_name} {self.middle_name} {self.last_name} - {self.email}"
    
class DoctorCatagory(models.Model):
    drcat_name = models.CharField(max_length = 100, null = True, blank = True)
    
    def __str__(self) -> str:
        return self.drcat_name
    
class DoctorAvailable(models.Model):
    available = models.CharField(max_length = 25, null = True, blank = True)

    def __str__(self) -> str:
        return self.available

class Doctor(models.Model):
    dr_uid = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    dr_regn = models.CharField(max_length = 50, null = True, blank = True)
    council_name = models.CharField(max_length = 300, null = True, blank = True)
    dr_qua = models.CharField(max_length = 200, null = True, blank = True)
    dr_desig = models.CharField(max_length = 200, null = True, blank = True)
    dr_cat = models.ForeignKey(DoctorCatagory, on_delete = models.CASCADE, null = True)
    opd_visitchgs = models.FloatField(default = 0.00)
    dr_visitchgs = models.FloatField(default = 0.00)
    dr_status = models.ForeignKey(DoctorAvailable, on_delete = models.CASCADE, default = 1, null = True)

    def __str__(self) -> str:
        return f"{self.dr_uid.uid} - {self.dr_uid.first_name} {self.dr_uid.middle_name} {self.dr_uid.last_name}"

class DoctorsAway(models.Model):
    dr_id = models.ForeignKey(Doctor, on_delete = models.CASCADE, null = True, blank = True)
    leave_from = models.DateField(null = True, blank = True)
    leave_to = models.DateField(null = True, blank = True)


class OpdConfiguration(models.Model):
    dr = models.ForeignKey(Doctor, on_delete = models.CASCADE, null = True)
    week_day = models.ForeignKey(WeekDays, on_delete = models.CASCADE, null = True)
    from_time = models.CharField(max_length = 50, null = True, blank = True)
    to_time = models.CharField(max_length = 50, null = True, blank = True)
    max_count = models.IntegerField(default = 0)
    status = models.ForeignKey(Status, on_delete = models.CASCADE, null = True)

# class LaboratoryType(models.Model):
#     type_name = models.CharField(max_length = 100, null = True, blank = True)

#     def __str__(self) -> str:
#         return self.type_name
    
# class Laboratory(models.Model):
#     lab_id = models.CharField(max_length = 20, unique = True, null= True, blank = True)
#     lab_name = models.CharField(max_length = 100, null = True, blank = True)
#     lab_type = models.ForeignKey(LaboratoryType, on_delete = models.CASCADE, null = True)
#     lab_status = models.ForeignKey(Status, on_delete = models.CASCADE, null = True, default = 1)
    

# Menus & Submenus
class Menu(models.Model):
    menus = models.CharField(max_length = 50, null = True, blank = True)
    menu_role = models.ForeignKey(Role, on_delete = models.CASCADE, null = True)

    def __str__(self) -> str:
        return self.menus
    

class SubMenu(models.Model):
    sub_menus = models.CharField(max_length = 50, null = True, blank = True)
    menu_name = models.ForeignKey(Menu, on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.sub_menus