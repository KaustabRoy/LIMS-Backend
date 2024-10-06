#NOTE: Rest Functionals import 
from rest_framework import status
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#NOTE: Basic Functionals imports
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import get_object_or_404
from lims.models import *
# from lims.serializers import UserSerializer, AddUserSerializer, RoleSerializer, DeptSerializer, GenderSerializer, StatusSerializer, MenuSerializer, SubMenuSerializer, DoctorSerializer, DoctorCategorySerializer, ManageDoctorSerializer, ManageDoctorsAwaySerializer, WeekDaysSerializer
from lims.serializers import *
from lims.customid import customID, generate_org_uid, generate_laboratory_id

import time
from termcolor import colored
# Create your views here.

User = get_user_model()

class AuthenticateUser(APIView):
    """
    Login user based on valid credentials.
    """

    def post(self, request):
        print(request.data)
        uid = request.data['uid']
        password = request.data['password']
        user = auth.authenticate(uid = uid, password = password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user = user)
            return Response(
                {
                    "token":token.key,
                    "email":user.email,
                    "status": status.HTTP_200_OK
                }
            )
        elif user is None:
            return Response(
                {
                    "token":"Not found.",
                    "emai":"Not found.",
                    "status": status.HTTP_400_BAD_REQUEST
                }
            )


class AuthnticatedUserData(APIView):
    """
    Provides minimal data of authenticated user.

    * Requires token authentication.
    * Only accessible after authentication.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth_user = request.user
        uid = auth_user.uid
        email = auth_user.email
        full_name = f"{auth_user.first_name} {auth_user.last_name}"
        role_serializer = RoleSerializer(instance = auth_user.urole)
        return Response(
            {
                "uid": uid,
                "email": email,
                "full_name": full_name,
                "role": role_serializer.data,
            }
        )


class RoleMenu(APIView):
    """
    View to list all the menus based on authenticated user's role.

    * Requires token authentication.
    * Only accessible after authentication.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        menus = Menu.objects.filter(menu_role = user.urole.id)
        serializer = MenuSerializer(menus, many = True)
        return Response(
            {
                "menus": serializer.data,
                "status": status.HTTP_200_OK
            }
        )

class MenuSubmenu(APIView):
    """
    View to list all the submenus for a selected menu.

    * Requires token authentication.
    * Only accessible after authentication.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, menu_id):
        submenus = SubMenu.objects.filter(menu_name = menu_id)
        serializer = SubMenuSerializer(submenus, many = True)
        return Response(
            {
                "submenus":serializer.data,
                "status": status.HTTP_200_OK
            }
        )

class UserRoleList(APIView):
    """
    View to list all the available user roles.

    * Requires token authentication.
    * Only accessible after authentication.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(instance = roles, many = True)
        return Response(
            {
                "roles": serializer.data,
                "status": status.HTTP_200_OK
            }
        )

class DepartmentList(APIView):
    """
    View to list all the available user deppartments.

    * Requires token authentication.
    * Only accessible after authentication.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        department = Department.objects.all()
        serializer = DeptSerializer(instance = department, many = True)
        return Response(
            {
                "departments": serializer.data,
                "status": status.HTTP_200_OK
            }
        )

class GenderList(APIView):
    """
    View to list all gender options.

    * Requires token authentication.
    * Only accessible after authentication.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gender = Gender.objects.all()
        serializer = GenderSerializer(instance = gender, many = True)
        return Response(
            {
                "genders": serializer.data,
                "status": status.HTTP_200_OK
            }
        )

class StatusList(APIView):
    """
    View to list all gender options.
    """
    def get(self, request):
        act_status = Status.objects.all()
        serializer = StatusSerializer(instance = act_status, many = True)
        return Response(
            {
                "stat": serializer.data,
                "status": status.HTTP_200_OK
            }
        )
    
class WeekDaysList(APIView):
    """
    View to list all days in a week.

    * Requires token authentication.
    * Only accessible after authentication.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = WeekDays.objects.all()
        serializer = WeekDaysSerializer(instance = days, many = True)
        return Response(
            {
                "days": serializer.data,
                "status": status.HTTP_200_OK
            }
        )

class ListUsers(APIView):
    """
    View to list and manage all the users in the system.

    * Requires Token authentication.
    * Only users with admin role can access this view.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, uid = None):
        if not uid:
            users = User.objects.all()
            serializer = UserSerializer(instance = users, many = True)
            return Response(
                {
                    "users": reversed(serializer.data),
                    "status": status.HTTP_200_OK
                }
            )
        elif uid:
            user = User.objects.get(uid = uid)
            serializer = UserSerializer(instance = user)
            return Response(
                {
                    "user": serializer.data,
                    "status": status.HTTP_200_OK
                }
            )
    
    
    def post(self, request):
        serializer = AddUserSerializer(data = request.data)
        if serializer.is_valid():
            # try:
                # serializer.save(uid = customID(int(request.data['urole'])))
                serializer.save(uid = generate_org_uid(previous_uid = User.objects.last().uid))
                user = User.objects.get(email = request.data['email'])
                user.set_password(request.data['password'])
                user.save()
                if user.urole == Role.objects.get(role = "doctor"):
                    ltst_uid = User.objects.last().uid
                    dr_uid = User.objects.get(uid = ltst_uid)
                    doctor = Doctor(dr_uid = dr_uid)
                    doctor.save()
                # token = Token.objects.create(user = user)
                print(serializer.data)
                return Response(
                    {
                        "message": "User created successfully.",
                        "status": status.HTTP_201_CREATED
                    }
                )
            # except Exception as httpe:
            #     print(colored(f"Http Exception : {httpe}", "red"))
            #     return Response(
            #         {
            #             "message": "Form not filled properly.",
            #             "status": status.HTTP_501_NOT_IMPLEMENTED
            #         }
            #     )
        else:
            print(colored(f"Serializer Exception : {serializer.errors}"))
            return Response(
                    {
                        "message": "Form not filled properly.", 
                        "status": status.HTTP_400_BAD_REQUEST
                    }
                )
        
    def put(self, request, uid):
        try:
            user = User.objects.get(uid = uid)
            serializer = AddUserSerializer(instance = user, data = request.data, partial = True)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "user": serializer.data,
                        "status": status.HTTP_200_OK
                    }
                )
            else:
                return Response(
                    {
                        "status": status.HTTP_304_NOT_MODIFIED
                    }
                )
        except User.DoesNotExist:
            return Response(
                {
                    "status": status.HTTP_204_NO_CONTENT
                }
            )
        except Exception:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST
                }
            )
        
