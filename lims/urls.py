from django.urls import path
from lims import views

urlpatterns = [
    path('login', views.AuthenticateUser.as_view()),
    path('auth_user_data', views.AuthnticatedUserData.as_view()),
    path('role_menu', views.RoleMenu.as_view()),
    path('menu_submenu/<int:menu_id>', views.MenuSubmenu.as_view()),
    path('user_role_list', views.UserRoleList.as_view()),
    path('department_list', views.DepartmentList.as_view()),
    path('sex_list', views.GenderList.as_view()),
    path('active_status_list', views.StatusList.as_view()),
    path('days_list', views.WeekDaysList.as_view()),

    path('user_list', views.ListUsers.as_view()),
    path('user_list/<str:uid>', views.ListUsers.as_view()),
    path('search_user/<str:fname>', views.SearchUser.as_view()),

    path('dr_category_list', views.DoctorCategoryList.as_view()),
    path('doctor_list', views.ManageDocotrs.as_view()),
    path('doctor_list/<str:uid>', views.ManageDocotrs.as_view()),

    path('opd_config', views.ConfigureOPD.as_view()),
    path('opd_config/<str:uid_day>', views.ConfigureOPD.as_view()),

    path('doctors_away', views.ManageDoctorsAway.as_view()),
    path('search_doctor/<str:fname>', views.SearchDoctor.as_view())
]