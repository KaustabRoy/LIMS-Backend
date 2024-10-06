from rest_framework import serializers
from lims.models import User, Role, Department, Gender, Status, Menu, SubMenu, Doctor, DoctorCatagory, OpdConfiguration, DoctorsAway, WeekDays

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class DeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class WeekDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekDays
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'uid',
            'first_name',
            'middle_name',
            'last_name',
            'uaddr',
            'upin',
            'uphn',
            'email',
            'urole',
            'udept',
            'usex'
        ]
        depth = 1

class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'uid',
            'first_name',
            'middle_name',
            'last_name',
            'uaddr',
            'upin',
            'uphn',
            'email',
            'urole',
            'udept',
            'usex',
            'password'
        ]

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
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
        depth = 2

class ManageDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
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

class OPDConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpdConfiguration
        fields = [
            'dr',
            'week_day',
            'from_time',
            'to_time',
            'max_count',
            'status',
        ]

class ConfiguredOpdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpdConfiguration
        fields = [
            'dr',
            'week_day',
            'from_time',
            'to_time',
            'max_count',
            'status',
        ]
        depth = 2

class ManageDoctorsAwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorsAway
        fields = [
            'dr_id',
            'leave_from',
            'leave_to'
        ]

class DoctorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorCatagory
        fields = [
            'id',
            'drcat_name',
        ]

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            'id',
            'stat'
        ]

# Menu & Submenu Serializer
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'id',
            'menus'
        ]

class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields = [
            'sub_menus'
        ]