class SearchUser(APIView):
    """
    View to search and list the users progressively.

    * Requires Token authentication.
    * Only users with admin role can access this view.
    """

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, fname = None):
        users = User.objects.filter(first_name__icontains = fname)
        serializer = UserSerializer(instance = users, many = True)
        return Response(
            {
                "users": serializer.data,
                "status": status.HTTP_200_OK
            }
        )

class DoctorCategoryList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dr_categories = DoctorCatagory.objects.all()
        serializer = DoctorCategorySerializer(instance = dr_categories, many = True)
        return Response(
            {
                "dr_categories": serializer.data,
                "status": status.HTTP_200_OK
            }
        )
        
class ManageDocotrs(APIView):
    """
    View to list and manage all the users in the system.

    * Requires Token authentication.
    * Only users with admin role can access this view.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, uid = None):
        if not uid:
            doctors = Doctor.objects.all()
            print(doctors)
            serializer = DoctorSerializer(instance = doctors, many = True)
            return Response(
                {
                    "doctors": reversed(serializer.data),
                    "status": 200
                }
            )
        elif uid:
            user = User.objects.get(uid = uid)
            doctor = Doctor.objects.get(dr_uid = user)
            print(doctor)
            serializer = DoctorSerializer(instance = doctor)
            return Response(
                {
                    "doctor": serializer.data,
                    "status": 200
                }
            )

    def post(self, request):
        pass

    def patch(self, request, uid):
        try:
            user = User.objects.get(uid = uid)
            doctor = Doctor.objects.get(dr_uid = user)
            serializer = ManageDoctorSerializer(instance = doctor, data = request.data, partial = True)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "doctor": serializer.data,
                        "status": status.HTTP_200_OK
                    }
                )
            else:
                return Response(
                    {
                        "error": serializer.errors,
                        "status": status.HTTP_304_NOT_MODIFIED
                    }
                )
        except User.DoesNotExist:
            return Response(
                {
                    "status": status.HTTP_204_NO_CONTENT
                }
            )
        except Exception:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST
                }
            )

class ManageDoctorsAway(APIView):
    """
    View to list and manage all the users in the system.

    * Requires Token authentication.
    * Only users with admin role can access this view.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctors_away = DoctorsAway.objects.all()
        serializer = ManageDoctorsAwaySerializer(instance = doctors_away)
        return Response(
            {
                "doctors_away": serializer.data,
                "status": status.HTTP_200_OK
            }
        )

    def post(self, request):
        serializer = ManageDoctorsAwaySerializer(data = request.data)
        if serializer.is_valid():
            return Response(
                {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                }
            )
        else:
            return Response(
                {
                    "error": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST
                }
            )

    def put(self, request):
        pass

class SearchDoctor(APIView):
    """
    View to search and list the doctors progressively.

    * Requires Token authentication.
    * Only users with admin role can access this view.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, fname = None):
        doctors = Doctor.objects.filter(dr_uid__first_name__icontains = fname)
        serializer = DoctorSerializer(instance = doctors, many = True)
        return Response(
            {
                "doctors": serializer.data,
                "status": status.HTTP_200_OK
            }
        )
    
class ConfigureOPD(APIView):
    """
    View to search and list the doctors progressively.

    * Requires Token authentication.
    * Only users with admin role can access this view.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, uid_day = None):
        if uid_day is not None:
            uid, day = uid_day.split("_")
            print(f"Editing OPD for uid - {uid} of {day}")
        elif uid_day is None:
            opds = OpdConfiguration.objects.all()
            serializer = ConfiguredOpdListSerializer(instance = opds, many = True)
            return Response(
                {
                    "opd_list": serializer.data,
                    "status": status.HTTP_200_OK                
                }
            )

    def post(self, request):
        serializer = OPDConfigSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": serializer.data,
                    "status": status.HTTP_201_CREATED
                }
            )
        else:
            return Response(
                {
                    "message": serializer.errors,
                    "status": status.HTTP_501_NOT_IMPLEMENTED
                }
            )

    def put(self, request):
        pass

    def patch(self, request):
        pass